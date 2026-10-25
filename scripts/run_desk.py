"""Run the versioned desk from this self-contained Skill folder."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from desk_core.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
