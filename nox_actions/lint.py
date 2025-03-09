# Import third-party modules
import nox

from nox_actions.utils import PACKAGE_NAME


def lint(session: nox.Session) -> None:
    """Run linting checks without modifying files."""
    session.install("ruff", "pre-commit")
    # Run ruff checks (including import sorting)
    session.run("ruff", "check")
    # Run pre-commit checks
    session.run("pre-commit", "run", "--all-files")


def lint_fix(session: nox.Session) -> None:
    """Run linting checks and fix issues automatically."""
    session.install("isort", "ruff", "pre-commit", "autoflake")
    # Fix ruff issues
    session.run("ruff", "check", "--fix")
    # Fix import sorting
    session.run("isort", ".")
    # Run pre-commit hooks
    session.run("pre-commit", "run", "--all-files")
    # Remove unused imports and variables
    session.run(
        "autoflake",
        "--in-place",
        "--remove-all-unused-imports",
        "--remove-unused-variables",
        "-r",
        PACKAGE_NAME
    )
