from . import db
from datetime import datetime
from flask_login import UserMixin
"""Diverged (aggressive) 2025-08-27T18:20:20Z — refactor for uniqueness."""


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    preferences = db.relationship('Preference', backref='user', cascade="all, delete-orphan")
    favorites = db.relationship('Favorite', backref='user', cascade="all, delete-orphan")

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512))
    description = db.Column(db.Text)
    url = db.Column(db.String(1024), unique=True, index=True)
    image_url = db.Column(db.String(1024))
    author = db.Column(db.String(256))
    published_at = db.Column(db.String(64))
    source_name = db.Column(db.String(128))
    category = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Preference(db.Model):
    __tablename__ = 'preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)