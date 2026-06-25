# MEMORY.md — the memory index

> The always-loaded index of an agent's file-based memory: **one line per memory file**,
> grouped by theme. Loaded into context every session so the agent knows *what it knows*.
> This is an anonymized, representative version — confidential project/people/client entries
> have been removed; the structure and the non-sensitive architectural entries are real.

## 🚨 Read first on restart (handoff)
- Dashboard / current focus — the one or two things in flight right now.
- Open marathons — multi-session efforts with their progress file.

## Identity (canonical)
- [IDENTITY.md](IDENTITY.md) — single source for character, tone, style. See the constitution's identity block.

## Principal — profile
- Identity & work style — who the principal is and how he likes to work.
- (Confidential profile entries — family, social graph, finances — live only on the local machine and are **not** indexed here.)

## Boards (projects)
- One file per active project: goal, status, next steps, key people.
- (Confidential client/partner boards are excluded from this public index.)

## Principles
- [principles_core.md](principles_core.md) — cross-review every phase (never self-approve); smoke-test before "done"; the tired-indicator; pattern-grep before acting.

## Honesty / verification / quality (feedback)
- Fact vs assumption — a "fact" drives decisions only after a check; otherwise say "I assume".
- [failures.md](failures.md) — registry of recurring errors, `trigger → correct_action`; feeds the learning loop.
- Cross-verify load-bearing hypotheses with a second model before acting.
- Pursuit of 10/10 — polish artifacts over several passes; "9.5, close enough" = reject.
- Quality over speed — reread before output; no typos, no language-mixing.
- Pre-completion checklist — criterion → verify → full output → traceability.

## Communication & tone (feedback)
- Writing style — short, clean, no jargon, no hype.
- No emotion projection — quote literally, don't impute feelings.
- No time estimates — just do it and report by fact.
- Lead with the win — the best option stated up front as the recommendation.
- More autonomy, fewer questions — decide and come back with a result.
- One message per event — don't mirror the same content to two chats.

## Procedures
- Session continuity — context pickup, event-driven state, journal, deny-list.
- Task queue — add now / touch / wait / done; a hook blocks "I'm on it" without a queue entry.
- Memory git + lock — auto-commit + read-only lock + sentinel unlock.
- CLI reference — email / tasks / vault: commands + flow.
- Confidentiality — the absolute protocol for red-zone topics.

## Reference (infra / schema)
- [reference_frontmatter_schema.md](reference_frontmatter_schema.md) — required frontmatter, provenance, priority tiers.
- Event log — the event-log API and action types.
- Lazy-code ladder — a checklist before writing code: stop at the first rung that holds.
- Hook infrastructure — where hooks live and how they load without a restart (see [`../hooks/`](../hooks/)).

## Micro-learnings
- One-line operational lessons (append-only) — written here, not in this index.
