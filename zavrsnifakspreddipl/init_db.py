"""Helper script to initialize the SQLite database for the Flask app.

Works when executed from inside the project folder by importing the package by its folder name.
"""
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
db = getattr(pkg, "db")

if __name__ == "__main__":
    print("Creating all database tables...")
    with app.app_context():
        db.create_all()
    print("Done. Database tables created in news.db")
