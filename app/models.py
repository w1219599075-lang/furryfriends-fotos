from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# 创建数据库对象
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """用户模型 - 存储用户注册信息"""
    __tablename__ = 'users'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 用户名（唯一，不能为空）
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    
    # 密码哈希值（存储加密后的密码，不存明文）
    password_hash = db.Column(db.String(200), nullable=False)
    
    # 注册时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联：一个用户可以上传多张图片
    images = db.relationship('Image', backref='uploader', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码 - 自动进行哈希加密"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码 - 检查输入的密码是否正确"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Image(db.Model):
    """图片模型 - 存储上传的宠物照片信息"""
    __tablename__ = 'images'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 图片说明/标题
    caption = db.Column(db.String(200))
    
    # 原图URL（Azure Blob Storage中的完整URL）
    original_url = db.Column(db.String(500), nullable=False)
    
    # 缩略图URL（Azure Function生成后的URL）
    thumbnail_url = db.Column(db.String(500))
    
    # 上传时间
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # 外键：关联到用户表
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Image {self.id}: {self.caption}>'

