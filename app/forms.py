from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from app.models import User

class RegistrationForm(FlaskForm):
    """Registration form"""
    username = StringField('Username', 
                          validators=[
                              DataRequired(message='Username is required'),
                              Length(min=3, max=20, message='Username must be 3-20 characters')
                          ])
    
    password = PasswordField('Password',
                           validators=[
                               DataRequired(message='Password is required'),
                               Length(min=6, message='Password must be at least 6 characters')
                           ])
    
    confirm_password = PasswordField('Confirm Password',
                                    validators=[
                                        DataRequired(message='Please confirm password'),
                                        EqualTo('password', message='Passwords must match')
                                    ])
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken')


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username',
                          validators=[DataRequired(message='Username is required')])

    password = PasswordField('Password',
                           validators=[DataRequired(message='Password is required')])

    submit = SubmitField('Login')


class UploadForm(FlaskForm):
    """Image upload form"""
    image = FileField('Choose Image',
                     validators=[
                         FileRequired(message='Please select an image'),
                         FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'webp'],
                                   message='Only image files are allowed (PNG, JPG, GIF, WebP)')
                     ])

    caption = TextAreaField('Caption (Optional)',
                          validators=[
                              Optional(),
                              Length(max=200, message='Caption must be less than 200 characters')
                          ])

    submit = SubmitField('Upload')

