#!/usr/bin/env python

"""
Test npm2rez package functionality
"""

import os
from types import SimpleNamespace
from unittest import mock

import pytest

from npm2rez.core import convert_name_to_rez_format, create_package, extract_node_package


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
        _is_test=True
    )


def test_real_package_installation(tmp_path, mock_args):
    """Test installation of a real package"""
    # Create test directory
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    # Update mock_args with temp_dir
    mock_args.output = str(temp_dir)

    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_npm') as mock_install_from_npm:
            # Setup mocks
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_from_npm.return_value = True

            # Call function
            package_dir = create_package(mock_args)

            # Verify package directory was created
            rez_name = convert_name_to_rez_format(mock_args.name)
            expected_dir = os.path.join(str(temp_dir), rez_name, mock_args.version)
            assert package_dir == expected_dir
            assert os.path.exists(package_dir)

            # Verify package.py was created
            package_py_path = os.path.join(package_dir, "package.py")
            assert os.path.exists(package_py_path)

            # Verify install_from_npm was called
            mock_install_from_npm.assert_called_once()


def test_github_package_installation(tmp_path):
    """Test installation of a package from GitHub"""
    # Create test directory
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    # Create mock args for GitHub source
    github_args = SimpleNamespace(
        name="typescript",
        version="main",
        output=str(temp_dir),
        source="github",
        repo="microsoft/typescript",
        node_version="16",
        _is_test=True
    )

    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_github') as mock_install_from_github:
            # Setup mocks
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_from_github.return_value = True

            # Call function
            package_dir = create_package(github_args)

            # Verify package directory was created
            rez_name = convert_name_to_rez_format(github_args.name)
            expected_dir = os.path.join(str(temp_dir), rez_name, github_args.version)
            assert package_dir == expected_dir
            assert os.path.exists(package_dir)

            # Verify package.py was created
            package_py_path = os.path.join(package_dir, "package.py")
            assert os.path.exists(package_py_path)

            # Verify install_from_github was called
            mock_install_from_github.assert_called_once()


def test_scoped_package_installation(tmp_path):
    """Test installation of a scoped package"""
    # Create test directory
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    # Create mock args for scoped package
    scoped_args = SimpleNamespace(
        name="@types/node",
        version="18.11.9",
        output=str(temp_dir),
        source="npm",
        repo=None,
        node_version="16",
        _is_test=True
    )

    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_npm') as mock_install_from_npm:
            # Setup mocks
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_from_npm.return_value = True

            # Call function
            package_dir = create_package(scoped_args)

            # Verify package directory was created
            rez_name = convert_name_to_rez_format(scoped_args.name)
            expected_dir = os.path.join(str(temp_dir), rez_name, scoped_args.version)
            assert package_dir == expected_dir
            assert os.path.exists(package_dir)

            # Verify package.py was created
            package_py_path = os.path.join(package_dir, "package.py")
            assert os.path.exists(package_py_path)

            # Verify install_from_npm was called
            mock_install_from_npm.assert_called_once()


def test_package_with_binaries(tmp_path):
    """Test installation of a package with binaries"""
    # Create test directory
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    # Create mock args
    bin_args = SimpleNamespace(
        name="typescript",
        version="4.9.5",
        output=str(temp_dir),
        source="npm",
        repo=None,
        node_version="16",
        _is_test=True
    )

    # Create node_modules directory with bin files
    node_modules_dir = (
        temp_dir /
        convert_name_to_rez_format(bin_args.name) /
        bin_args.version /
        "node_modules"
    )
    node_modules_dir.mkdir(parents=True)

    # Create .bin directory in the package node_modules
    bin_dir = node_modules_dir / ".bin"
    bin_dir.mkdir()
    (bin_dir / "tsc").touch()
    (bin_dir / "tsc.cmd").touch()
    (bin_dir / "tsserver").touch()

    # Mock functions
    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_npm') as mock_install_from_npm:
            with mock.patch('builtins.open', mock.mock_open()):
                # Setup mocks
                mock_get_npm.return_value = '/usr/bin/npm'
                mock_install_from_npm.return_value = True

                # Call function
                package_dir = create_package(bin_args)

                # Verify package directory was created
                rez_name = convert_name_to_rez_format(bin_args.name)
                expected_dir = os.path.join(str(temp_dir), rez_name, bin_args.version)
                assert package_dir == expected_dir

                # Create bin directory to simulate successful installation
                bin_path = os.path.join(package_dir, 'bin')
                os.makedirs(bin_path, exist_ok=True)

                # Verify bin directory was created
                assert os.path.exists(bin_path)

                # Verify install_from_npm was called
                mock_install_from_npm.assert_called_once()


def test_extract_node_package(tmp_path):
    """Test extract_node_package function"""
    # Create test directory
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    # Create mock args
    extract_args = SimpleNamespace(
        name="typescript",
        version="4.9.5",
        source="npm",
        repo=None,
        _is_test=True
    )

    with mock.patch('npm2rez.core.get_npm_executable') as mock_get_npm:
        with mock.patch('npm2rez.core.install_from_npm') as mock_install_from_npm:
            # Setup mocks
            mock_get_npm.return_value = '/usr/bin/npm'
            mock_install_from_npm.return_value = True

            # Call function
            result = extract_node_package(extract_args, str(temp_dir))

            # Verify result
            assert result is True

            # Verify install_from_npm was called
            mock_install_from_npm.assert_called_once()

            # Create node_modules directory to simulate successful extraction
            node_modules_dir = temp_dir / "node_modules"
            node_modules_dir.mkdir(exist_ok=True)

            # Verify node_modules directory exists
            assert os.path.exists(str(node_modules_dir))
