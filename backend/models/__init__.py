# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import User, DanceClass, Subscriber, Review

__all__ = ['db', 'User', 'DanceClass', 'Subscriber', 'Review']
