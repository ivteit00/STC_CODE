# Standard libary imports
from datetime import datetime, timedelta, date
import time

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user

# Local application imports
from .models import User, Vacation, Illness
from . import db


views = Blueprint('views', __name__)

# MA-home-viewfunction


@views.route('/home')
@login_required
def home():
    user = User.query.filter_by(id=session.get('user_id')).first()
    today = date.today()
    first_date = date.today().replace(day=1)
    hours_till_today = get_workdays(first_date, today) * 8
    requests = Vacation.query.filter_by(user_id=user.id).all()
    return render_template('home.html', full_name=session.get('full_name'), user=current_user, roles_id=session.get('roles_id'), user_data=user, hours_till_today=hours_till_today, requests=requests)


"""@views.route('/worktime', methods=['GET', 'POST'])
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
        if start_time > end_time or break_time < datetime.time(0) or worktime_in_minutes < 0:
        flash('You have entered invalid values. Please check your input.',
              category='danger')
        return redirect(url_for('views.worktime'))

        user = User.query.filter_by(id=session.get('user_id')).first()
        user.worked_hours = user.worked_hours + worktime_in_hours
        db.session.add(user)
        db.session.commit()
        flash('You successfully uploaded your worked hours.', category='success')
        return redirect(url_for('views.worktime'))

    return render_template('worktime.html', user=current_user, roles_id=session.get('roles_id'))
"""
"""
@views.route('/vacation', methods=['GET', 'POST'])
@login_required
def vacation():
    if request.method == 'POST':
        start_date = datetime.strptime(
            request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(
            request.form.get('end_date'), '%Y-%m-%d')
        dif = get_workdays(start_date, end_date)
        user = User.query.filter_by(
            id=session.get('user_id')).first()
        vacation_days = user.vacation_days
        vacation_days_taken = user.vacation_days_taken
        vacation_days_available = vacation_days - vacation_days_taken
        if start_date > end_date:
            flash(
                'You selected a start date before your end date! Please try again.', category='danger')
            return redirect(url_for('views.vacation'))
        else:
            if dif <= vacation_days_available:
                user = User.query.filter_by(id=session.get('user_id')).first()
                req = Vacation(start_date=start_date,
                               end_date=end_date, user=user)
                db.session.add(req)
                db.session.commit()
                flash('Successfully handed in your vacation request.',
                      category='success')
                return redirect(url_for('views.vacation'))
            else:
                flash(
                    'You selected a period that exceeds your available vacation days!', category='danger')
                return redirect(url_for('views.vacation'))
    user = User.query.filter_by(id=session.get('user_id')).first()
    requests = Vacation.query.filter_by(user_id=user.id).all()
    return render_template('vacation.html', user=current_user, requests=requests, roles_id=session.get('roles_id'))
"""

"""
@views.route('/vacation_requests', methods=['GET', 'POST'])
@login_required
def vacation_requests():
    if request.method == 'POST':
        if request.form.get('accept-button'):
            request_id = request.form.get('accept-button')
            req = Vacation.query.filter_by(id=request_id).first()
            req.approved = True
            db.session.add(req)
            db.session.commit()
            flash('You successfully accepted the Vacation Request.',
                  category='success')
            return redirect(url_for('views.vacation_requests'))
        elif request.form.get('reject-button'):
            request_id = request.form.get('reject-button')
            Vacation.query.filter_by(id=request_id).delete()
            db.session.commit()
            flash('You succesfully rejected the Vacation request. The employee is getting notified.', category='warning')
            return redirect(url_for('views.vacation_requests'))

    requests = Vacation.query.all()
    users = User.query.all()
    return render_template('vacation_requests.html', requests=requests, user=current_user,  users=users, User=User, roles_id=session.get('roles_id'))
"""
"""
@views.route('/illness', methods=['GET', 'POST'])
@login_required
def illness():
    if request.method == 'POST':
        start_date = datetime.strptime(
            request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(
            request.form.get('end_date'), '%Y-%m-%d')
        user = User.query.filter_by(
            id=session.get('user_id')).first()

        ill = Illness(start_date=start_date, end_date=end_date, user=user)
        db.session.add(ill)
        db.session.commit()
        flash('You successfully handed in your medical certificate.',
              category='success')
    return render_template('illness.html', user=current_user, roles_id=session.get('roles_id'))
"""

"""
@views.route('/illness_cases', methods=['GET', 'POST'])
@login_required
def illness_cases():
    if request.method == 'POST':
        case_id = request.form.get('accept-button')
        case = Illness.query.filter_by(id=case_id).first()
        case.approved = True
        db.session.add(case)
        db.session.commit()
    cases = Illness.query.all()
    return render_template('illness_cases.html', user=current_user, roles_id=session.get('roles_id'), cases=cases, User=User)
"""


def get_workdays(from_date: datetime, to_date: datetime):
    # if the start date is on a weekend, forward the date to next Monday
    if from_date.weekday() > 4:
        from_date = from_date + timedelta(days=7 - from_date.weekday())
    # if the end date is on a weekend, rewind the date to the previous Friday
    if to_date.weekday() > 4:
        to_date = to_date - timedelta(days=to_date.weekday() - 4)
    if from_date > to_date:
        return 0
    # that makes the difference easy, no remainders etc
    diff_days = (to_date - from_date).days + 1
    weeks = int(diff_days / 7)
    return weeks * 5 + (to_date.weekday() - from_date.weekday()) + 1
