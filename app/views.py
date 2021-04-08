# Standard libary imports
from datetime import datetime
from functools import wraps

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint

# Local application imports

views = Blueprint('views', __name__)

# MA-home-viewfunction


@views.route('/home')
def home():
    return '<h1>Mitarbeiter Home View'


@views.route('/logout')
def logout():
    session.pop('logged_in')


# MA-statistic-viewfunction


# MA-vacation-viewfunction


# SU-home-viewfunction


# SU-applications-viewfunction


# HR-home-viewfunction
