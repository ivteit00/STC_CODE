from flask import Flask, render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from os import path

from config import config

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app(config_name):
    app = Flask(__name__)
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

    create_database(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('app/'+DB_NAME):
        db.create_all(app=app)
        print('Created database!')
