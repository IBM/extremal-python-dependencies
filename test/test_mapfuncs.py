# (C) Copyright IBM 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Unit tests for the pure mapping functions."""

import pytest

from extremal_python_dependencies.main import (
    inplace_map,
    mapfunc_minimum,
    mapfunc_replace,
)


class TestMapfuncMinimum:
    """Tests for mapfunc_minimum."""

    def test_ge_becomes_eq(self):
        assert mapfunc_minimum("foo>=1.2.3") == "foo==1.2.3"

    def test_compatible_release_becomes_eq(self):
        assert mapfunc_minimum("bar~=2.0") == "bar==2.0"

    def test_already_pinned_unchanged(self):
        assert mapfunc_minimum("baz==3.0") == "baz==3.0"

    def test_multiple_clauses(self):
        # Only >= and ~= are rewritten; != is left alone
        assert mapfunc_minimum("foo>=1.0,!=1.5") == "foo==1.0,!=1.5"

    def test_include_group_passthrough(self):
        dep = {"include-group": "test"}
        assert mapfunc_minimum(dep) is dep

    def test_asterisk_with_eq_raises(self):
        with pytest.raises(ValueError, match="Asterisks"):
            mapfunc_minimum("foo==1.*")


class TestMapfuncReplace:
    """Tests for mapfunc_replace."""

    def test_single_replacement(self):
        f = mapfunc_replace(["foo@ git+https://example.com/foo.git"])
        assert f("foo>=1.0") == "foo@ git+https://example.com/foo.git"

    def test_non_matching_dep_unchanged(self):
        f = mapfunc_replace(["foo@ git+https://example.com/foo.git"])
        assert f("bar>=2.0") == "bar>=2.0"

    def test_multiple_replacements(self):
        f = mapfunc_replace(["foo==1.0", "bar==2.0"])
        assert f("foo>=0.1") == "foo==1.0"
        assert f("bar~=1.5") == "bar==2.0"

    def test_include_group_passthrough(self):
        f = mapfunc_replace(["foo==1.0"])
        dep = {"include-group": "test"}
        assert f(dep) is dep

    def test_duplicate_name_raises(self):
        with pytest.raises(RuntimeError, match="Duplicate"):
            mapfunc_replace(["foo==1.0", "foo==2.0"])

    def test_bad_replacement_name_raises(self):
        with pytest.raises(RuntimeError, match="PEP 508"):
            mapfunc_replace(["@@@"])

    def test_dep_with_bad_name_raises(self):
        f = mapfunc_replace(["foo==1.0"])
        with pytest.raises(RuntimeError, match="PEP 508"):
            f("@@@")


class TestInplaceMap:
    """Tests for inplace_map."""

    def test_mutates_list(self):
        lst = ["a", "b", "c"]
        inplace_map(str.upper, lst)
        assert lst == ["A", "B", "C"]

    def test_empty_list(self):
        lst = []
        inplace_map(str.upper, lst)
        assert not lst
