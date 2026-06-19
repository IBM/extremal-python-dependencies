# (C) Copyright IBM 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for process_dependencies_in_place."""

import tomlkit
import pytest

from extremal_python_dependencies.main import mapfunc_minimum, process_dependencies_in_place


def _parse(toml_text):
    return tomlkit.loads(toml_text)


class TestProcessDependenciesInPlace:
    def test_project_dependencies(self):
        d = _parse(
            "[project]\ndependencies = ['foo>=1.0', 'bar~=2.0']\n"
        )
        process_dependencies_in_place(d, mapfunc_minimum)
        assert list(d["project"]["dependencies"]) == ["foo==1.0", "bar==2.0"]

    def test_optional_dependencies(self):
        d = _parse(
            "[project]\ndependencies = []\n"
            "[project.optional-dependencies]\ntest = ['pytest>=7.0']\n"
        )
        process_dependencies_in_place(d, mapfunc_minimum)
        assert list(d["project"]["optional-dependencies"]["test"]) == ["pytest==7.0"]

    def test_dependency_groups(self):
        d = _parse(
            "[project]\ndependencies = []\n"
            '[dependency-groups]\ndev = ["ruff>=0.1"]\n'
        )
        process_dependencies_in_place(d, mapfunc_minimum)
        assert list(d["dependency-groups"]["dev"]) == ["ruff==0.1"]

    def test_build_system_requires(self):
        d = _parse(
            "[project]\ndependencies = []\n"
            '[build-system]\nrequires = ["hatchling>=1.0"]\nbuild-backend = "hatchling.build"\n'
        )
        process_dependencies_in_place(d, mapfunc_minimum)
        assert list(d["build-system"]["requires"]) == ["hatchling==1.0"]

    def test_include_group_in_dependency_groups(self):
        d = _parse(
            "[project]\ndependencies = []\n"
            '[dependency-groups]\ndev = ["ruff>=0.1", {include-group = "test"}]\n'
        )
        process_dependencies_in_place(d, mapfunc_minimum)
        devdeps = list(d["dependency-groups"]["dev"])
        assert devdeps[0] == "ruff==0.1"
        assert devdeps[1] == {"include-group": "test"}

    def test_no_dependencies_key(self):
        d = _parse("[project]\nname = 'x'\n")
        process_dependencies_in_place(d, mapfunc_minimum)  # must not raise

    def test_no_optional_dependencies(self):
        d = _parse("[project]\ndependencies = []\n")
        process_dependencies_in_place(d, mapfunc_minimum)  # must not raise

    def test_no_dependency_groups(self):
        d = _parse("[project]\ndependencies = []\n")
        process_dependencies_in_place(d, mapfunc_minimum)  # must not raise

    def test_no_build_system(self):
        d = _parse("[project]\ndependencies = []\n")
        process_dependencies_in_place(d, mapfunc_minimum)  # must not raise

    def test_build_system_without_requires(self):
        d = _parse(
            "[project]\ndependencies = []\n"
            '[build-system]\nbuild-backend = "hatchling.build"\n'
        )
        process_dependencies_in_place(d, mapfunc_minimum)  # must not raise
