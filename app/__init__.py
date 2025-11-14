from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.models import db, User

# init Flask-Login
login_manager = LoginManager()

def create_app(config_class=Config):
    """Create and configure the Flask app"""

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in first'

    with app.app_context():
        db.create_all()

    from app.routes import register_routes
    register_routes(app)

    return app


# module-level app instance for Azure deployment
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        print(f"Error loading user {user_id}: {str(e)}")
        return None
