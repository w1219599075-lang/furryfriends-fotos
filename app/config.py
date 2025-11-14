import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

class Config:
    """App configuration from environment variables"""

    # Flask basic config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change'

    # Database config - PostgreSQL in production, SQLite for dev
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database connection pool settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,      # recycle connections after 1 hour
        'pool_pre_ping': True,     # test connection before use
        'max_overflow': 20,
        'pool_timeout': 30,
    }

    # Azure Blob Storage config
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_STORAGE_CONTAINER_ORIGINAL = os.environ.get('AZURE_STORAGE_CONTAINER_ORIGINAL', 'originals')
    AZURE_STORAGE_CONTAINER_THUMBNAIL = os.environ.get('AZURE_STORAGE_CONTAINER_THUMBNAIL', 'thumbnails')

    # File upload config
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # max upload size 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

