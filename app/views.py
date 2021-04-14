# Standard libary imports
from datetime import datetime, timedelta, date
from functools import wraps
import time

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user

# Local application imports
from .models import User, Vacation


views = Blueprint('views', __name__)

# MA-home-viewfunction


@views.route('/home')
@login_required
def home():
    return render_template('home.html', full_name=session.get('full_name'), user=current_user)


@views.route('/worktime', methods=['GET', 'POST'])
@login_required
def worktime():
    if request.method == 'POST':
        start = request.form.get('start-time')
        end = request.form.get('end-time')
        breaktime = request.form.get('break-time')

        start_time = datetime.strptime(start, '%H:%M').time()
        end_time = datetime.strptime(end, '%H:%M').time()
        time_string = '{:02d}:{:02d}'.format(*divmod(int(breaktime), 60))

        break_time = datetime.strptime(time_string, '%H:%M').time()
        worktime_in_minutes = (end_time.hour-start_time.hour - break_time.hour) * \
            60 + (end_time.minute - start_time.minute - break_time.minute)
        worktime_in_hours = (end_time.hour-start_time.hour - break_time.hour) + \
            ((end_time.minute - start_time.minute - break_time.minute)/60)
        print(worktime_in_minutes, "minutes")
        print(worktime_in_hours, "hours")

    return render_template('worktime.html', user=current_user)


@views.route('/vacation', methods=['GET', 'POST'])
@login_required
def vacation():
    if request.method == 'POST':
        start_date = datetime.strptime(
            request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strftime(
            request.form.get('end_date'), '%Y-%m-%d').date()
        user_days = User.query.filter_by(id=session.get('user_id')).first()
    return render_template('vacation.html', user=current_user)


@views.route('/vacation_requests')
@login_required
def vacation_requests():
    requests = Vacation.query.all()
    users = User.query.all()
    return render_template('vacation_requests.html', requests=requests, user=current_user,  users=users, User=User)
