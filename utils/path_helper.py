import sys
import os

def setup_project_path():
    """Add project root to Python path"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

# Automatically setup path when module is imported
setup_project_path()
