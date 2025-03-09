#!/usr/bin/env python

"""
Command line interface for npm2rez
"""

import sys
from types import SimpleNamespace

import click

from npm2rez.core import create_package, extract_node_package


@click.group()
def cli():
    """npm2rez - Convert npm packages to rez packages"""


@cli.command()
@click.option("--name", required=True, help="Name of the npm package")
@click.option("--version", required=True, help="Version of the npm package")
@click.option(
    "--source",
    default="npm",
    type=click.Choice(["npm", "github"]),
    help="Source to install from (npm or github)",
)
@click.option(
    "--repo",
    help="GitHub repository (required when source=github)",
)
@click.option(
    "--output",
    default="./rez-packages",
    help="Output directory for the rez package",
)
@click.option(
    "--node-version",
    default="16",
    help="Node.js version to use",
)
def create(name, version, source, repo, output, node_version):
    """Create a rez package from an npm package"""
    # Validate GitHub source arguments
    if source == "github" and not repo:
        click.echo("Error: When using github source, --repo is required")
        return 1

    # Create args object to pass to create_package
    args = SimpleNamespace(
        name=name,
        version=version,
        source=source,
        repo=repo,
        output=output,
        node_version=node_version,
        _is_test=False
    )

    try:
        package_dir = create_package(args)
        click.echo(f"Created package at: {package_dir}")
        return 0
    except Exception as e:
        click.echo(f"Error creating package: {str(e)}")
        return 1


@cli.command()
@click.option("--name", required=True, help="Name of the npm package")
@click.option("--version", required=True, help="Version of the npm package")
@click.option(
    "--source",
    default="npm",
    type=click.Choice(["npm", "github"]),
    help="Source to install from (npm or github)",
)
@click.option(
    "--repo",
    help="GitHub repository (required when source=github)",
)
@click.option(
    "--output",
    default="./node_modules",
    help="Output directory for the node modules",
)
def extract(name, version, source, repo, output):
    """Extract a Node.js package without creating a rez package"""
    # Validate GitHub source arguments
    if source == "github" and not repo:
        click.echo("Error: When using github source, --repo is required")
        return 1

    # Create args object to pass to extract_node_package
    args = SimpleNamespace(
        name=name,
        version=version,
        source=source,
        repo=repo,
        _is_test=False
    )

    try:
        result = extract_node_package(args, output)
        if result:
            click.echo(f"Successfully extracted package to: {output}")
            return 0
        else:
            click.echo(f"Failed to extract package to: {output}")
            return 1
    except Exception as e:
        click.echo(f"Error extracting package: {str(e)}")
        return 1


def main():
    """Main entry point for npm2rez"""
    return cli()


if __name__ == "__main__":
    sys.exit(main())
