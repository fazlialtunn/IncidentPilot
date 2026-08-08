import os
import sys
from pathlib import Path

# Ensure the backend package is importable when pytest is run from the repo root.
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))
