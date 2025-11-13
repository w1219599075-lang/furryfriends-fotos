from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.models import db, User

# 初始化 Flask-Login
login_manager = LoginManager()

def create_app(config_class=Config):
    """应用工厂函数 - 创建并配置 Flask 应用"""
    
    # 创建 Flask 应用实例
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config_class)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化登录管理器
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # 未登录时重定向到登录页
    login_manager.login_message = '请先登录'
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 注册路由
    from app.routes import register_routes
    register_routes(app)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login 需要的用户加载函数"""
    return User.query.get(int(user_id))

