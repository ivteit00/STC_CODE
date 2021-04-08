from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9QxEIB84nNKgxjz9ahPjM2HRtwrERAli4PGtjRjV'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Register all blueprints
    from .auth import auth
    from .views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)

    from .models import User

    create_database(app=app)

    return app


def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Created database!')
