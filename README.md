# npm2rez

<div align="center">
    <img src="./logo.svg" alt="npm2rez Logo" width="200"/>
</div>

A tool to convert Node.js packages to rez packages for VFX and animation pipeline integration.

[![PyPI version](https://badge.fury.io/py/npm2rez.svg)](https://badge.fury.io/py/npm2rez)
[![Python Version](https://img.shields.io/pypi/pyversions/npm2rez.svg)](https://pypi.org/project/npm2rez/)
[![Downloads](https://static.pepy.tech/badge/npm2rez)](https://pepy.tech/project/npm2rez)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/loonghao/npm2rez/branch/master/graph/badge.svg)](https://codecov.io/gh/loonghao/npm2rez)

[English](README.md) | [中文](README_zh.md)

## Features

- Support for installing Node.js packages from npm or GitHub
- Automatically create rez-compliant package structure
- Configure correct environment variables and paths
- Support for executable creation and configuration
- Generate detailed documentation and changelogs

## Installation

```bash
# Install from PyPI
pip install npm2rez
# Or use uv to install
uv pip install npm2rez

# Or install from source
git clone https://github.com/loonghao/npm2rez.git
cd npm2rez
uv pip install -e .
```

## Usage

### Basic Usage

```bash
# Run with uvx (recommended)
uvx npm2rez --name typescript --version 4.9.5 --source npm --node-version 16.14.0

# Or run directly
npm2rez --name typescript --version 4.9.5 --source npm --node-version 16.14.0

# Create package from GitHub
uvx npm2rez --name typescript --version 4.9.5 --source github --repo microsoft/TypeScript
```

### Command Line Arguments

| Parameter | Description | Default |
|-----------|-------------|--------|
| `--name` | Package name | (required) |
| `--version` | Package version | (required) |
| `--source` | Package source (npm or github) | npm |
| `--repo` | GitHub repository (format: user/repo), required when source=github | None |
| `--output` | Output directory | ./rez-packages |
| `--node-version` | Node.js version requirement | 16 |
| `--global` | Install package globally | False |
| `--install` | Install package after creation | False |
| `--bin-name` | Name of the executable file | None |

## Examples

### Creating a TypeScript Package

```bash
npm2rez --name typescript --version 4.9.5 --bin-name tsc
```

This will create a rez package for TypeScript version 4.9.5 with the executable `tsc`.

### Using the Created Package

```bash
# Activate the package environment
rez env typescript-4.9.5

# Or directly run the executable
rez env typescript-4.9.5 -- tsc --version
```

## Development

```bash
# Clone the repository
git clone https://github.com/loonghao/npm2rez.git
cd npm2rez

# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
uvx nox -s pytest

# Run real package tests
uvx nox -s pytest-real-packages

# Run linting
uvx nox -s lint
```

## License

MIT
