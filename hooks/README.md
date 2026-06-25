# Hooks — the reflex layer

The constitution and memory tell the agent *what it should do*. Hooks are what make some of
it **non-optional**. A hook is a small script the harness runs **before** (or after) a tool
call — file edits, shell commands, sending a message. It can inspect the action and **block
it**, or inject a reminder into the agent's context. Crucially, a hook fires even when the
model has "forgotten" the rule — it's a reflex, not a memory.

The design rule: **a hook only for the irreversible.** Guarding every action puts the robot
in a cast — every move trips over a check. Guard the things you can't take back, and leave
the rest to judgment.

> The actual hook source is withheld from this public excerpt: the guard's trigger lists
> embed the very confidential terms it exists to protect. Below is what each hook does. The
> wiring (`settings.json`) is included with paths genericized.

## The four hooks

### `guard` (PreToolUse)
The safety + anti-capitulation gate. Runs before risky tool calls and before outbound
messages. It blocks actions that would:
- send email, post publicly, or delete the principal's files without explicit approval;
- touch an absolutely-red topic in any outbound channel;
- declare a task finished while the success criterion is provably unmet (the
  "never capitulate" enforcement — words alone don't hold under pressure, so a mechanical
  gate does).

### `retrieve-lessons` (PreToolUse)
Before an edit / command, it matches the current action against the failures ledger and
injects the relevant past mistake as `trigger → correct_action`. This is how a written
lesson actually changes behaviour instead of decaying in a file no one re-reads.

### `memory-cap` (PreToolUse on writes)
Enforces per-file line ceilings on memory. If a write would push a file past its tier limit,
it flags it — keeping memory lean so every morning's full re-read stays fast and cheap.

### `telegram-stop` (Stop)
When a turn ends, it checks that a substantive answer actually reached the messaging channel
the principal watches — catching the failure mode where the agent "answers" only into a
terminal the principal can't see.

## Why hooks instead of just rules

Rules live in the prompt and depend on the model choosing to follow them. Under load,
ambiguity, or a clever framing, a rule can be rationalized away. A hook can't be talked out
of its check — it's code. So the few rules that must *never* slip (don't leak the red zone,
don't fake completion, don't send without approval) are backed by a hook, and the rest stay
as guidance.
