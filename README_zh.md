# npm2rez

<div align="center">
    <img src="https://raw.githubusercontent.com/loonghao/npm2rez/master/logo.svg" alt="npm2rez Logo" width="200"/>
</div>

一个将 Node.js 包转换为 rez 包的工具，用于 VFX 和动画流水线集成。

[![PyPI version](https://badge.fury.io/py/npm2rez.svg)](https://badge.fury.io/py/npm2rez)
[![Python Version](https://img.shields.io/pypi/pyversions/npm2rez.svg)](https://pypi.org/project/npm2rez/)
[![Downloads](https://static.pepy.tech/badge/npm2rez)](https://pepy.tech/project/npm2rez)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/loonghao/npm2rez/branch/master/graph/badge.svg)](https://codecov.io/gh/loonghao/npm2rez)

[English](README.md) | [中文](README_zh.md)

## 功能特点

- 支持从 npm 或 GitHub 安装 Node.js 包
- 自动创建符合 rez 规范的包结构
- 配置正确的环境变量和路径
- 支持可执行文件的创建和配置
- 生成详细的文档和更新日志

## 安装

```bash
# 从 PyPI 安装
pip install npm2rez
# 或使用 uv 安装
uv pip install npm2rez

# 或从源码安装
git clone https://github.com/loonghao/npm2rez.git
cd npm2rez
uv pip install -e .
```

## 使用方法

### 基本用法

```bash
# 使用 uvx 运行（推荐）
uvx npm2rez --name typescript --version 4.9.5 --source npm --node-version 16.14.0

# 或直接运行
npm2rez --name typescript --version 4.9.5 --source npm --node-version 16.14.0

# 从 GitHub 创建包
uvx npm2rez --name typescript --version 4.9.5 --source github --repo microsoft/TypeScript
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--name` | 包名称 | (必填) |
| `--version` | 包版本 | (必填) |
| `--source` | 包源（npm 或 github） | npm |
| `--repo` | GitHub 仓库（格式：user/repo），当 source=github 时必填 | 无 |
| `--output` | 输出目录 | ./rez-packages |
| `--node-version` | Node.js 版本要求 | 16 |
| `--global` | 全局安装包 | False |
| `--install` | 创建后安装包 | False |
| `--bin-name` | 可执行文件名称 | 无 |

## 示例

### 创建 TypeScript 包

```bash
npm2rez --name typescript --version 4.9.5 --bin-name tsc
```

这将创建一个 TypeScript 版本 4.9.5 的 rez 包，并配置 `tsc` 可执行文件。

### 使用创建的包

```bash
# 激活包环境
rez env typescript-4.9.5

# 或直接运行可执行文件
rez env typescript-4.9.5 -- tsc --version
```

## 开发

```bash
# 克隆仓库
git clone https://github.com/loonghao/npm2rez.git
cd npm2rez

# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
uvx nox -s pytest

# 运行真实包测试
uvx nox -s pytest-real-packages

# 运行代码检查
uvx nox -s lint
```

## 许可证

MIT
