import os
from app import create_app
from flask_script import Manager, Shell


app = create_app('default')


if __name__ == '__main__':
    app.run(debug=True)
