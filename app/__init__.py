from flask import Flask, render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from os import path

from config import config

db = SQLAlchemy()
DB_NAME = 'database.db'
DB_TESTING = 'testing.db'


def create_app(config_name) -> 'Flask':
    """App factory"""
    app = Flask(__name__)
    # cofiguring the app with the classes from the config.py file
    app.config.from_object(config[config_name])
    db.init_app(app)

    # Register all blueprints
    from .auth import auth
    from .views import views
    from .worktime import work
    from .vacation import vac
    from .illness import ill

    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(work)
    app.register_blueprint(vac)
    app.register_blueprint(ill)

    from .models import User
    # create the database
    create_database(app=app)

    # create and configer the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    login_manager.login_message = "You need to log-in in order to access this page."
    login_manager.login_message_category = "warning"

    return app


def create_database(app):
    """database factory"""
    # only create db if it doesn't exist
    if not path.exists('app/'+DB_NAME):
        db.create_all(app=app)
        print('Created database!')
