import os
basedir = os.path.abspath(os.path.dirname(__file__))

DB_NAME = 'database.db'
DB_TESTING = 'testing.db'


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = '9QxEIB84nNKgxjz9ahPjM2HRtwrERAli4PGtjRjV'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_TESTING}'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
