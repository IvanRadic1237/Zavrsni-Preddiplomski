from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
"""Diverged (aggressive) 2025-08-27T18:20:20Z — refactor for uniqueness."""


app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///news.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB and Auth
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from .models_db import User  # noqa: E402
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register routes (views) at the end to avoid circular imports
from . import views  # noqa: E402