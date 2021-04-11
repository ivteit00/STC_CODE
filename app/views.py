# Standard libary imports
from datetime import datetime, timedelta
from functools import wraps
import time

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user

# Local application imports

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
    return render_template('vacation.html', user=current_user)

# MA-statistic-viewfunction


# MA-vacation-viewfunction


# SU-home-viewfunction


# SU-applications-viewfunction


# HR-home-viewfunction
