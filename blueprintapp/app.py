from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder= 'templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitconnect.db'
    app.config['SECRET_KEY'] = "my secret key you should not know"


    db.init_app(app)

    # Register Blueprints
    from blueprintapp.routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app