import sys
import os


def setup_project_root():
    """
    Ensures project root is added to sys.path
    so 'src' imports work correctly.
    """
    current_file = os.path.abspath(__file__)

    # Go up two levels → project root
    project_root = os.path.dirname(os.path.dirname(current_file))

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    return project_root