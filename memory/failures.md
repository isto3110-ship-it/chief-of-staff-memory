---
name: failures
description: Registry of recurring mistakes — trigger → correct_action. Feeds the learning loop.
metadata:
  type: feedback
  priority: 2
---

# Failures ledger

Append-only registry of the agent's recurring mistakes. Each entry is a **pattern**, not a
diary line: a `trigger` (the situation that sets up the error) and the `correct_action`
(what to do instead). Before an edit or command, a `retrieve-lessons` hook surfaces the
entries whose trigger matches the current action, so the same rake isn't stepped on twice.

> The examples below are illustrative (synthetic), to show the format. The live ledger is
> private.

---

**[F001] Claiming "done" from memory instead of from the source.**
- trigger: about to report a task complete based on what I *think* the state is.
- correct_action: read the actual state / event log first; only then say "done". A claim of
  completeness is never satisfied by a partial check.

**[F002] Guessing a missing parameter under time pressure.**
- trigger: a request is missing a date, amount, or recipient, and a reply is expected fast.
- correct_action: stop and ask one clarifying question. A wrong confident action costs more
  than a five-second question — especially in the red zone (email, deletion, anything
  confidential).

**[F003] Treating "found in N places" as "fixed everywhere".**
- trigger: I patched an issue in the obvious spot and assume that's all of them.
- correct_action: search every class of location (code, config, cron, scheduled jobs,
  databases) before declaring it generalized.

**[F004] Reporting PARTIAL after a single method.**
- trigger: one approach didn't reach the goal, so I'm tempted to say "not possible".
- correct_action: change the *class* of method (different source / tool / provider /
  standard of proof). PARTIAL is only legitimate after several genuinely different classes
  were tried.

**[F005] Editing locked state without announcing it.**
- trigger: about to edit a config / scheduled job / schema / locked memory file.
- correct_action: announce the edit in one line first; back up; verify by fact after.
