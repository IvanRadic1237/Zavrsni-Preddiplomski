"""Helper script to run the Flask app directly with `python run.py`."""
import sys
from pathlib import Path
import importlib

project_dir = Path(__file__).resolve().parent
parent_dir = project_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

pkg_name = project_dir.name
pkg = importlib.import_module(pkg_name)
app = getattr(pkg, "app")

if __name__ == "__main__":
    app.run(debug=True)
