#!/usr/bin/env python

"""
Test basic functionality of npm2rez package
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

from npm2rez.core import create_package_py, install_node_package


class TestNpm2Rez(unittest.TestCase):
    """Test basic functionality of npm2rez package"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.args = mock.MagicMock()
        self.args.name = "test-package"
        self.args.version = "1.0.0"
        self.args.node_version = "16"
        self.args.bin_name = "test-bin"
        self.args.source = "npm"
        self.args.repo = "test/repo"

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_create_package_py(self):
        """Test creating package.py file"""
        create_package_py(self.args, self.temp_dir)
        package_py_path = os.path.join(self.temp_dir, "package.py")
        self.assertTrue(os.path.exists(package_py_path))

        # Check file content
        with open(package_py_path, encoding="utf-8") as f:
            content = f.read()
            self.assertIn('name = "test_package"', content)
            self.assertIn('version = "1.0.0"', content)
            self.assertIn('nodejs-16+', content)
            self.assertIn('env.PATH.append', content)


class TestRealPackages(unittest.TestCase):
    """Test downloading and installing real packages"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        # Check if npm is available
        try:
            subprocess.check_call(
                [shutil.which("npm"), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.npm_available = True
        except (subprocess.SubprocessError, FileNotFoundError):
            self.npm_available = False

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @unittest.skipIf(
        not os.environ.get("RUN_REAL_PACKAGE_TESTS"),
        "Skipping real package tests. Set RUN_REAL_PACKAGE_TESTS=1 to run"
    )
    def test_install_typescript(self):
        """Test installing TypeScript package"""
        if not self.npm_available:
            self.skipTest("npm not available, skipping test")

        args = mock.MagicMock()
        args.name = "typescript"
        args.version = "4.9.5"
        args.node_version = "16"
        args.bin_name = "tsc"
        args.source = "npm"
        args.install = True

        # Create installation directory
        install_path = os.path.join(self.temp_dir, "typescript")
        os.makedirs(install_path, exist_ok=True)

        # Install package
        install_node_package(args, install_path)

        # Check if package was installed successfully
        bin_path = os.path.join(install_path, "bin", "tsc")
        if os.name == "nt":  # Windows
            bin_path += ".cmd"

        self.assertTrue(os.path.exists(bin_path), f"{bin_path} does not exist")

        # Check package content
        node_modules_path = os.path.join(install_path, "node_modules", "typescript")
        self.assertTrue(os.path.exists(node_modules_path), f"{node_modules_path} does not exist")

        # Check version information
        package_json_path = os.path.join(node_modules_path, "package.json")
        self.assertTrue(os.path.exists(package_json_path), f"{package_json_path} does not exist")

        # Check version number
        with open(package_json_path, encoding="utf-8") as f:
            package_json = json.load(f)
            self.assertEqual(package_json.get("version"), "4.9.5")

    @unittest.skipIf(
        not os.environ.get("RUN_REAL_PACKAGE_TESTS"),
        "Skipping real package tests. Set RUN_REAL_PACKAGE_TESTS=1 to run"
    )
    def test_install_eslint(self):
        """Test installing ESLint package"""
        if not self.npm_available:
            self.skipTest("npm not available, skipping test")

        args = mock.MagicMock()
        args.name = "eslint"
        args.version = "8.40.0"
        args.node_version = "16"
        args.bin_name = "eslint"
        args.source = "npm"
        args.install = True

        # Create installation directory
        install_path = os.path.join(self.temp_dir, "eslint")
        os.makedirs(install_path, exist_ok=True)

        # Install package
        install_node_package(args, install_path)

        # Check if package was installed successfully
        bin_path = os.path.join(install_path, "bin", "eslint")
        if os.name == "nt":  # Windows
            bin_path += ".cmd"

        self.assertTrue(os.path.exists(bin_path), f"{bin_path} does not exist")

        # Check package content
        node_modules_path = os.path.join(install_path, "node_modules", "eslint")
        self.assertTrue(os.path.exists(node_modules_path), f"{node_modules_path} does not exist")


class TestCliArguments(unittest.TestCase):
    """Test command line argument parsing"""

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_npm(self, mock_parse_args):
        """Test parsing npm source arguments"""
        from npm2rez.cli import parse_args

        # Mock command line arguments
        mock_args = mock.MagicMock()
        mock_args.name = "typescript"
        mock_args.version = "4.9.5"
        mock_args.source = "npm"
        mock_args.repo = None
        mock_args.output = "./rez-packages"
        mock_args.node_version = "16"
        mock_args.bin_name = "tsc"
        mock_args.install = False
        mock_parse_args.return_value = mock_args

        args = parse_args()
        self.assertEqual(args.name, "typescript")
        self.assertEqual(args.version, "4.9.5")
        self.assertEqual(args.source, "npm")
        self.assertEqual(args.output, "./rez-packages")

    @mock.patch('argparse.ArgumentParser.parse_args')
    @mock.patch('argparse.ArgumentParser.error')
    def test_parse_args_github_without_repo(self, mock_error, mock_parse_args):
        """Test parsing GitHub source arguments without providing a repository"""
        from npm2rez.cli import parse_args

        # Mock command line arguments
        mock_args = mock.MagicMock()
        mock_args.name = "typescript"
        mock_args.version = "4.9.5"
        mock_args.source = "github"
        mock_args.repo = None
        mock_parse_args.return_value = mock_args

        parse_args()
        # Verify that error method was called
        mock_error.assert_called_once_with("GitHub repository is required when using source=github")


if __name__ == "__main__":
    unittest.main()
