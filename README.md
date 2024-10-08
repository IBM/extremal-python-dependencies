[![Release](https://img.shields.io/pypi/v/extremal-python-dependencies.svg?label=Release)](https://github.com/IBM/extremal-python-dependencies/releases)
[![Python](https://img.shields.io/pypi/pyversions/extremal-python-dependencies?label=Python&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/github/license/IBM/extremal-python-dependencies?label=License)](LICENSE.txt)
[![Downloads](https://img.shields.io/pypi/dm/extremal-python-dependencies.svg?label=Downloads)](https://pypi.org/project/extremal-python-dependencies/)
[![Tests](https://github.com/IBM/extremal-python-dependencies/actions/workflows/test_latest_versions.yml/badge.svg)](https://github.com/IBM/extremal-python-dependencies/actions/workflows/test_latest_versions.yml)
[![Coverage](https://coveralls.io/repos/github/IBM/extremal-python-dependencies/badge.svg?branch=main)](https://coveralls.io/github/IBM/extremal-python-dependencies?branch=main)

# extremal-python-dependencies

_A utility for installing extremal versions of dependencies for more robust testing._

Install extremal versions of package dependencies for more robust continuous integration testing, given a package that specifies its dependencies in a `pyproject.toml` file.

For instance, one might use this utility to install the minimum supported version of each dependency before a CI run.  Ensuring all tests then pass adds confidence that the code is indeed compatible with the full range of package versions it claims to be compatible with, helping to prevent users from encountering broken installs.

Another way to use this tool is to install development versions of certain packages.

This utility works with dependencies specified in a `pyproject.toml` file.  It modifies `pyproject.toml`, either by sending the transformed version to stdout (the default) or by modifying in place (which may be useful in CI scripts).

## How to use

The following snippet modifies `pyproject.toml` in place to test with the minimum supported version of each direct dependency, under the minimum supported [tox](https://tox.wiki/) version (as specified by `minversion` in `tox.ini`).

```sh
pip install "tox==$(extremal-python-dependencies get-tox-minversion)"
extremal-python-dependencies pin-dependencies-to-minimum --inplace
tox -epy
```

The following snippet modifies `pyproject.toml` in place to test with the development version of one or more dependencies:

```sh
extremal-python-dependencies pin-dependencies \
    "qiskit @ git+https://github.com/Qiskit/qiskit.git" \
    "qiskit-ibm-runtime @ git+https://github.com/Qiskit/qiskit-ibm-runtime.git" \
    --inplace
tox -epy
```

Each of the above patterns can be used in a CI script.

## Caveats

- The minimum versions of all optional dependencies installed simultaneously must be compatible with each other.
- This tool does not set the minimum supported version of transitive dependencies.

## Similar tools

- [requirements-builder](https://requirements-builder.readthedocs.io/) (builds requirements from a `setup.py` file instead of a `pyproject.toml` file)
