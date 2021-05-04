# Standard libary imports
from datetime import datetime

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, login_required, logout_user, current_user

# Local imports
from .models import User, Role


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login() -> 'html':
    """Log-In-viewfunction"""
    logout_user()  # log the user in
    if request.method == 'POST':  # check for the http request method
        email = request.form.get('email')
        password = request.form.get('password')
        # query the database for user
        user = User.query.filter_by(email=email).first()

        if user:
            if password == user.password:  # check the database for valid credentials
                flash('Logged in successfully.', category='success')
                login_user(user)  # log the user in
                session['full_name'] = user.full_name
                session['user_id'] = user.id
                session['roles_id'] = user.roles_id
                # redirect the user to the home view
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Email does not exist.', category='danger')
    # code executed if the http request is not a POST request
    # return the rendered template which the user can see
    return (render_template('login.html', user=current_user, roles_id=session.get('roles_id')), 200, {'location': '/login'})


@auth.route('/logout')
@login_required
def logout() -> 'redirect':
    """Logout view function, that only redirects to auth.login"""
    logout_user()
    # log out the user
    # delete all user specific entries from the session variable
    session.pop('full_name', None)
    session.pop('user_id', None)
    session.pop('roles_id', None)
    # redirect the user to the login view
    return redirect(url_for('auth.login'))
