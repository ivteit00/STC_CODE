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
        flash('You are currently not logged in. Please log in', category='error')
        return redirect(url_for('auth.login'))
    return wrapper


@auth.route('/', methods=['GET', 'POST'])
def login():
    """Log-In-viewfunction"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if True:
            if True:
                session['logged_in'] = True
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist or has a spelling mistake.', category='error')
    return render_template('login.html', boolean=True)
