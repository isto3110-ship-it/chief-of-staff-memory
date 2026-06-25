# Chief of Staff — memory & harness

An anonymized look inside a **real, running AI chief-of-staff agent**: the constitution it
boots from, how its file-based memory is organized, the hooks that enforce its hard rules,
and the two-hour interview that gives a fresh install its personality.

This is not a framework or a product — it's the actual scaffolding one agent runs on, with
the private parts removed. Names of people, clients, projects, finances, IDs and absolute
paths are stripped; the structure and the non-sensitive content are reproduced faithfully.

The agent is **Kaira** — a daily working partner that runs many parallel projects for one
person, lives on a small always-on machine, and talks mostly through Telegram.

## The anatomy

Every agent on this base shares the same six parts:

| Part | What it is |
|------|------------|
| **Brain** | the language model — thinks, but remembers nothing between sessions |
| **Memory** | plain text files on disk — re-read every wake-up; this is what makes it a *person*, not an amnesiac |
| **Harness** | the runtime (Claude Code) — terminal, files, web, email, messenger: how the brain acts |
| **Hooks** | small guard scripts that fire *before* an action — reflexes that hold even when the brain "forgot" |
| **Projects** | one dossier file per area of the owner's life — switch contexts without losing the thread |
| **Skills** | learned procedures — how to write emails, build decks, run a calendar |

## What's in here

- **[`CLAUDE.md`](CLAUDE.md)** — the constitution: identity + the 10 rules + boundaries.
  Always loaded, kept under ~150 lines on purpose.
- **[`memory/`](memory/)** — the file-based memory (see structure below).
- **[`hooks/`](hooks/)** — what the reflex layer does and how it's wired.
- **[`onboarding-interview.md`](onboarding-interview.md)** — the ~2-hour interview that
  populates a fresh agent's memory from a conversation with its new owner.

---

## How the memory is structured

The memory is the heart of the system. The design goal: an agent that reads its *entire*
memory at every launch and still boots fast, cheap, and focused. That forces discipline.

### One fact per file, indexed
Each memory is a single small Markdown file holding **one fact**, with YAML frontmatter
(`name`, `description`, `type`, `priority`). A master index — [`MEMORY.md`](memory/MEMORY.md) —
holds **one line per file**. The index is what's loaded into context every session, so a
file that isn't in the index is effectively forgotten. (Format spec:
[`reference_frontmatter_schema.md`](memory/reference_frontmatter_schema.md).)

### Four kinds of memory
- **user** — who the principal is (role, expertise, preferences).
- **feedback** — *how to work*: corrections and confirmed approaches, each carrying its
  **why** so it generalizes. (e.g. [`principles_core.md`](memory/principles_core.md),
  [`IDENTITY.md`](memory/IDENTITY.md).)
- **project** — one board per track of work: goal, status, next step, what "done" means.
- **reference** — schemas, APIs, infra pointers.

### Two storage tiers
- **Fast disk = the brain** — runtime state, memory, configs, code.
- **Bulk disk = heavy assets** — video/audio masters, research PDFs, archives. Heavy media
  never lands on the system disk.

### Line ceilings, git, and locks
- Every file has a **hard line limit** by tier; a `memory-cap` hook enforces it on write.
  Outgrew it → compress, or split it off with a one-line pointer in the index. Bloated
  memory = a slow, scattered, expensive agent.
- `memory/` is **git-tracked** with a once-a-minute auto-commit; constitution-adjacent
  files are locked read-only and edited only through an explicit unlock-with-reason.

### A learning loop, not a junk drawer
Mistakes don't just pile up. Each one is distilled into a **pattern** in the failures
ledger ([`failures.md`](memory/failures.md)) as `trigger → correct_action`, and a
`retrieve-lessons` hook surfaces the relevant one *before* the agent repeats it. Memory that
corrects behaviour, not memory that merely accumulates.

### Lifecycle of a fact
```
something learned ─▶ written as one memory file ─▶ one-line pointer added to MEMORY.md
        ▲                                                      │
        └────────── corrected/merged/retired ◀── re-read every session, applied, refined
```

---

## A note on scope

This agent is deliberately **single-user and small**. It does not aim to be a multi-tenant
platform, an orchestration framework, or an enterprise observability stack — those are
explicit non-goals. The interesting part isn't scale; it's how little structure it takes to
make a model show up every day already knowing who you are.

*Everything here is anonymized. It's shared to show how the thing is built, not to ship a product.*
