# (C) Copyright IBM 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Shared fixtures for the extremal-python-dependencies test suite."""

import pytest  # pylint: disable=import-error
from typer.testing import CliRunner


SAMPLE_PYPROJECT = """\
[build-system]
requires = ["hatchling>=1.0", "hatch-vcs~=0.3"]
build-backend = "hatchling.build"

[project]
name = "demo"
version = "0.1.0"
dependencies = ["foo>=1.2", "bar~=2.0"]

[project.optional-dependencies]
test = ["pytest>=7.0"]

[dependency-groups]
dev = ["ruff>=0.1", {include-group = "test"}]
"""


@pytest.fixture
def runner():
    """Return a Typer CliRunner."""
    return CliRunner()


@pytest.fixture
def sample_pyproject():
    """Return the text of the shared sample pyproject.toml."""
    return SAMPLE_PYPROJECT


@pytest.fixture
def project_dir(tmp_path, monkeypatch, sample_pyproject):  # pylint: disable=redefined-outer-name
    """Write sample_pyproject to tmp_path and chdir there."""
    (tmp_path / "pyproject.toml").write_text(sample_pyproject, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return tmp_path
