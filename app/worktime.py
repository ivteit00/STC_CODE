# Standard libary imports
from datetime import datetime, timedelta, date
import time

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user

# Local application imports
from .models import User, Vacation, Illness
from . import db


work = Blueprint('worktime', __name__)


@work.route('/worktime', methods=['GET', 'POST'])
@login_required
def worktime():
    if request.method == 'POST':
        error = False
        start = request.form.get('start-time')
        end = request.form.get('end-time')
        breaktime = '{:02d}:{:02d}'.format(
            *divmod(int(request.form.get('break-time')), 60))

        start_time = datetime.strptime(start, '%H:%M').time()
        end_time = datetime.strptime(end, '%H:%M').time()
        break_time = datetime.strptime(breaktime, '%H:%M').time()

        start_minutes = calculate_minutes(start_time)
        end_minutes = calculate_minutes(end_time)
        break_minutes = calculate_minutes(break_time)

        if start_minutes > end_minutes:
            error = True
        if break_minutes < 0:
            error = True

        if calculate_worktime_minutes(start_minutes=start_minutes, end_minutes=end_minutes, break_minutes=break_minutes) < 0:
            error = True
        if break_minutes < 30:
            flash('Your break time is to low. Please resubmit your Worktime later and make a longer break :) ',
                  category='warning')
            return redirect(url_for('worktime.worktime'))
        if error:
            flash('You have entered invalid values. Please check your input.',
                  category='danger')
            return redirect(url_for('worktime.worktime'))
        else:
            user = User.query.filter_by(id=session.get('user_id')).first()
            user.worked_hours = user.worked_hours + w

    return render_template('worktime.html', user=current_user, roles_id=session.get('roles_id'))


def calculate_minutes(time: datetime.time):
    return (time.hour*60 + time.minute)


def calculate_worktime_minutes(start_minutes: int, end_minutes: int, break_minutes: int) -> int:
    return (end_minutes - start_minutes - break_minutes)
