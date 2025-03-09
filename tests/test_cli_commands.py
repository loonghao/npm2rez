#!/usr/bin/env python

"""
Test CLI commands for npm2rez package
"""

from unittest import mock

import pytest
from click.testing import CliRunner

from npm2rez.cli import cli


@pytest.fixture
def runner():
    """Create CLI runner for testing"""
    return CliRunner()


def test_cli_help(runner):
    """Test CLI help command"""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
    assert 'create' in result.output
    assert 'extract' in result.output


def test_create_help(runner):
    """Test create command help"""
    result = runner.invoke(cli, ['create', '--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
    assert '--name' in result.output
    assert '--version' in result.output


def test_extract_help(runner):
    """Test extract command help"""
    result = runner.invoke(cli, ['extract', '--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
    assert '--name' in result.output
    assert '--version' in result.output


def test_create_command_npm_source(runner):
    """Test create command with npm source"""
    with mock.patch('npm2rez.cli.create_package') as mock_create:
        # Setup mock
        mock_create.return_value = '/path/to/package'

        # Call command
        result = runner.invoke(cli, [
            'create',
            '--name', 'typescript',
            '--version', '4.9.5',
            '--output', './rez-packages',
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
        assert args.output == './rez-packages'
        assert args.source == 'npm'
        assert args.node_version == '16'


def test_create_command_github_source(runner):
    """Test create command with github source"""
    with mock.patch('npm2rez.cli.create_package') as mock_create:
        # Setup mock
        mock_create.return_value = '/path/to/package'

        # Call command
        result = runner.invoke(cli, [
            'create',
            '--name', 'typescript',
            '--version', 'main',
            '--output', './rez-packages',
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
        assert args.output == './rez-packages'
        assert args.source == 'github'
        assert args.repo == 'microsoft/typescript'
        assert args.node_version == '16'


def test_create_command_missing_required_args(runner):
    """Test create command with missing required arguments"""
    # Test missing name
    result = runner.invoke(cli, [
        'create',
        '--version', '4.9.5',
        '--output', './rez-packages'
    ])
    assert result.exit_code != 0
    assert 'Missing option' in result.output

    # Test missing version
    result = runner.invoke(cli, [
        'create',
        '--name', 'typescript',
        '--output', './rez-packages'
    ])
    assert result.exit_code != 0
    assert 'Missing option' in result.output


def test_create_command_github_source_missing_repo(runner):
    """Test create command with github source but missing repo"""
    result = runner.invoke(cli, [
        'create',
        '--name', 'typescript',
        '--version', 'main',
        '--output', './rez-packages',
        '--source', 'github'
    ])
    assert result.exit_code == 0
    assert 'Error: When using github source, --repo is required' in result.output


def test_extract_command(runner):
    """Test extract command"""
    with mock.patch('npm2rez.cli.extract_node_package') as mock_extract:
        # Setup mock
        mock_extract.return_value = True

        # Call command
        result = runner.invoke(cli, [
            'extract',
            '--name', 'typescript',
            '--version', '4.9.5',
            '--output', './node_modules',
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
        assert output_dir == './node_modules'


def test_extract_command_failure(runner):
    """Test extract command when extraction fails"""
    with mock.patch('npm2rez.cli.extract_node_package') as mock_extract:
        # Setup mock
        mock_extract.return_value = False

        # Call command
        result = runner.invoke(cli, [
            'extract',
            '--name', 'typescript',
            '--version', '4.9.5',
            '--output', './node_modules',
            '--source', 'npm'
        ])

        # Verify result
        assert result.exit_code == 0
        assert 'Failed to extract' in result.output
