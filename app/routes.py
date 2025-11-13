from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from app.forms import RegistrationForm, LoginForm

def register_routes(app):
    """注册所有路由到应用"""
    
    @app.route('/')
    def index():
        """首页"""
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """用户注册"""
        # 如果已登录，重定向到首页
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = RegistrationForm()
        
        if form.validate_on_submit():
            # 创建新用户
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            
            # 保存到数据库
            db.session.add(user)
            db.session.commit()
            
            flash(f'注册成功！欢迎 {user.username}', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """用户登录"""
        # 如果已登录，重定向到首页
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            # 查找用户
            user = User.query.filter_by(username=form.username.data).first()
            
            # 验证用户名和密码
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f'欢迎回来，{user.username}！', 'success')
                
                # 登录成功后，跳转到之前访问的页面或首页
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('用户名或密码错误', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        """用户登出"""
        logout_user()
        flash('已退出登录', 'info')
        return redirect(url_for('index'))

