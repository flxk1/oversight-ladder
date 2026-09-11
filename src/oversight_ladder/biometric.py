# SPDX-License-Identifier: Apache-2.0
"""The biometric two-person add-on (AI Act Art. 14(5)) — separate, optional.

Deliberately NOT part of :mod:`oversight_ladder.obligations`'s rung table:
it declares no `grade` at all (see lg/biometric-two-person.lg), so it is
attachable to a deployment at any rung rather than being a grade-independent
floor every rung inherits. This module's only job is to say where the patch
lives and to make "separable" a checkable property (see
tests/test_biometric_addon_separable.py): the file is self-contained and no
L0-L6 patch references it.
"""
from __future__ import annotations

from pathlib import Path

_LG_DIR = Path(__file__).resolve().parents[2] / "lg"

BIOMETRIC_ADDON_FILE = "biometric-two-person.lg"
ART_14_5_CITE = "Art. 14(5)"
SUMMARY = (
    "Two-person verification for biometric-identification deployments: a "
    "reservation with a conjunction target (two distinct parties, quorum "
    "distinctness over provenance) — attach alongside any rung's gate for a "
    "`biometric-id-decision` kind. Not a default floor; not part of the core "
    "L0-L6 ladder."
)


def biometric_addon_path() -> Path:
    return _LG_DIR / BIOMETRIC_ADDON_FILE
