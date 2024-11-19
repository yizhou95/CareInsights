from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Single instance of SQLAlchemy

def init_app(app):
    db.init_app(app)

__all__ = ['db','init_app']