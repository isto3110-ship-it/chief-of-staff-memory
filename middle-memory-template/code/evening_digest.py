#!/usr/bin/env python3
"""Evening facts digest (anonymized reference, optional part 4).

Once a day: the top few facts of the day from middle memory. Nominated durable
facts (awaiting review) first, then fresh observations from today. Empty -> an
honest "no new facts today". Sent via curl to a messenger's Bot API (a plain
HTTP client's default user-agent can be rejected by a CDN-fronted API).

Fill from the agent's own config; never hardcode a real token or chat id:
  DB   -> the agent's data-dir/claude-mem.db
  ENV  -> path to the messenger .env (holds the bot token)
  CHAT -> recipient id
"""
import json
import sqlite3
import subprocess
import sys
from datetime import datetime

DB = "~/agent-data/<name>/claude-mem.db"
ENV = "<path>/.env"
CHAT = "<chat_id>"


def bot_token():
    for line in open(ENV, encoding="utf-8"):
        line = line.strip()
        if line.startswith("BOT_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("no BOT_TOKEN in .env")


def top_facts(limit=3):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    items = []
    for r in con.execute(
        "SELECT entity_canon, attribute, fact FROM durable_facts "
        "WHERE status='nominated' ORDER BY observed_at_epoch DESC LIMIT ?", (limit,)
    ):
        attr = f" · {r['attribute']}" if r["attribute"] else ""
        items.append((f"{r['entity_canon']}{attr}: {r['fact']}", "to review"))
    if len(items) < limit:
        midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        since = int(midnight.timestamp() * 1000)
        for r in con.execute(
            "SELECT title, subtitle FROM observations WHERE created_at_epoch >= ? "
            "AND type IN ('discovery','decision','change') ORDER BY id DESC LIMIT ?",
            (since, limit - len(items))
        ):
            text = r["title"] + (f" — {r['subtitle']}" if r["subtitle"] else "")
            items.append((text, "recorded"))
    con.close()
    return items


def main():
    dry = "--dry" in sys.argv
    facts = top_facts()
    today = datetime.now().strftime("%d.%m")
    if facts:
        lines = [f"Top facts of the day ({today}):"]
        for i, (text, kind) in enumerate(facts, 1):
            mark = " — yes/no/correction?" if kind == "to review" else ""
            lines.append(f"{i}. {text}{mark}")
    else:
        lines = [f"{today}: no new facts recorded to middle memory today."]
    msg = "\n".join(lines)
    if dry:
        print(msg)
        return
    out = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"https://api.telegram.org/bot{bot_token()}/sendMessage",
         "-d", f"chat_id={CHAT}", "--data-urlencode", f"text={msg}"],
        capture_output=True, text=True, timeout=30,
    )
    resp = json.loads(out.stdout or "{}")
    if not resp.get("ok"):
        print(f"SEND FAILED: {out.stdout[:300]}", file=sys.stderr)
        sys.exit(1)
    print(f"sent msg {resp['result']['message_id']}")


if __name__ == "__main__":
    main()
