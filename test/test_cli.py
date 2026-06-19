# (C) Copyright IBM 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests of the commandline interface."""

import tomlkit
from typer.testing import CliRunner

from extremal_python_dependencies.main import app

_runner = CliRunner()


class TestPinDependenciesToMinimum:
    """Tests for the pin-dependencies-to-minimum command."""

    # pylint: disable=unused-argument  # project_dir used for chdir side effect

    def test_stdout_contains_pinned_versions(self, project_dir):
        result = _runner.invoke(app, ["pin-dependencies-to-minimum"])
        assert result.exit_code == 0
        assert "foo==1.2" in result.stdout
        assert "bar==2.0" in result.stdout

    def test_stdout_contains_allow_direct_references(self, project_dir):
        result = _runner.invoke(app, ["pin-dependencies-to-minimum"])
        assert "allow-direct-references" in result.stdout

    def test_inplace_writes_file(self, project_dir):
        result = _runner.invoke(app, ["pin-dependencies-to-minimum", "--inplace"])
        assert result.exit_code == 0
        assert result.stdout == ""
        with open(project_dir / "pyproject.toml", encoding="utf-8") as f:
            d = tomlkit.load(f)
        assert "foo==1.2" in d["project"]["dependencies"]
        assert "bar==2.0" in d["project"]["dependencies"]

    def test_optional_deps_pinned(self, project_dir):
        result = _runner.invoke(app, ["pin-dependencies-to-minimum"])
        assert "pytest==7.0" in result.stdout

    def test_build_system_pinned(self, project_dir):
        result = _runner.invoke(app, ["pin-dependencies-to-minimum"])
        assert "hatchling==1.0" in result.stdout

    def test_dependency_group_pinned(self, project_dir):
        result = _runner.invoke(app, ["pin-dependencies-to-minimum"])
        assert "ruff==0.1" in result.stdout

    def test_include_group_preserved(self, project_dir):
        result = _runner.invoke(app, ["pin-dependencies-to-minimum"])
        assert 'include-group = "test"' in result.stdout


class TestPinDependencies:
    """Tests for the pin-dependencies command."""

    # pylint: disable=unused-argument  # project_dir used for chdir side effect

    def test_named_dep_replaced(self, project_dir):
        result = _runner.invoke(
            app,
            ["pin-dependencies", "foo@ git+https://example.com/foo.git"],
        )
        assert result.exit_code == 0
        assert "foo@ git+https://example.com/foo.git" in result.stdout

    def test_unspecified_dep_unchanged(self, project_dir):
        result = _runner.invoke(
            app,
            ["pin-dependencies", "foo@ git+https://example.com/foo.git"],
        )
        assert "bar~=2.0" in result.stdout

    def test_allow_direct_references_added(self, project_dir):
        result = _runner.invoke(
            app,
            ["pin-dependencies", "foo@ git+https://example.com/foo.git"],
        )
        assert "allow-direct-references" in result.stdout

    def test_inplace_writes_file(self, project_dir):
        result = _runner.invoke(
            app,
            [
                "pin-dependencies",
                "foo@ git+https://example.com/foo.git",
                "--inplace",
            ],
        )
        assert result.exit_code == 0
        assert result.stdout == ""
        with open(project_dir / "pyproject.toml", encoding="utf-8") as f:
            d = tomlkit.load(f)
        assert "foo@ git+https://example.com/foo.git" in d["project"]["dependencies"]


class TestAddDependency:
    """Tests for the add-dependency command."""

    # pylint: disable=unused-argument  # project_dir used for chdir side effect

    def test_appends_to_stdout(self, project_dir):
        result = _runner.invoke(app, ["add-dependency", "newpkg==1.0"])
        assert result.exit_code == 0
        assert "newpkg==1.0" in result.stdout

    def test_inplace_writes_file(self, project_dir):
        result = _runner.invoke(app, ["add-dependency", "newpkg==1.0", "--inplace"])
        assert result.exit_code == 0
        with open(project_dir / "pyproject.toml", encoding="utf-8") as f:
            d = tomlkit.load(f)
        assert "newpkg==1.0" in d["project"]["dependencies"]


class TestGetToxMinversion:
    """Tests for the get-tox-minversion command."""

    # pylint: disable=unused-argument  # project_dir used for chdir side effect

    def test_prints_minversion(self, project_dir):
        (project_dir / "tox.ini").write_text(
            "[tox]\nminversion = 3.25\n", encoding="utf-8"
        )
        result = _runner.invoke(app, ["get-tox-minversion"])
        assert result.exit_code == 0
        assert result.stdout.strip() == "3.25"

    def test_prints_min_version(self, project_dir):
        (project_dir / "tox.ini").write_text(
            "[tox]\nmin_version = 4.0\n", encoding="utf-8"
        )
        result = _runner.invoke(app, ["get-tox-minversion"])
        assert result.exit_code == 0
        assert result.stdout.strip() == "4.0"

    def test_entrypoint(self, project_dir):
        """Smoke test: the installed entry point responds to --help."""
        result = _runner.invoke(app, ["--help"])
        assert result.exit_code == 0
