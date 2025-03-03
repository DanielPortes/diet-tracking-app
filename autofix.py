#!/usr/bin/env python
"""Script to automatically fix common flake8 issues."""

import re
import sys
from pathlib import Path


def fix_docstring_periods(file_path):
    """Add periods to docstrings that are missing them."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find docstrings that don't end with periods
    pattern = r'(def [^:]+:\s*\n\s*"""[^".]*[^.\s"])("""\s*\n)'
    updated = re.sub(pattern, r"\1.\2", content)

    # Fixed triple-quoted docstrings at the beginning of functions
    pattern = r'(def [^:]+:\s*\n\s*"""[^".]*[^.\s"])(\s*\n)'
    updated = re.sub(pattern, r"\1.\2", updated)

    # Find class/module level docstrings without periods
    pattern = r'("""[^".]*[^.\s"])("""\s*\n)'
    updated = re.sub(pattern, r"\1.\2", updated)

    if content != updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
    return False


def fix_unused_imports(file_path):
    """Remove unused imports."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Simple pattern to detect import lines
    import_pattern = re.compile(r"^\s*import\s+([^\s]+)|^\s*from\s+([^\s]+)\s+import")

    # Get unused imports from running flake8
    import subprocess

    result = subprocess.run(
        ["flake8", "--select=F401", str(file_path)], capture_output=True, text=True
    )

    unused_imports = []
    for line in result.stdout.splitlines():
        if "F401" in line:
            # Extract the import name
            match = re.search(r"'([^']+)'", line)
            if match:
                unused_imports.append(match.group(1))

    if unused_imports:
        # Create a new file with unused imports removed
        with open(file_path + ".tmp", "w", encoding="utf-8") as f:
            for line in lines:
                skip_line = False
                for unused in unused_imports:
                    if import_pattern.match(line) and unused in line:
                        skip_line = True
                        break
                if not skip_line:
                    f.write(line)

        # Replace the original file
        Path(file_path + ".tmp").replace(file_path)
        return True

    return False


def fix_unused_variables(file_path):
    """Rename or remove unused variables."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Get unused variables from running flake8
    import subprocess

    result = subprocess.run(
        ["flake8", "--select=F841", str(file_path)], capture_output=True, text=True
    )

    modified = False

    for line in result.stdout.splitlines():
        if "F841" in line:
            # Extract the variable name
            match = re.search(r"local variable '([^']+)' is", line)
            if match:
                var_name = match.group(1)
                # Find the assignment
                pattern = rf"({var_name}\s*=\s*[^;#\n]+)"

                # Replace with an underscore prefix to indicate intentional non-use
                updated = re.sub(pattern, r"_\1", content)

                # If we couldn't make the change (maybe it's a complex case), add a comment
                if updated == content:
                    # Try to find the line with the assignment
                    line_num = int(line.split(":")[1])
                    lines = content.splitlines()
                    if 0 <= line_num - 1 < len(lines):
                        lines[line_num - 1] += "  # noqa: F841"
                        content = "\n".join(lines)
                        modified = True
                else:
                    content = updated
                    modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    return False


def main():
    """Run the auto-fixer on specified files."""
    if len(sys.argv) < 2:
        print("Usage: python autofix.py <python_file1> [python_file2 ...]")
        return

    for file_path in sys.argv[1:]:
        path = Path(file_path)
        if not path.exists() or not path.is_file() or path.suffix != ".py":
            print(f"Skipping {file_path} - not a Python file or doesn't exist")
            continue

        print(f"Processing {file_path}...")

        changes = []

        if fix_docstring_periods(file_path):
            changes.append("Fixed missing periods in docstrings")

        # if fix_unused_imports(file_path):
        #     changes.append("Removed unused imports")
        #
        # if fix_unused_variables(file_path):
        #     changes.append("Fixed unused variables")

        if changes:
            print(f"✅ Changes made to {file_path}:")
            for change in changes:
                print(f"  - {change}")
        else:
            print(f"👍 No issues fixed in {file_path}")


if __name__ == "__main__":
    main()
