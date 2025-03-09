#!/usr/bin/env python

"""
Test core API functions for npm2rez package
"""

import os
from types import SimpleNamespace
from unittest import mock

import pytest

# No need to manually register pyfakefs plugin, it will be registered automatically
from npm2rez.core import (
    convert_name_to_rez_format,
    create_package_py,
    extract_node_package,
    get_npm_executable,
    install_from_github,
    install_from_npm,
    install_node_package,
)


@pytest.fixture
def mock_args():
    """Create mock arguments for testing"""
    return SimpleNamespace(
        name="typescript",
        version="4.9.5",
        output="./rez-packages",
        source="npm",
        repo=None,
        node_version="16",
        _is_test=True  # Use test mode to avoid actual npm calls
    )


def test_get_npm_executable():
    """Test get_npm_executable function"""
    with mock.patch('shutil.which') as mock_which:
        with mock.patch('subprocess.check_call') as mock_check_call:
            # Setup mocks
            mock_which.return_value = '/usr/bin/npm'
            mock_check_call.return_value = 0

            # Call function
            npm = get_npm_executable()

            # Verify result
            assert npm == '/usr/bin/npm'
            mock_which.assert_called_once_with('npm')
            mock_check_call.assert_called_once()


def test_get_npm_executable_not_found():
    """Test get_npm_executable when npm is not found"""
    with mock.patch('shutil.which') as mock_which:
        # Setup mock
        mock_which.return_value = None

        # Call function
        npm = get_npm_executable()

        # Verify result
        assert npm is None
        mock_which.assert_called_once_with('npm')


def test_create_package_py(fs, mock_args):
    """Test create_package_py function using pyfakefs"""
    # Create test directory
    test_dir = "/mock/path"
    fs.create_dir(test_dir)

    # Mock print function
    with mock.patch('builtins.print'):
        # Call function
        create_package_py(mock_args, test_dir)

        # Verify package.py file was created
        package_py_path = os.path.join(test_dir, "package.py")
        assert os.path.exists(package_py_path)

        # Verify package.py content
        with open(package_py_path) as f:
            content = f.read()
            assert 'name = "typescript"' in content
            assert f'version = "{mock_args.version}"' in content
            assert 'env.PATH.append("{root}/bin")' in content
            assert 'env.NODE_PATH = "{root}/node_modules"' in content


def test_install_from_npm(fs, mock_args):
    """Test install_from_npm function with test mode"""
    # Create test directory
    install_path = "/mock/path"
    fs.create_dir(install_path)

    # Mock npm executable
    npm_path = "/usr/bin/npm"

    # Mock print function
    with mock.patch('builtins.print'):
        # Call function (test mode)
        result = install_from_npm(npm_path, mock_args, install_path, is_test=True)

        # Verify result
        assert result is True

        # Verify bin directory was created
        bin_dir = os.path.join(install_path, "bin")
        assert os.path.exists(bin_dir)


def test_install_from_npm_real(fs):
    """Test install_from_npm function with real npm call"""
    # Create test arguments
    args = SimpleNamespace(
        name="typescript",
        version="4.9.5",
        _is_test=False
    )

    # Create test directories
    install_path = "/mock/path"
    temp_dir = "/mock/temp_npm"
    fs.create_dir(install_path)
    fs.create_dir(temp_dir)
    fs.create_dir(os.path.join(temp_dir, "node_modules", args.name))

    # Mock subprocess.check_call
    with mock.patch('subprocess.check_call') as mock_check_call:
        # Mock print function
        with mock.patch('builtins.print'):
            # Call function
            result = install_from_npm("/usr/bin/npm", args, install_path, is_test=False)

            # Verify result
            assert result is True
            mock_check_call.assert_called()

            # Verify node_modules directory was created
            node_modules_dir = os.path.join(install_path, "node_modules")
            assert os.path.exists(node_modules_dir)


def test_install_from_github(fs):
    """Test install_from_github function"""
    # Create test arguments
    args = SimpleNamespace(
        name="typescript",
        version="main",
        repo="microsoft/typescript",
        _is_test=True
    )

    # Create test directories
    install_path = "/mock/path"
    temp_dir = "/mock/temp_repo"
    fs.create_dir(install_path)
    fs.create_dir(temp_dir)

    # Mock subprocess.check_call
    with mock.patch('subprocess.check_call') as mock_check_call:
        # Mock print function
        with mock.patch('builtins.print'):
            # Call function
            result = install_from_github("/usr/bin/npm", args, install_path)

            # Verify result
            assert result is True
            mock_check_call.assert_called()


def test_install_node_package_npm_success(mock_args):
    """Test install_node_package with npm source"""
    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_npm') as mock_install_npm:
            # Setup mock
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_npm.return_value = True

            # Call function
            result = install_node_package(mock_args, "/mock/path")

            # Verify result
            assert result is True
            mock_get_npm.assert_called_once()
            mock_install_npm.assert_called_once_with(
                '/usr/bin/npm', mock_args, "/mock/path", mock_args._is_test
            )


def test_install_node_package_npm_failure(mock_args):
    """Test install_node_package with npm source when npm fails"""
    # Create a test_args object with _is_test=False
    test_args = SimpleNamespace(
        name="typescript",
        version="4.9.5",
        output="./rez-packages",
        source="npm",
        repo=None,
        node_version="16",
        _is_test=False
    )

    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_npm') as mock_install_npm:
            # Setup mock to simulate failure
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_npm.return_value = False

            # Call function
            result = install_node_package(test_args, "/mock/path")

            # Verify result
            assert result is False
            mock_get_npm.assert_called_once()
            mock_install_npm.assert_called_once()


def test_install_node_package_github():
    """Test install_node_package with github source"""
    # Create GitHub source arguments
    github_args = SimpleNamespace(
        name="typescript",
        version="main",
        output="./rez-packages",
        source="github",
        repo="microsoft/typescript",
        node_version="16",
        _is_test=True  # Use test mode to avoid actual npm calls
    )

    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_github') as mock_install_github:
            # Setup mock
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_github.return_value = True

            # Call function
            result = install_node_package(github_args, "/mock/path")

            # Verify result
            assert result is True
            mock_get_npm.assert_called_once()
            mock_install_github.assert_called_once_with('/usr/bin/npm', github_args, "/mock/path")


def test_extract_node_package(mock_args, fs):
    """Test extract_node_package function"""
    # Create test directory
    test_dir = "/mock/path"
    fs.create_dir(test_dir)

    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_npm') as mock_install_npm:
            # Setup mock
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_npm.return_value = True

            # Call function
            result = extract_node_package(mock_args, test_dir)

            # Verify result
            assert result is True
            mock_get_npm.assert_called_once()
            mock_install_npm.assert_called_once_with(
                '/usr/bin/npm', mock_args, test_dir, mock_args._is_test)


def test_convert_name_to_rez_format():
    """Test convert_name_to_rez_format function"""
    # Test with simple name
    assert convert_name_to_rez_format("typescript") == "typescript"

    # Test with hyphenated name
    assert convert_name_to_rez_format("ts-node") == "ts_node"

    # Test with scoped package name
    assert convert_name_to_rez_format("@types/node") == "types_node"
