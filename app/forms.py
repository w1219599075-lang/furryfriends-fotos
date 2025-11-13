from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', 
                          validators=[
                              DataRequired(message='请输入用户名'),
                              Length(min=3, max=20, message='用户名长度3-20个字符')
                          ])
    
    password = PasswordField('密码',
                           validators=[
                               DataRequired(message='请输入密码'),
                               Length(min=6, message='密码至少6个字符')
                           ])
    
    confirm_password = PasswordField('确认密码',
                                    validators=[
                                        DataRequired(message='请确认密码'),
                                        EqualTo('password', message='两次密码不一致')
                                    ])
    
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        """自定义验证：检查用户名是否已存在"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已被注册，请换一个')


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名',
                          validators=[DataRequired(message='请输入用户名')])
    
    password = PasswordField('密码',
                           validators=[DataRequired(message='请输入密码')])
    
    submit = SubmitField('登录')

