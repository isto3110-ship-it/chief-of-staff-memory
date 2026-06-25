# The ~2-hour onboarding interview

When a fresh agent is first installed, it doesn't start with a personality — it starts with
a blank `memory/` and a README. The first thing it does is **interview its new owner**.
Over roughly two hours, that conversation is what turns a brilliant amnesiac into *your*
chief of staff: every answer becomes a memory file, and those files are what the agent
re-reads each morning forever after.

This file describes that interview — what it's for, how it's structured, and what it writes.

## Why an interview, not a form

A form gives you fields; a conversation gives you *why*. The agent needs not just "I run
three businesses" but how you make decisions, what you never want touched without asking,
how you like to be spoken to, and where the landmines are. So the onboarding is a guided
dialogue: the agent asks, listens, reflects back what it heard, and writes it down in front
of you — correcting on the spot when it got something wrong.

It runs in plain language, one topic at a time, and it's resumable: if you stop at the
60-minute mark, it picks up exactly where it left off next session.

## The arc (six passes, ~20 min each)

1. **Who you are.** Role, the businesses/projects you juggle, your working day, your
   languages. → writes the *user* profile and seeds the project boards.

2. **How you decide & how you talk.** Risk appetite, what "good" looks like to you, tone
   you want (formal vs. casual, terse vs. detailed), pet peeves. → writes `IDENTITY.md`
   and the first *feedback* memos (e.g. "no time estimates", "lead with the win").

3. **The projects.** One pass per major track: goal, current status, key people, the next
   concrete step, what "done" means. → one *project* board per track, each with a success
   criterion in your own words.

4. **Boundaries & the red zone.** What the agent may do freely (green), what it must ask
   about the first time (yellow), and what it must *never* do without explicit confirmation
   (red) — plus the absolutely-red topics that never leave your machine at all. → writes the
   confidentiality protocol and the autonomy rules.

5. **The tools & the channels.** Which mailboxes, which chats/groups go where, what the
   agent is allowed to touch, where heavy files live vs. the working brain. → writes the
   routing and storage-tier memos.

6. **How you want it to learn.** How you'll give feedback ("log this mistake"), how it
   should handle being unsure, how often to check in. → seeds the failures ledger and the
   learning-loop rules.

## What you have at the end

- A populated `memory/` — a `user` profile, an `IDENTITY.md`, one board per project, the
  confidentiality and autonomy rules, routing and storage memos, and an indexed `MEMORY.md`.
- A constitution (`CLAUDE.md`) tuned to your boundaries.
- An agent that, on its very next restart, reads all of the above and shows up already
  knowing who you are — and that keeps getting sharper as you correct it.

## Ground rules during the interview

- **One question at a time**, in human language — no jargon, no documentation references.
- **Reflect back** each answer before writing it, so misunderstandings are caught live
  (voice answers especially can be mis-transcribed).
- **Nothing destructive, nothing sent outward** during onboarding — it only writes local
  memory files, and asks before anything with side effects.
- **Resumable** — long is fine; it remembers where you stopped.
