import sys
from pathlib import Path

# Ensure project root (containing the 'api' package) is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent  # Берем папку, а не файл
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
