from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
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


def create_dummy_users():
    from .models import User, Role

    worker_role = Role(name='worker')
    chef_role = Role(name='chef')
    hr_role = Role(name='hr')

    test_user_1 = User(email='test1@gmail.de',
                       password='password', full_name='Max Mustermann')
    test_user_1 = User(email='test2@gmail.de',
                       password='password', full_name='John Doe')
    test_user_1 = User(email='test3@gmail.de',
                       password='password', full_name='Anita John')
