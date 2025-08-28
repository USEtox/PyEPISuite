#!/usr/bin/env python3
"""
Script to help with version management and release preparation.
"""

import os
import re
import sys
import subprocess
from pathlib import Path


def get_current_version():
    """Get the current version from __init__.py"""
    init_file = Path("src/pyepisuite/__init__.py")
    if not init_file.exists():
        raise FileNotFoundError("Could not find src/pyepisuite/__init__.py")
    
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find __version__ in __init__.py")
    
    return match.group(1)


def update_version(new_version):
    """Update version in __init__.py and pyproject.toml"""
    # Update __init__.py
    init_file = Path("src/pyepisuite/__init__.py")
    content = init_file.read_text()
    updated_content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    init_file.write_text(updated_content)
    print(f"✓ Updated version in {init_file}")
    
    # Update pyproject.toml
    pyproject_file = Path("pyproject.toml")
    content = pyproject_file.read_text()
    updated_content = re.sub(
        r'version\s*=\s*["\'][^"\']+["\']',
        f'version = "{new_version}"',
        content
    )
    pyproject_file.write_text(updated_content)
    print(f"✓ Updated version in {pyproject_file}")


def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def create_and_push_tag(version):
    """Create and push a git tag"""
    tag_name = f"v{version}"
    
    # Check if we're in a git repository
    result = run_command("git status", check=False)
    if result.returncode != 0:
        print("Error: Not in a git repository")
        sys.exit(1)
    
    # Check for uncommitted changes
    result = run_command("git diff --exit-code", check=False)
    if result.returncode != 0:
        print("Warning: You have uncommitted changes. Commit them first.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create tag
    run_command(f'git tag -a {tag_name} -m "Release {version}"')
    print(f"✓ Created tag {tag_name}")
    
    # Push tag
    run_command(f"git push origin {tag_name}")
    print(f"✓ Pushed tag {tag_name} to origin")


def main():
    if len(sys.argv) < 2:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
        print()
        print("Usage:")
        print("  python scripts/release.py <new_version>  # Update version and create tag")
        print("  python scripts/release.py --current      # Show current version")
        print("  python scripts/release.py --tag-only     # Create tag for current version")
        print()
        print("Examples:")
        print("  python scripts/release.py 1.0.1")
        print("  python scripts/release.py 1.1.0")
        print("  python scripts/release.py 2.0.0-beta1")
        sys.exit(0)
    
    if sys.argv[1] == "--current":
        print(get_current_version())
        return
    
    if sys.argv[1] == "--tag-only":
        version = get_current_version()
        create_and_push_tag(version)
        return
    
    new_version = sys.argv[1]
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+(-\w+\d*)?$', new_version):
        print(f"Error: Invalid version format '{new_version}'")
        print("Expected format: X.Y.Z or X.Y.Z-suffix (e.g., 1.0.0, 1.0.0-beta1)")
        sys.exit(1)
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")
    print()
    
    response = input("Update version and create tag? (y/N): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    # Update version files
    update_version(new_version)
    
    # Commit version changes
    run_command("git add src/pyepisuite/__init__.py pyproject.toml")
    run_command(f'git commit -m "Bump version to {new_version}"')
    print("✓ Committed version changes")
    
    # Push changes
    run_command("git push origin main")
    print("✓ Pushed version changes")
    
    # Create and push tag
    create_and_push_tag(new_version)
    
    print()
    print("🎉 Release process completed!")
    print(f"✓ Version updated to {new_version}")
    print(f"✓ Tag v{new_version} created and pushed")
    print()
    print("Next steps:")
    print("1. Check GitHub Actions to ensure the release workflow runs successfully")
    print("2. Verify the package is published to PyPI")
    print("3. Check that the GitHub release was created with the correct assets")


if __name__ == "__main__":
    main()
