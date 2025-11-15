"""Pytest configuration for src module tests."""

import sys
from pathlib import Path

# Set up Python path at module level so it's available when test modules are imported
# Get the backend directory (parent of tests directory) and resolve to absolute path
_backend_dir = Path(__file__).parent.parent.parent.resolve()
_backend_dir_str = str(_backend_dir)

# Add to Python path if not already there (check both absolute and relative)
if _backend_dir_str not in sys.path:
    sys.path.insert(0, _backend_dir_str)
# Also add relative path in case pytest uses relative paths
_backend_dir_relative = str(Path(__file__).parent.parent.parent)
if _backend_dir_relative not in sys.path and _backend_dir_relative != _backend_dir_str:
    sys.path.insert(0, _backend_dir_relative)

