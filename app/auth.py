# Standard libary imports
from datetime import datetime
from functools import wraps

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, login_required, logout_user, current_user

# Local imports
from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    """Log-In-viewfunction"""
    if request.method == 'POST':
        email = request.form.get('emaiL')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', boolean=True)
