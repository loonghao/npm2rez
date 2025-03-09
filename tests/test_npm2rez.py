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

from npm2rez.cli import main, parse_args
from npm2rez.core import create_package, create_package_py, install_node_package


class TestNpm2Rez(unittest.TestCase):
    """Test basic functionality of npm2rez package"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.args = mock.MagicMock()
        self.args.name = "test-package"
        self.args.version = "1.0.0"
        self.args.node_version = "16"
        self.args.source = "npm"
        self.args.repo = "test/repo"
        self.args.output = self.temp_dir

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
            self.assertIn('env.PATH.append("{root}/bin")', content)

    def test_create_package_py_without_bin(self):
        """Test creating package.py file without bin_name"""
        args = mock.MagicMock()
        args.name = "test-package"
        args.version = "1.0.0"
        args.node_version = "16"
        args.source = "npm"

        create_package_py(args, self.temp_dir)
        package_py_path = os.path.join(self.temp_dir, "package.py")
        self.assertTrue(os.path.exists(package_py_path))

        # Check file content
        with open(package_py_path, encoding="utf-8") as f:
            content = f.read()
            self.assertIn('name = "test_package"', content)
            self.assertIn('version = "1.0.0"', content)
            self.assertIn('nodejs-16+', content)
            self.assertIn('env.PATH.append("{root}/bin")', content)
            self.assertIn('NODE_PATH', content)

    def test_create_package_with_scoped_name(self):
        """Test creating package with scoped name (@org/package)"""
        args = mock.MagicMock()
        args.name = "@test/package"
        args.version = "1.0.0"
        args.node_version = "16"
        args.source = "npm"

        create_package_py(args, self.temp_dir)
        package_py_path = os.path.join(self.temp_dir, "package.py")
        self.assertTrue(os.path.exists(package_py_path))

        # Check file content
        with open(package_py_path, encoding="utf-8") as f:
            content = f.read()
            # @ 和 / 被替换为下划线
            self.assertIn('name = "test_package"', content)
            # 原始包名会出现在描述中
            self.assertIn('description = "Rez package for @test/package Node.js package"', content)

    @mock.patch('npm2rez.core.create_package_py')
    @mock.patch('npm2rez.core.install_node_package')
    def test_create_package(self, mock_install, mock_create_py):
        """Test create_package function"""
        package_dir = create_package(self.args)

        # Verify the expected directory was created
        expected_dir = os.path.join(os.path.abspath(self.temp_dir), "test_package", "1.0.0")
        self.assertEqual(package_dir, expected_dir)
        self.assertTrue(os.path.exists(expected_dir))

        # Verify the functions were called with correct arguments
        mock_create_py.assert_called_once()
        mock_install.assert_called_once()


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

    @mock.patch('subprocess.check_call')
    @mock.patch('shutil.which')
    def test_install_node_package_npm_not_available(self, mock_which, mock_check_call):
        """Test install_node_package when npm is not available"""
        mock_which.return_value = "npm"
        mock_check_call.side_effect = subprocess.SubprocessError("npm not found")

        args = mock.MagicMock()
        args.name = "test-package"
        args.version = "1.0.0"
        args.source = "npm"

        install_path = os.path.join(self.temp_dir, "test-package")
        install_node_package(args, install_path)

        # Verify node_modules directory was created even though npm failed
        node_modules_path = os.path.join(install_path, "node_modules")
        self.assertTrue(os.path.exists(node_modules_path))

        # Verify subprocess.check_call was called with npm --version
        mock_check_call.assert_called_once()

    @mock.patch('subprocess.check_call')
    @mock.patch('shutil.which')
    @mock.patch('os.symlink')
    def test_install_node_package_from_npm(self, mock_symlink, mock_which, mock_check_call):
        """Test install_node_package from npm source"""
        mock_which.return_value = "npm"

        # Create mock bin directory structure
        bin_dir = os.path.join(self.temp_dir, "node_modules", ".bin")
        os.makedirs(bin_dir, exist_ok=True)
        with open(os.path.join(bin_dir, "test-bin"), "w") as f:
            f.write("#!/bin/bash\necho test")

        args = mock.MagicMock()
        args.name = "test-package"
        args.version = "1.0.0"
        args.source = "npm"
        args._is_test = True  # Mark this as a test run

        # Create node_modules directory for the package
        package_dir = os.path.join(self.temp_dir, "node_modules", "test-package")
        os.makedirs(package_dir, exist_ok=True)

        # Create bin directory in package
        package_bin_dir = os.path.join(package_dir, "bin")
        os.makedirs(package_bin_dir, exist_ok=True)
        with open(os.path.join(package_bin_dir, "test-bin"), "w") as f:
            f.write("#!/bin/bash\necho test")

        install_node_package(args, self.temp_dir)

        # Verify bin directory was created
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "bin")))


class TestCliArguments(unittest.TestCase):
    """Test command line argument parsing"""

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_npm(self, mock_parse_args):
        """Test parsing npm source arguments"""
        # Mock command line arguments
        mock_args = mock.MagicMock()
        mock_args.name = "typescript"
        mock_args.version = "4.9.5"
        mock_args.source = "npm"
        mock_args.repo = None
        mock_args.output = "./rez-packages"
        mock_args.node_version = "16"
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

    @mock.patch('npm2rez.cli.parse_args')
    @mock.patch('npm2rez.cli.create_package')
    def test_main(self, mock_create_package, mock_parse_args):
        """Test main function"""
        # Setup mock arguments
        mock_args = mock.MagicMock()
        mock_args.name = "test-package"
        mock_args.version = "1.0.0"
        mock_args.output = "./rez-packages"
        mock_parse_args.return_value = mock_args

        # Setup mock return value for create_package
        mock_create_package.return_value = "/path/to/package"

        # Call main function
        main()

        # Verify create_package was called with the correct arguments
        mock_create_package.assert_called_once_with(mock_args)


if __name__ == "__main__":
    unittest.main()
