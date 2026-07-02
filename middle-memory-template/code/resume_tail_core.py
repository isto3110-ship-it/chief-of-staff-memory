"""Seamless-restart core (anonymized reference).

The universal, reusable part of the pattern: a WRITER that stamps a compact
`resume_tail` into the agent's state file mid-turn, and a BOOT reader that
reconciles before surfacing it. Per-agent adaptation: the state path, the
schema, and the "is this unit of work closed?" predicate.

Rails: temp + fsync + atomic replace + parent-dir fsync; a file lock guards
read-modify-write races. A torn base state does not crash the checkpointer and
does not clobber the file — the tail goes to a sidecar for hand-recovery.
"""
import fcntl
import os
import re
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, date, timezone
from pathlib import Path
import yaml

RESUME_TAIL_TTL_DAYS = 7.0

# --- minimal schema: allow the resume_tail key, else strict save would reject it
STATE_SCHEMA = {
    "required": [],                 # <-- the agent's own required keys
    "allowed": {"resume_tail"},     # <-- plus the agent's own keys
    "types": {"resume_tail": dict},
}


class SchemaError(ValueError):
    pass


def validate(data, schema, strict=True, label="state"):
    if not isinstance(data, dict):
        if strict:
            raise SchemaError(f"{label}: top level must be a dict")
        return [f"{label}: not a dict"]
    errs = [f"missing required: {k}" for k in schema.get("required", []) if k not in data]
    for k, t in schema.get("types", {}).items():
        if k in data and not isinstance(data[k], t):
            errs.append(f"{k}: wrong type")
    if errs and strict:
        raise SchemaError(f"{label}: " + "; ".join(errs))
    return errs


# --- atomic rail -----------------------------------------------------------
def _acquire_lock(fd, timeout):
    deadline = time.monotonic() + timeout
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except BlockingIOError:
            if time.monotonic() >= deadline:
                raise TimeoutError("state lock timeout")
            time.sleep(0.1)


def load_yaml(path):
    p = Path(path)
    if not p.exists() or not p.read_text().strip():
        return {}
    r = yaml.safe_load(p.read_text())
    return r if isinstance(r, dict) else {}


def _write_atomic(path, data):
    p = Path(path).resolve()
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=p.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
        try:
            dfd = os.open(p.parent, os.O_DIRECTORY)
            os.fsync(dfd)
            os.close(dfd)
        except OSError:
            pass
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass


@contextmanager
def atomic_yaml(path, timeout=30.0, schema=None):
    p = Path(path).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    lock = p.with_suffix(p.suffix + ".lock")
    with open(lock, "a+") as lf:
        _acquire_lock(lf, timeout)
        data = load_yaml(path)
        yield data
        if schema is not None:
            validate(data, schema, strict=True, label=p.name)
        _write_atomic(path, data)


def sidecar(state_path):
    return str(state_path) + ".resume_tail"


# --- writer ----------------------------------------------------------------
def write_resume_tail(state_path, *, goal=None, subtask=None, next_step=None,
                      files=None, blockers=None, uncommitted=None,
                      task_id=None, updated_at=None, timeout=30.0):
    """Overwrite a compact resume_tail. Only non-None fields stored. Torn base
    state -> sidecar, main file untouched."""
    if updated_at is None:
        updated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tail = {}
    for k, v in (("goal", goal), ("subtask", subtask), ("next_step", next_step),
                 ("files", files), ("blockers", blockers),
                 ("uncommitted", uncommitted), ("task_id", task_id)):
        if v is not None:
            tail[k] = v
    tail["updated_at"] = updated_at
    try:
        with atomic_yaml(state_path, timeout=timeout, schema=STATE_SCHEMA) as data:
            data["resume_tail"] = tail
    except (yaml.YAMLError, SchemaError):
        _write_atomic(sidecar(state_path), {"resume_tail": tail})
        return tail
    try:
        os.unlink(sidecar(state_path))
    except OSError:
        pass
    return tail


# --- boot read + reconcile + surface --------------------------------------
def read_resume_tail(state_path):
    """Never raises on a corrupt state. Returns (tail_or_None, warning)."""
    warning, data = None, None
    if os.path.exists(state_path):
        try:
            data = yaml.safe_load(open(state_path))
        except Exception as e:
            warning, data = f"state unparseable ({type(e).__name__})", None
        if data is not None and not isinstance(data, dict):
            warning, data = "state root not a dict", None
    tail = (data or {}).get("resume_tail")
    if tail is not None and not isinstance(tail, dict):
        return None, "resume_tail not a dict"
    if isinstance(tail, dict) and tail:
        return tail, None
    sc = sidecar(state_path)
    if os.path.exists(sc):
        try:
            s = yaml.safe_load(open(sc))
            st = s.get("resume_tail") if isinstance(s, dict) else None
            if isinstance(st, dict) and st:
                return st, warning
        except Exception:
            pass
    return None, warning


def _age_days(tail):
    raw = tail.get("updated_at")
    if raw is None:
        return None
    if isinstance(raw, datetime):
        dt = raw
    elif isinstance(raw, date):
        dt = datetime(raw.year, raw.month, raw.day)
    else:
        try:
            dt = datetime.fromisoformat(str(raw).strip())
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0


def reconcile(tail, is_closed):
    """is_closed(task_id)->bool is the agent's own 'work finished?' predicate.
    Returns (status, reason). status in {live, stale, aged}. Unknown = NOT closed
    (losing an in-flight tail is worse than one extra line)."""
    if not tail:
        return ("stale", "empty")
    tid = tail.get("task_id")
    if tid and is_closed(str(tid)):
        return ("stale", f"unit {tid} closed")
    age = _age_days(tail)
    if age is not None and age > RESUME_TAIL_TTL_DAYS:
        return ("aged", f"{int(age)}d without re-stamp")
    return ("live", "open")


def format_lines(tail, is_closed, redact=lambda s: s or ""):
    if not tail:
        return []
    status, reason = reconcile(tail, is_closed)
    if status == "stale":
        return []
    if status == "aged":
        return [f"(resume_tail expired — {reason}; not resuming)"]
    goal = str(tail.get("goal", "") or "").strip()
    nxt = str(tail.get("next_step", "") or "").strip()
    head = redact(goal) if goal else "(in-flight work)"
    if nxt:
        head = f"{head} / {redact(nxt)}"
    lines = [f"## resume here: {head[:400]}"]
    for label, key in (("subtask", "subtask"), ("files", "files"),
                       ("blockers", "blockers"), ("uncommitted", "uncommitted")):
        v = tail.get(key)
        if not v:
            continue
        rendered = ", ".join(map(str, v)) if isinstance(v, (list, tuple)) else str(v)
        if rendered.strip():
            lines.append(f"- {label}: {redact(rendered)[:240]}")
    if tail.get("task_id"):
        lines.append(f"- task_id: {tail['task_id']} (still open)")
    return lines
