#!/usr/bin/env python3
"""
Run the project's test suite using Poetry, a virtualenv, or the system Python.
Usage: ./scripts/run_tests.py
"""
import os
import shutil
import subprocess
import sys


def run(cmd):
    print("Running:", " ".join(cmd))
    rc = subprocess.call(cmd)
    return rc


def main():
    print("🧪 Running tests...")

    poetry = shutil.which("poetry")
    if poetry:
        print("Using Poetry to run tests")
        rc = run([poetry, "run", "pytest", "tests/", "-v"])
        sys.exit(rc)

    # prefer venv python if present
    venv_py = None
    for candidate in ("venv/bin/python3", "venv/bin/python"):
        if os.path.exists(candidate):
            venv_py = candidate
            break

    if venv_py:
        print("Using venv python:", venv_py)
        rc = run([venv_py, "-m", "pytest", "tests/", "-v"])
        sys.exit(rc)

    # try current interpreter (if pytest is installed)
    try:
        import pytest  # noqa: F401
        print("Using current Python interpreter to run pytest")
        rc = run([sys.executable, "-m", "pytest", "tests/", "-v"])
        sys.exit(rc)
    except Exception:
        pytest_bin = shutil.which("pytest")
        if pytest_bin:
            print("Using system pytest:", pytest_bin)
            rc = run([pytest_bin, "tests/", "-v"])
            sys.exit(rc)

    print("No test runner found. Install Poetry or pytest (pip install pytest).")
    sys.exit(1)


if __name__ == "__main__":
    main()
