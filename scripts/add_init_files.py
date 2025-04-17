import os
from pathlib import Path
from typing import Union


def ensure_init_files(base_path: Union[str, Path]) -> None:
    abs_base_path = os.path.abspath(base_path)
    print(f"🔍 Scanning: {abs_base_path}")

    for root, dirs, files in os.walk(abs_base_path):
        # Skip hidden directories and their subdirectories
        if any(part.startswith(".") or part == "__pycache__" for part in root.split(os.sep)):
            continue

        print(f"📁 Checking: {root}")

        has_python_files = any(f.endswith(".py") for f in files)
        has_init = "__init__.py" in files

        print(f"   ├─ Contains .py files? {has_python_files}")
        print(f"   └─ Has __init__.py? {has_init}")

        if has_python_files and not has_init:
            init_path = os.path.join(root, "__init__.py")
            with open(init_path, "w") as f:
                f.write("# Automatically added __init__.py\n")
            print(f"✅ Added: {init_path}")


if __name__ == "__main__":
    ensure_init_files(".")  # current dir only
