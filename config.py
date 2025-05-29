import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

    # For Vercel deployment, use PostgreSQL or other cloud database
    # Default to in-memory SQLite for local development
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Production database (PostgreSQL, MySQL, etc.)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local development - use in-memory SQLite to avoid file system issues
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Disable Flask-SQLAlchemy's automatic instance folder creation
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
