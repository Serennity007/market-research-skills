"""Run the self-contained chemicals research desk."""
import sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
if not (root/'desk_core').is_dir():
    root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root))
from desk_core.cli import main
if __name__=="__main__":
    raise SystemExit(main('chemicals'))
