# Standard libary imports
from datetime import datetime
from functools import wraps

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash


# Local imports
from .models import User


auth = Blueprint('auth', __name__)


def check_logged_in(func: object) -> object:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return redirect(url_for('login'))
    return wrapper


@auth.route('/', methods=['GET', 'POST'])
def login():
    """Log-In-viewfunction"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist or has a spelling mistake.', category='error')

    return render_template('login.html', boolean=True)
