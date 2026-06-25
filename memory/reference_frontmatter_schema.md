---
name: reference_frontmatter_schema
description: Required frontmatter for every memory file; provenance and priority tiers.
metadata:
  type: reference
  priority: 2
---

# Memory file format

Every memory is **one file holding one fact**, with YAML frontmatter followed by the body.

```markdown
---
name: <short-kebab-case-slug>          # must equal the filename (without .md)
description: <one-line summary>         # used to decide relevance during recall
metadata:
  type: user | feedback | project | reference
  priority: 1 | 2 | 3 | 4              # 1 = load-bearing, 4 = paused/archival
  provenance: <where this came from>    # e.g. "principal, 2026-06-11" or a source link
---

<the fact>

**Why:** <for feedback/project — the reasoning behind it>
**How to apply:** <the concrete trigger → action>

Related: [[other-memory-slug]]
```

## The four types
- **user** — who the principal is (role, expertise, preferences).
- **feedback** — guidance on *how to work*: corrections and confirmed approaches. Always
  carries the **why**, so it generalizes instead of overfitting to one incident.
- **project** — ongoing work, goals, constraints not derivable from code or history.
  Relative dates are converted to absolute.
- **reference** — pointers to external resources or internal schemas/APIs.

## Rules
- **One fact per file.** If a file grows two ideas, split it and add a one-line pointer in
  the index.
- **Index everything.** A memory not listed in `MEMORY.md` is effectively forgotten —
  the index is what's loaded each session.
- **Link liberally.** `[[slug]]` cross-links related memories; a link to a not-yet-written
  slug marks something worth writing later.
- **Line ceilings.** Each tier has a hard line limit; a `memory-cap` hook enforces it on write.
- **Priority drives load order.** Priority-1 files are the constitution-adjacent ones read
  first on restart; priority-4 are paused and skipped.
