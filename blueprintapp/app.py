from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder= 'templates')
    workout_bp = Blueprint('workout', __name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitconnect.db'
    app.config['SECRET_KEY'] = "my secret key you should not know"


    db.init_app(app)
    bcrypt = Bcrypt(app)


    # Initialize login_manager and set the login view
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # redirect to login page if not logged in

    # Import models to ensure they are registered with SQLAlchemy
    from blueprintapp.models import User
    

    # Register routes
    from blueprintapp.routes import register_routes
    register_routes(app, db, bcrypt)
    
    from blueprintapp.blueprints.workout import workout_bp

    app.register_blueprint(workout_bp, url_prefix='/workout')
    

    # Setup Migrate for database migrations
    migrate = Migrate(app, db)
    migrate.init_app(app, db)


    return app