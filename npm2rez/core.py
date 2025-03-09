"""
Core functionality for npm2rez - A tool to convert Node.js packages to rez packages
"""

import json
import os
import shutil
import subprocess


def create_package(args):
    """Create rez package"""
    # Convert package name to rez compatible format (use underscore instead of hyphen)
    rez_name = args.name.replace("-", "_").replace("@", "").replace("/", "_")

    # Create output directory
    output_dir = os.path.abspath(args.output)
    package_dir = os.path.join(output_dir, rez_name, args.version)
    os.makedirs(package_dir, exist_ok=True)
    # Create package.py file
    create_package_py(args, package_dir)

    # Install Node.js package
    install_node_package(args, package_dir)

    return package_dir


def create_package_py(args, package_dir):
    """Create package.py file"""
    package_py_path = os.path.join(package_dir, "package.py")

    # Convert package name to rez compatible format (use underscore instead of hyphen)
    rez_name = args.name.replace("-", "_").replace("@", "").replace("/", "_")

    # Prepare template content
    package_content = f'''
name = "{rez_name}"
version = "{args.version}"

description = "Rez package for {args.name} Node.js package"

requires = [
    "nodejs-{args.node_version}+",
]

def commands():
    import os
    # Set environment variable (uppercase, replace hyphen with underscore)
    env.{rez_name.upper()}_ROOT = "{{root}}"
'''

    # If there is an executable file, add to PATH
    if getattr(args, 'bin_name', None):
        package_content += '''
    # Add executable to PATH
    env.PATH.append("{{root}}")
'''

    # Add to NODE_PATH
    package_content += '''
    # Add to NODE_PATH
    if "NODE_PATH" not in env:
        env.NODE_PATH = "{{root}}/node_modules"
    else:
        env.NODE_PATH.append("{{root}}/node_modules")
'''

    # Write to file
    with open(package_py_path, "w", encoding="utf-8") as f:
        f.write(package_content)

    print(f"Created {package_py_path}")


def install_node_package(args, install_path):
    """Install Node.js package to specified directory"""
    # Create installation directory
    os.makedirs(install_path, exist_ok=True)
    npm = shutil.which("npm")
    # Check if npm is available
    try:
        subprocess.check_call(
            [npm, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # npm is available, continue with installation
    except (subprocess.SubprocessError, FileNotFoundError):
        # npm is not available
        print("Warning: npm command not found. Package files will be created but "
              "Node.js packages won't be installed.")
        print("Please install Node.js and npm to enable package installation.")
        # Create empty node_modules directory
        os.makedirs(os.path.join(install_path, "node_modules"), exist_ok=True)
        return

    if args.source == "npm":
        # Install from npm
        # Create package.json file to ensure local installation
        package_json_path = os.path.join(install_path, "package.json")
        with open(package_json_path, "w", encoding="utf-8") as f:
            json.dump({
                "name": "npm2rez-temp",
                "version": "1.0.0",
                "private": True
            }, f)

        # Install locally (without --global flag)
        subprocess.check_call([
            npm, "install", f"{args.name}@{args.version}",
            "--save", "--save-exact"
        ], cwd=install_path)

        # Create bin directory and symlink or copy binaries
        bin_dir = os.path.join(install_path, "bin")
        os.makedirs(bin_dir, exist_ok=True)

        # Find binaries in node_modules/.bin
        node_bin_dir = os.path.join(install_path, "node_modules", ".bin")
        if os.path.exists(node_bin_dir):
            # Copy or create symlinks to binaries
            for bin_file in os.listdir(node_bin_dir):
                src_path = os.path.join(node_bin_dir, bin_file)
                dst_path = os.path.join(bin_dir, bin_file)

                if os.name == "nt":  # Windows
                    # On Windows, copy the file
                    shutil.copy2(src_path, dst_path)
                else:  # Unix-like
                    # On Unix, create a symlink
                    if os.path.exists(dst_path):
                        os.remove(dst_path)
                    os.symlink(src_path, dst_path)
    else:
        # Install from GitHub
        repo_url = f"https://github.com/{args.repo}.git"
        temp_dir = os.path.join(os.path.dirname(install_path), "temp_repo")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # Clone to temporary directory
            subprocess.check_call([
                "git", "clone", "--depth", "1", "--branch", f"v{args.version}",
                repo_url, temp_dir
            ])

            # Install dependencies and build
            subprocess.check_call([npm, "install"], cwd=temp_dir)
            subprocess.check_call([npm, "run", "build"], cwd=temp_dir)

            # Copy all files to installation directory
            for item in os.listdir(temp_dir):
                src_path = os.path.join(temp_dir, item)
                dst_path = os.path.join(install_path, item)

                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)

            print(f"Installed {args.name}@{args.version} from GitHub")
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
