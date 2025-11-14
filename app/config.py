import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

class Config:
    """App config class - reads settings from environment variables"""

    # Flask basic config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change'

    # Database config
    # Use PostgreSQL if available, otherwise fallback to SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        # Fix Heroku's postgres:// to postgresql://
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # disable modification tracking to save memory

    # Database connection pool settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,           # 连接池大小
        'pool_recycle': 3600,      # 1小时后回收连接（Azure SQL 默认连接超时）
        'pool_pre_ping': True,     # 每次使用前测试连接是否有效
        'max_overflow': 20,        # 连接池满时允许的额外连接数
        'pool_timeout': 30,        # 获取连接的超时时间（秒）
    }

    # Azure Blob Storage config
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_STORAGE_CONTAINER_ORIGINAL = os.environ.get('AZURE_STORAGE_CONTAINER_ORIGINAL', 'originals')
    AZURE_STORAGE_CONTAINER_THUMBNAIL = os.environ.get('AZURE_STORAGE_CONTAINER_THUMBNAIL', 'thumbnails')

    # File upload config
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # max upload size 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

