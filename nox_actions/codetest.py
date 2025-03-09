# Import built-in modules
import os

# Import third-party modules
import nox

from nox_actions.utils import PACKAGE_NAME, THIS_ROOT


def pytest(session: nox.Session) -> None:
    """Run basic unit tests without real package installation."""
    session.install(".")
    session.install("pytest", "pytest-cov", "pytest-mock")
    test_root = os.path.join(THIS_ROOT, "tests")
    session.run(
        "pytest",
        f"--cov={PACKAGE_NAME}",
        "--cov-report=xml:coverage.xml",
        f"--rootdir={test_root}",
        "-k", "not test_install_",
        env={"PYTHONPATH": THIS_ROOT.as_posix()}
    )


def pytest_real_packages(session: nox.Session) -> None:
    """Run tests that involve real npm package installation."""
    session.install(".")
    session.install("pytest")
    test_root = os.path.join(THIS_ROOT, "tests")
    session.run(
        "pytest",
        f"--rootdir={test_root}",
        "-k", "test_install_",
        "-v",
        env={
            "PYTHONPATH": THIS_ROOT.as_posix(),
            "RUN_REAL_PACKAGE_TESTS": "1"
        }
    )
