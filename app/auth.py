# Standard libary imports
from datetime import datetime

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, login_required, logout_user, current_user

# Local imports
from .models import User, Role


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login() -> 'html':
    """Log-In-viewfunction"""
    logout_user()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if password == user.password:
                flash('Logged in successfully.', category='success')
                login_user(user)
                session['full_name'] = user.full_name
                session['user_id'] = user.id
                session['roles_id'] = user.roles_id
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Email does not exist.', category='danger')

    return render_template('login.html', user=current_user, roles_id=session.get('roles_id'))


@auth.route('/logout')
@login_required
def logout() -> 'redirect':
    logout_user()
    session.pop('full_name', None)
    session.pop('user_id', None)
    session.pop('roles_id', None)

    return redirect(url_for('auth.login'))
