# -*- coding: utf-8 -*-

"""
Command-line interface for npm2rez - A tool to convert Node.js packages to rez packages
"""

import argparse
import os

from npm2rez.core import create_package


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Convert Node.js package to rez package")
    parser.add_argument("--name", required=True, help="Package name")
    parser.add_argument("--version", required=True, help="Package version")
    parser.add_argument("--source", default="npm", choices=["npm", "github"], help="Package source (npm or github)")
    parser.add_argument("--repo", help="GitHub repository (format: user/repo), required when source=github")
    parser.add_argument("--output", default="./rez-packages", help="Output directory")
    parser.add_argument("--node-version", default="16", help="Node.js version requirement")
    parser.add_argument("--global", action="store_true", help="Install package globally")
    parser.add_argument("--install", action="store_true", help="Install package after creation")
    parser.add_argument("--bin-name", help="Name of the executable file")
    
    args = parser.parse_args()
    
    if args.source == "github" and not args.repo:
        parser.error("GitHub repository is required when using source=github")
        
    return args


def main():
    """Main entry point"""
    args = parse_args()
    
    # Convert package name to rez compatible format (use underscore instead of hyphen)
    rez_name = args.name.replace("-", "_").replace("@", "").replace("/", "_")
    
    # Create output directory
    output_dir = os.path.abspath(args.output)
    package_dir = os.path.join(output_dir, rez_name, args.version)
    os.makedirs(package_dir, exist_ok=True)
    
    print(f"Creating rez package: {rez_name}-{args.version}")
    
    # Create package
    package_dir = create_package(args)

    
    print(f"\nDone! Rez package created: {package_dir}")


if __name__ == "__main__":
    main()
