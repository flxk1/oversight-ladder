# oversight-ladder

**What is the overseer owed at this autonomy grade?**

Human-oversight obligations keyed to loomground's L0-L6 autonomy ladder.

## Problem

An autonomy grade fixes how much a system may do unattended; it leaves the
overseer's duty unstated. This names one obligation per rung.

## Install

```
pip install "oversight-ladder @ git+https://github.com/flxk1/oversight-ladder@v0.1.0"
```

The ladder, the ceiling calculus and the `.lg` checker are read at runtime from
a sibling `loomground-repos/` checkout; `OVERSIGHT_LADDER_LOOMGROUND_REPOS`
points at it elsewhere. `loomground_solver` must be importable.

## Usage

```python
from oversight_ladder.ladder import autonomy_ladder
from oversight_ladder.escalation_bridge import resolve_with_escalation
autonomy_ladder()                       # puts loomground_escalation on sys.path
from loomground_escalation import Factor
ob, esc = resolve_with_escalation(
    [Factor("data-sensitivity", "L2"), Factor("reversibility", "L4")], delegated="L5")
print(esc.granted, esc.binding)
print(ob.label, ob.art14, ob.lg_file)
```

## Example

```
in : delegated L5 · data-sensitivity caps L2 · reversibility caps L4
out: L2 ('data-sensitivity',)
     partial Art. 14(4)(c) L2.lg
```

## Interface

- `ladder`: `grade_levels()` · `grade_grounding()` · `ladder_info()` ·
  `autonomy_ladder()` — read from `standard/vocabulary/grades.json`
- `obligations`: `rung_table()` · `obligation_for(rung)` → `RungObligation(rung,
  label, status, art14, summary, lg_file, certificate_facets, grounding)` ·
  `lg_path(rung)` · `CERTIFICATE_FACETS`
- `escalation_bridge`: `resolve(factors, delegated=)` ·
  `resolve_with_escalation(factors, delegated=)`
- `validator`: `validate_text(src, engine="ref")` · `validate_file(path,
  engine="skill")` → `ValidationResult`
- `biometric`: `biometric_addon_path()`; declarations in `lg/L0.lg` …
  `lg/L6.lg` and `lg/biometric-two-person.lg`
- rung table, Art. 14 letters, the two-person add-on: [docs/rungs.md](docs/rungs.md)

## Family

Assurance artifacts. It mints no ladder of its own: the L0-L6 tokens come from
`loomground-governance`, the ceiling calculus from `loomground-escalation`, the
`.lg` checker from `loomground-ref`, each read off a checkout on disk.
`pyproject.toml` declares zero dependencies, so the package installs and
imports standalone; the reads above are what want the checkout present. Plane
division, caveats, and consumed versus authored:
[docs/planes.md](docs/planes.md).

## Status

0.1.0 · 41 tests ([running them](docs/planes.md#running-the-tests)) · Python
>=3.10 · zero declared dependencies

## License

Apache-2.0 `LICENSES/Apache-2.0.txt` · `REUSE.toml`
