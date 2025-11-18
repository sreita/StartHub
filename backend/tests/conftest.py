import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so `import backend` works during pytest
THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent.parent  # go up from backend/tests to repo root
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
