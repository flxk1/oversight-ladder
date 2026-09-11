# SPDX-License-Identifier: Apache-2.0
"""Locate the sibling loomground-repos checkout this package reads.

Local-only repo: no pin, no vendoring, no package install of the planes it
consumes. Everything here is a READ off the checkout on disk. Override with
the OVERSIGHT_LADDER_LOOMGROUND_REPOS env var if the checkout lives somewhere
other than the conventional sibling of this repo.
"""
from __future__ import annotations

import os
from pathlib import Path


def loomground_repos_dir() -> Path:
    env = os.environ.get("OVERSIGHT_LADDER_LOOMGROUND_REPOS")
    if env:
        p = Path(env).expanduser().resolve()
    else:
        # this file: <repo>/src/oversight_ladder/_paths.py -> <repo>/../loomground-repos
        p = (Path(__file__).resolve().parents[2] / ".." / "loomground-repos").resolve()
    if not p.is_dir():
        raise FileNotFoundError(
            f"loomground-repos checkout not found at {p}; set "
            "OVERSIGHT_LADDER_LOOMGROUND_REPOS to override")
    return p


def governance_standard_dir() -> Path:
    return loomground_repos_dir() / "loomground-governance" / "standard"


def escalation_src_dir() -> Path:
    return loomground_repos_dir() / "loomground-escalation" / "src"


def ref_impl_dir() -> Path:
    """loomground-ref: the second conformance implementation, current against
    grades.json's L0-L6 ladder. Used here as the validation engine (see
    validator.py for why the plugin-cached skill copy is not used directly)."""
    return loomground_repos_dir() / "loomground-ref"
