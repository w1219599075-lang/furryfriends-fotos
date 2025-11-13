import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Config:
    """应用配置类 - 从环境变量读取配置信息"""
    
    # Flask基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change'
    
    # 数据库配置
    # 优先使用PostgreSQL，如果没配置就用本地SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        # 修复Heroku的postgres://为postgresql://
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭修改追踪，节省内存
    
    # Azure Blob Storage配置
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_STORAGE_CONTAINER_ORIGINAL = os.environ.get('AZURE_STORAGE_CONTAINER_ORIGINAL', 'originals')
    AZURE_STORAGE_CONTAINER_THUMBNAIL = os.environ.get('AZURE_STORAGE_CONTAINER_THUMBNAIL', 'thumbnails')
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

