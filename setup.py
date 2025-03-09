#!/usr/bin/env python


from setuptools import setup

setup(
    name="npm2rez",
    version="0.0.1",
    description="Convert npm packages to rez packages",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Hal Long",
    author_email="hal.long@outlook.com",
    url="https://github.com/loonghao/npm2rez",
    packages=["npm2rez"],
    package_data={"npm2rez": ["*.py"]},
    entry_points={
        "console_scripts": [
            "npm2rez=npm2rez.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
