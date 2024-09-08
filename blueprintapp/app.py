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

    login_manager = LoginManager()
    login_manager.init_app(app)

    from blueprintapp.models import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    bcrypt = Bcrypt(app)

    # Register routes
    from blueprintapp.routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)
    migrate.init_app(app, db)


    return app