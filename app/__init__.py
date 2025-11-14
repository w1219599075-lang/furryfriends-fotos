from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.models import db, User

# init Flask-Login
login_manager = LoginManager()

def create_app(config_class=Config):
    """App factory - create and configure Flask app"""

    # create Flask app instance
    app = Flask(__name__)

    # load config
    app.config.from_object(config_class)

    # init database
    db.init_app(app)

    # init login manager
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # redirect to login if not authenticated
    login_manager.login_message = 'Please log in first'

    # create database tables
    with app.app_context():
        db.create_all()

    # register routes
    from app.routes import register_routes
    register_routes(app)

    return app


# expose a module-level `app` instance so hosts expecting `app:app` (e.g. Azure)
# can locate the Flask application without a custom startup command.
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    """User loader function required by Flask-Login"""
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        # Log the error and return None to handle database connection issues gracefully
        print(f"Error loading user {user_id}: {str(e)}")
        return None
