# Standard libary imports
from datetime import datetime
from functools import wraps

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user

# Local application imports

views = Blueprint('views', __name__)

# MA-home-viewfunction


@views.route('/home')
@login_required
def home():
    return render_template('home.html', full_name=session.get('full_name'))


# MA-statistic-viewfunction


# MA-vacation-viewfunction


# SU-home-viewfunction


# SU-applications-viewfunction


# HR-home-viewfunction
