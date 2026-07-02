# Seeding durable facts from curated files

The seeder reads curated memory files **read-only** and *nominates* candidates — it never
promotes (promotion is a human decision) and never writes back to the memory files.

**What it keeps / skips**
- Skips headings, code fences, horizontal rules, checkbox lines and dated journal lines —
  process and episodes are not durable facts.
- Keeps only lines that assert a clear facet (role, spouse, location, legal form, preference),
  matched across scripts via Unicode lookarounds.
- Resolves entities through the alias table; an unkeyable entity is rejected.
- **Verbatim check:** a fact must be a literal (whitespace-normalized) substring of its own
  source line, or it is rejected — no provenance washing.

**Run it safely**
1. Isolation + backup: set the data dir; back up the database before seeding.
2. Run the seeder over the agent's curated files + its alias table. Expect N nominated,
   0 promoted, some rejected. A refuse-real guard prevents writing into real memory without an
   explicit token.
3. Dump the nominated facts to the **owner** (not to yourself) for yes/no/correction. A
   correction is reject + re-nominate, not an edit that bypasses the gate.
4. Promote only the confirmed facts. A unique index keeps at most one current truth per
   (entity, attribute) — split facets before promoting.
5. Fact-check counts before/after; confirm no other agent's database changed.

**Rollback:** restore the database from the pre-seed backup, or un-promote individual facts.
