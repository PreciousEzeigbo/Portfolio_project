from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder= 'templates')
    workout_bp = Blueprint('workout', __name__, template_folder='templates', static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitconnect.db'
    app.config['SECRET_KEY'] = "my secret key you should not know"
    app.config['LOGIN_VIEW'] = 'login'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size: 16MB


    db.init_app(app)
    bcrypt = Bcrypt(app)


    # Initialize login_manager and set the login view
    login_manager.init_app(app)

    # Import models so they can be registered with SQLAlchemy
    from blueprintapp.models import User
    

    # Register routes
    from blueprintapp.routes import register_routes
    register_routes(app, db, bcrypt)
    
    from blueprintapp.blueprints.workout.routes import workout_bp
    app.register_blueprint(workout_bp, url_prefix='/workout')
    

    # Setup Migrate for database migrations
    migrate = Migrate(app, db)
    migrate.init_app(app, db)


    return app