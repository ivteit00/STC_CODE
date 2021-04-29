# Standard libary imports
from datetime import datetime, timedelta, date
import time

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from workdays import networkdays

# Local application imports
from .models import User, Vacation, Illness, Notification
from . import db
from .functions import chef_or_hr_role_required, create_message


vac = Blueprint('vac', __name__)


@vac.route('/vacation', methods=['GET', 'POST'])
@login_required
def vacation() -> 'html':
    """View function for vacations"""
    # check if the http request is a POST request
    if request.method == 'POST':
        # query the database
        start_date = datetime.strptime(
            request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(
            request.form.get('end_date'), '%Y-%m-%d')
        dif = networkdays(start_date, end_date)
        user = User.query.filter_by(
            id=session.get('user_id')).first()
        vacation_days = user.vacation_days
        vacation_days_taken = user.vacation_days_taken
        vacation_days_available = vacation_days - vacation_days_taken
        # do some calculations in order to validate wether the vacation request is valid or not
        if start_date > end_date:
            flash(
                'You selected a start date before your end date! Please try again.', category='danger')
            return redirect(url_for('vac.vacation'))
        elif start_date.date() <= date.today():
            flash('You tried to create a vacation requests which starts at a passed date. Please try again.', category='danger')
            return redirect(url_for('vac.vacation'))
        else:
            if dif <= vacation_days_available:
                user = User.query.filter_by(id=session.get('user_id')).first()
                req = Vacation(start_date=start_date,
                               end_date=end_date, user=user)
                db.session.add(req)
                db.session.commit()
                # add the vacation request to the database
                flash('Successfully handed in your vacation request.',
                      category='success')
                return redirect(url_for('vac.vacation'))
            else:
                flash(
                    'You selected a period that exceeds your available vacation days!', category='danger')
                return redirect(url_for('vac.vacation'))
    # code executed if the http request is not a POST request
    # return the rendered template which the user can see
    user = User.query.filter_by(id=session.get('user_id')).first()
    requests = Vacation.query.filter_by(user_id=user.id).all()
    return (render_template('vacation.html', user=current_user, requests=requests, roles_id=session.get('roles_id')),
            200,
            {'location': '/vacation'})


@vac.route('/vacation_requests', methods=['GET', 'POST'])
@login_required
@chef_or_hr_role_required
def vacation_requests() -> 'html':
    """View function for all vacation-requests"""
    if request.method == 'POST':
        # check if the http request is a POST request
        if request.form.get('accept-button'):
            # check if the accept button was clicked in order to accept the vacation requet
            request_id = request.form.get('accept-button')
            req = Vacation.query.filter_by(id=request_id).first()
            req.approved = True
            req.notify = True
            user = User.query.filter_by(id=req.user_id).first()
            vacation_length = networkdays(req.start_date, req.end_date)
            user.vacation_days_taken += vacation_length

            db.session.add_all([req, user])
            db.session.commit()
            flash('You successfully accepted the Vacation Request.',
                  category='success')
            return redirect(url_for('vac.vacation_requests'))
        elif request.form.get('reject-button'):
            # check if the reject button was clicked in order to reject the vacation request
            request_id = request.form.get('reject-button')
            user_id = Vacation.query.filter_by(id=request_id).first().user_id
            user = User.query.filter_by(id=user_id).first()

            req = Vacation.query.filter_by(id=request_id).first()
            msg = create_message(req)
            noti = Notification(user=user, message=msg)
            db.session.add(noti)
            Vacation.query.filter_by(id=request_id).delete()
            db.session.commit()
            flash('You succesfully rejected the Vacation request. The employee is getting notified.', category='warning')
            return redirect(url_for('vac.vacation_requests'))

    # code executed if the http request is not a POST request
    # return the rendered template which the user can see
    requests = Vacation.query.all()
    users = User.query.all()
    return (render_template('vacation_requests.html', requests=requests, user=current_user,  users=users, User=User, roles_id=session.get('roles_id')),
            200,
            {'location': '/vacation_requests'})
