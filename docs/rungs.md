# The rung table

All seven rung meanings are authored and adopted by this package. They are
marked `adopted`, not `[CANDIDATE — needs ratification]`; a consuming host may
enforce a stricter policy but is not the source of these public meanings.

| Rung | Label | Status | Art. 14 measure | Obligation (summary) | `.lg` |
|---|---|---|---|---|---|
| L0 | operator-controlled | adopted | Art. 14(4)(d) | Per-step approval: every action referred to a human operator, unconditionally. | `lg/L0.lg` |
| L1 | propose/notify | **adopted** | Art. 14(4)(a) | After-the-fact notify on every action; auto-release restricted to reversible effects. | `lg/L1.lg` |
| L2 | partial | adopted | Art. 14(4)(c) | Required grade L2 on the gate (below it, withheld pending oversight); consequential-effect actions reserved to a human reviewer. | `lg/L2.lg` |
| L3 | standby-conditional | adopted | Art. 14(4)(d)+(e) | Financial / irreversible / external-publish footprints clear only via reservation to a standby human (sign-off). | `lg/L3.lg` |
| L4 | supervised automation | **adopted** | Art. 14(4)(b)+(e) | Unattended, under continuous-monitoring and intervention/stop obligations; separate quorum-gated separation-of-duties on self-widening. | `lg/L4.lg` |
| L5 | full automation | adopted | Art. 26 | Auto-releases with ex-post audit + kill-switch obligations; every high-stakes footprint prohibited outright. | `lg/L5.lg` |
| L6 | self-governing | adopted | — | No meaningful oversight is possible; every action prohibited, unconditionally. Never granted. | `lg/L6.lg` |

The rung tokens themselves are never hardcoded: `rung_table()` builds its keys
from `oversight_ladder.ladder.grade_levels()`, so a rung added or renamed in
`grades.json` surfaces as a `KeyError` rather than as a silently stale row.

## The biometric two-person add-on (separate, optional)

`lg/biometric-two-person.lg` expresses AI Act **Art. 14(5)** — two-person
verification for biometric-identification deployments — as a `reserve`
declaration with a conjunction target (two distinct human parties; quorum
distinctness over `provenance`, spec §6). It is:

- **outside the core L0-L6 ladder** — no rung's `.lg` file references it,
  and it references no rung;
- **not a default floor** — it declares no `grade` at all, so it does not
  attach to any rung automatically; a deployment attaches it alongside
  whichever rung otherwise governs a biometric-ID deployment;
- **separable** — `tests/test_biometric_addon_separable.py` checks the core
  ladder compiles and resolves with no reference to it.

`oversight_ladder.biometric` carries the add-on's metadata:
`BIOMETRIC_ADDON_FILE`, `ART_14_5_CITE`, `SUMMARY`, and
`biometric_addon_path()`.
