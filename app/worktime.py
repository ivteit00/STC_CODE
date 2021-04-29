# Standard libary imports
from datetime import datetime, timedelta, date
import time

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from workdays import networkdays


# Local application imports
from .models import User, Vacation, Illness
from .functions import chef_role_required
from . import db


work = Blueprint('worktime', __name__)


@work.route('/worktime', methods=['GET', 'POST'])
@login_required
def worktime() -> 'html':
    """view function for worktime view"""
    if request.method == 'POST':
        # check wether the http request was a POST request
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

        # do some calculations in order to validate the worktime
        if start_minutes > end_minutes:
            error = True
        if break_minutes < 0:
            error = True

        if calculate_worktime_minutes(start_minutes=start_minutes, end_minutes=end_minutes, break_minutes=break_minutes) < 0:
            error = True
        if break_minutes < 30:
            flash('Your break time is to low. Please resubmit your Worktime later and take a longer break :) ',
                  category='warning')
            return redirect(url_for('worktime.worktime'))
        if error:
            flash('You have entered invalid values. Please check your input.',
                  category='danger')
            return redirect(url_for('worktime.worktime'))
        else:
            # upload the worktime for the user
            user = User.query.filter_by(id=session.get('user_id')).first()
            worked_hours = (end_minutes-start_minutes-break_minutes) / 60

            user.worked_hours += worked_hours
            db.session.add(user)
            db.session.commit()
            flash('You have successfully uploaded your worktime. Enjoy your day!',
                  category='success')
            return redirect(url_for('worktime.worktime'))

    # code executed if the http request is not a POST request
    # return the rendered template which the user can see

    return (render_template('worktime.html', user=current_user, roles_id=session.get('roles_id')),
            200,
            {'location': '/worktime'})


@work.route('/approve_worktime', methods=['GET', 'POST'])
@chef_role_required
@login_required
def approve_worktime() -> 'html':
    """viewfunction for worktime approval"""
    if request.method == 'POST':
        if request.form.get('accept-button'):
            user_id = request.form.get('accept-button')
            user = User.query.filter_by(id=user_id).first()
            user_full_name = user.full_name
            user.worked_hours_approved = True
            user.notify = True
            db.session.add(user)
            db.session.commit()
            flash(('You successfully approved the worked hours of ' +
                  user_full_name), category='success')
            return redirect(url_for('worktime.approve_worktime'))
        elif request.form.get('reject-button'):
            user_id = request.form.get('reject-button')
            user = User.query.filter_by(id=user_id).first()
            user_full_name = user.full_name
            flash(('You rejected the worktime of ' + user_full_name +
                  '. She/He will be notified.'), category='warning')

    # code executed if the http request is not a POST request
    # return the rendered template which the user can see

    users = User.query.all()
    today = date.today()
    first_date = date.today().replace(day=1)
    hours_till_today = networkdays(first_date, today) * 8
    return (render_template('approve_worktime.html',
                            user=current_user,
                            roles_id=session.get('roles_id'),
                            users=users,
                            User=User,
                            hours_till_today=hours_till_today),
            200,
            {'location': '/approve_worktime'}
            )


def calculate_minutes(time: datetime.time) -> int:
    """function to calculate datetime.time in minutes"""
    return (time.hour*60 + time.minute)


def calculate_worktime_minutes(start_minutes: int, end_minutes: int, break_minutes: int) -> int:
    """function to calculate worktime per day"""
    return (end_minutes - start_minutes - break_minutes)
