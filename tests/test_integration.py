#!/usr/bin/env python

"""
Integration tests for npm2rez package
"""

import os
import shutil
import tempfile
from unittest import mock

import pytest
from click.testing import CliRunner

from npm2rez.cli import cli


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up after test
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def runner():
    """Create CLI runner for testing"""
    return CliRunner()


def test_create_command_integration(runner, temp_dir):
    """Integration test for create command"""
    with mock.patch('npm2rez.cli.create_package') as mock_create:
        with mock.patch('os.path.exists') as mock_exists:
            # Setup mocks
            mock_create.return_value = os.path.join(temp_dir, 'typescript', '4.9.5')
            mock_exists.return_value = True

            # Call command
            result = runner.invoke(cli, [
                'create',
                '--name', 'typescript',
                '--version', '4.9.5',
                '--output', temp_dir,
                '--source', 'npm',
                '--node-version', '16'
            ])

            # Verify result
            assert result.exit_code == 0
            assert 'Created package at' in result.output

            # Verify create_package was called with correct arguments
            mock_create.assert_called_once()
            args = mock_create.call_args[0][0]
            assert args.name == 'typescript'
            assert args.version == '4.9.5'
            assert args.output == temp_dir
            assert args.source == 'npm'
            assert args.node_version == '16'


def test_extract_command_integration(runner, temp_dir):
    """Integration test for extract command"""
    with mock.patch('npm2rez.cli.extract_node_package') as mock_extract:
        # Setup mocks
        mock_extract.return_value = True

        # Call command
        result = runner.invoke(cli, [
            'extract',
            '--name', 'typescript',
            '--version', '4.9.5',
            '--output', temp_dir,
            '--source', 'npm'
        ])

        # Verify result
        assert result.exit_code == 0
        assert 'Successfully extracted' in result.output

        # Verify extract_node_package was called with correct arguments
        mock_extract.assert_called_once()
        args = mock_extract.call_args[0][0]
        output_dir = mock_extract.call_args[0][1]
        assert args.name == 'typescript'
        assert args.version == '4.9.5'
        assert args.source == 'npm'
        assert output_dir == temp_dir


def test_create_command_github_integration(runner, temp_dir):
    """Integration test for create command with GitHub source"""
    with mock.patch('npm2rez.cli.create_package') as mock_create:
        with mock.patch('os.path.exists') as mock_exists:
            # Setup mocks
            mock_create.return_value = os.path.join(temp_dir, 'typescript', 'main')
            mock_exists.return_value = True

            # Call command
            result = runner.invoke(cli, [
                'create',
                '--name', 'typescript',
                '--version', 'main',
                '--output', temp_dir,
                '--source', 'github',
                '--repo', 'microsoft/typescript',
                '--node-version', '16'
            ])

            # Verify result
            assert result.exit_code == 0
            assert 'Created package at' in result.output

            # Verify create_package was called with correct arguments
            mock_create.assert_called_once()
            args = mock_create.call_args[0][0]
            assert args.name == 'typescript'
            assert args.version == 'main'
            assert args.output == temp_dir
            assert args.source == 'github'
            assert args.repo == 'microsoft/typescript'
            assert args.node_version == '16'


def test_create_command_error_handling(runner, temp_dir):
    """Test error handling in create command"""
    with mock.patch('npm2rez.cli.create_package') as mock_create:
        # Setup mock to raise an exception
        mock_create.side_effect = Exception("Test error")

        # Call command
        result = runner.invoke(cli, [
            'create',
            '--name', 'typescript',
            '--version', '4.9.5',
            '--output', temp_dir,
            '--source', 'npm',
            '--node-version', '16'
        ])

        # Verify result
        assert result.exit_code == 0
        assert 'Error' in result.output


def test_extract_command_error_handling(runner, temp_dir):
    """Test error handling in extract command"""
    with mock.patch('npm2rez.cli.extract_node_package') as mock_extract:
        # Setup mock to raise an exception
        mock_extract.side_effect = Exception("Test error")

        # Call command
        result = runner.invoke(cli, [
            'extract',
            '--name', 'typescript',
            '--version', '4.9.5',
            '--output', temp_dir,
            '--source', 'npm'
        ])

        # Verify result
        assert result.exit_code == 0
        assert 'Error' in result.output
