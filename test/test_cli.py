# (C) Copyright IBM 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests of the commandline interface."""

import tomlkit

from extremal_python_dependencies.main import app
from typer.testing import CliRunner

_runner = CliRunner()


class TestPinDependenciesToMinimum:
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
    def test_prints_minversion(self, project_dir):
        (project_dir / "tox.ini").write_text(
            "[tox]\nminversion = 3.25\n", encoding="utf-8"
        )
        result = _runner.invoke(app, ["get-tox-minversion"])
        assert result.exit_code == 0
        assert result.stdout.strip() == "3.25"
