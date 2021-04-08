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
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if password == user.password:
                flash('Logged in successfully', category='success')
                login_user(user)
                session['full_name'] = user.full_name
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='danger')
        else:
            flash('Email does not exist.', category='danger')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
