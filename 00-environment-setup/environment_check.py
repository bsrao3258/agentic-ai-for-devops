"""Example 2: verify the Python runtime without installing packages.

Run from the repository root:
    python 00-environment-setup/environment_check.py
"""
import platform
import sys
from pathlib import Path

print("Python version:", platform.python_version())
print("Operating system:", platform.system())
print("Python executable:", Path(sys.executable).name)
print("Virtual environment active:", sys.prefix != sys.base_prefix)
