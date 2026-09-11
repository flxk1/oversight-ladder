# Planes, caveats, and what was consumed

## Plane division

- **loomground grounds** the requirement — the declarations in `lg/*.lg` are
  what this layer asserts a rung obliges, expressed in loomground's
  vocabulary (`reserve`, `prohibit`, `obligation`, `redress`, quorum).
- **RVND enforces** — the actual gate (`action_gate.py`) and the oversight
  certificate (`oversight_extractor.py` / `oversight_compose.py` /
  `rvnd-pack/commons/commons.json`'s `meaningful-oversight` facets) are
  RVND's, cited here by name, not reimplemented. This repo names which
  three facets (`human-authorship-attestation`, `reasoned-rationale`,
  `considered-record`) a rung's human-facing obligation point should
  satisfy when exercised; whether they are in fact satisfied is RVND's
  concern, not this repo's.
- **ctrl surfaces** — a plan-time need (`max(grade, ...)`) is ctrl's
  concern; nothing here plans or dispatches anything.

Dependency direction: `oversight-ladder` -> `loomground-governance` /
`loomground-escalation`, never the reverse. Nothing here is referenced by
either plane, and no repo in the family catalogue declares it as a
dependency.

This package expresses obligations, the same way loomground's own spec (§1)
says of itself: expressing a measure here does not, by itself, satisfy any
legal obligation. Conformance is a property of the `.lg` patches; legal
compliance is a matter of law and policy, outside this repo.

## Caveats (durable, no slop)

- **The 0-6 shape and the L6 ceiling are the ecosystem's choice**, grounded
  in ISO/IEC 22989 §5.13 + the automation-levels literature (Sheridan 1978;
  PSW00) — **not** verbatim from ISO/SAE (SAE's own scale stops at level 5)
  and **not** from the AI Act (which is risk-tiered, not autonomy-graded).
  `grades.json` says this itself: "policy supplies the levels, their
  meanings, and their order; the language owns only the comparison rule."
  Do not read "L0-L6" as *the* ISO/SAE ladder.
- **RVND doc drift, not touched here.** RVND's `action_gate.py` still carries
  a stale inline comment (`autonomy_grade: str = "L1"  # L0..L4`) against the
  shipped L0-L6 ladder its own `grade_levels()` (from
  `adapters/policy_languages.py`) actually returns. That file is outside
  this repo's territory (`rvnd-repos/` is read-only here); it is RVND's
  owner's to fix.
- **A second, newly-found doc-drift: the loomground-governance skill's
  cached validator is stale.** The plugin-cached copy of the checker
  (`~/.claude/plugins/cache/loomground/loomground-governance/0.1.0/skills/
  loomground/loomground.py`) still carries a five-rung `GRADES` table
  (`L0..L4`), not grades.json's current seven — it correctly *rejects* any
  patch declaring `L5`/`L6` (`grade 'L5' is not a level of the active
  ladder`). This repo's `L5.lg`/`L6.lg` are not ill-formed: `loomground-ref`
  (`loomground-repos/loomground-ref/loomground.py`), the second conformance
  implementation, whose `GRADES` table already carries `L0..L6`, accepts
  both. `oversight_ladder/validator.py` runs both engines and
  `test_skill_engine_staleness_is_isolated_to_l5_l6` pins the discrepancy
  rather than routing around it silently. This is a finding for the skill's
  maintainer (the plugin cache is outside this repo's territory; not fixed
  here).
- **`lg_path()` and `biometric_addon_path()` assume the source checkout.**
  Both resolve `Path(__file__).resolve().parents[2] / "lg"`, which is
  `<repo>/lg` from `src/oversight_ladder/`, but resolves under the
  interpreter's `lib/` directory once the package is installed into a
  site-packages tree — so `.lg` paths, and `validator.validate_file()` on
  them, are usable from a checkout rather than from an installed wheel.
  `lg/` is not declared as package data in `pyproject.toml`.

## What was consumed vs authored

**Consumed, read-only, never copied:**
- the ladder tokens + total order (`loomground-governance/standard/
  vocabulary/grades.json`) — read at runtime via `ladder.grade_levels()`,
  never hardcoded (see `tests/test_ladder_tokens.py`'s AST-level guard);
- the comparison/gating rule (`SPEC.md` §6, §7.1) — expressed only through
  `grade <level>` clauses in the `.lg` patches, never reimplemented;
- the ceiling calculus (`loomground_escalation.ceiling()` /
  `autonomy_verdict()`) — imported straight off
  `loomground-escalation/src` (no pip install, no vendoring);
- the grammar/checker (`loomground-ref/loomground.py`, cross-checked against
  the loomground-governance skill's cached copy) — used to validate every
  `.lg` patch; no parser of its own;
- the RVND-authoritative rung meanings for L0/L2/L3/L5/L6
  (`action_gate.py`, `test_autonomy_ladder_iso.py`) — cited, not
  reimplemented;
- the oversight-certificate facet names (`rvnd-pack/commons/commons.json`'s
  `meaningful-oversight`) — cited by name in `obligations.CERTIFICATE_
  FACETS`, no compose logic reimplemented.

**Authored here:**
- the per-rung `.lg` patches (`lg/*.lg`) mapping each rung to loomground
  declarations;
- the AI Act Art. 14(4) letter mapping and the working meanings for L1/L4
  (ratified, marked adopted);
- `obligations.py`'s rung table, `escalation_bridge.py`'s wiring from a
  ceiling to an obligation, `biometric.py`'s add-on metadata, and
  `validator.py`'s dual-engine wrapper;
- the biometric two-person add-on `.lg` patch.

## Layout

```
lg/                          the .lg patches — one per rung, plus the add-on
src/oversight_ladder/
  ladder.py                  reads grades.json; builds a loomground_escalation.Ladder
  obligations.py             the per-rung obligation table (rung -> RungObligation)
  escalation_bridge.py       ceiling() -> rung -> obligation
  validator.py               .lg compile-check, both engines (ref + skill)
  biometric.py               the add-on's metadata + path
  _paths.py                  locates the sibling loomground-repos checkout
tests/                       see below
```

## Running the tests

```
cd oversight-ladder
python3 -m pytest tests/ -v
```

Requires a sibling `loomground-repos/` checkout (the conventional layout
under `Projects/`); override with `OVERSIGHT_LADDER_LOOMGROUND_REPOS` if it
lives elsewhere. Requires `loomground_solver` importable (loomground-
escalation's one dependency).

41 tests, all passing. Coverage:
- `test_ladder_tokens.py` — ladder read from grades.json, not hardcoded;
- `test_lg_compiles.py` — every rung + the add-on compiles WELL-FORMED
  (loomground-ref for all eight; the skill's cached engine for L0-L4 + the
  add-on, with the L5/L6 staleness pinned as its own test);
- `test_rung_lookup.py` — the rung -> obligation table, status labels,
  certificate facets;
- `test_escalation_integration.py` — `loomground_escalation.ceiling()`
  feeding this layer's lookup, including the fail-closed unassessed-factor
  case and the binding/why() reporting;
- `test_biometric_addon_separable.py` — the add-on's separability.
