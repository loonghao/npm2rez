# Import built-in modules
import os
import sys

# Import third-party modules
import nox

ROOT = os.path.dirname(__file__)

# Ensure npm2rez is importable.
if ROOT not in sys.path:
    sys.path.append(ROOT)

# Import local modules
from nox_actions import codetest, lint, release  # noqa: E402

nox.session(lint.lint, name="lint")
nox.session(lint.lint_fix, name="lint-fix")
nox.session(codetest.pytest, name="pytest")
nox.session(codetest.pytest_real_packages, name="pytest-real-packages")
nox.session(release.build_exe, name="build-exe")
