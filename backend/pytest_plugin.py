"""Pytest plugin to set up Python path early."""

import sys
from pathlib import Path


def pytest_configure(config):
    """Configure pytest - runs early in the pytest startup process."""
    # Get the backend directory (where pytest.ini is located)
    backend_dir = Path(config.rootdir).resolve()
    backend_dir_str = str(backend_dir)

    # Add to Python path if not already there
    if backend_dir_str not in sys.path:
        sys.path.insert(0, backend_dir_str)


def pytest_load_initial_conftests(early_config, parser, args):
    """Load initial conftests - runs even earlier than pytest_configure."""
    import sys
    from pathlib import Path

    # Get the backend directory
    backend_dir = Path(early_config.rootdir).resolve()
    backend_dir_str = str(backend_dir)

    # Add to Python path if not already there
    if backend_dir_str not in sys.path:
        sys.path.insert(0, backend_dir_str)

