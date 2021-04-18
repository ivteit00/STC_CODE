# Standard libary imports
from datetime import datetime, timedelta, date
import time

# Third pary imports
from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user

# Local application imports
from .models import User, Vacation, Illness
from .functions import hr_role_required
from . import db


ill = Blueprint('ill', __name__)


@ill.route('/illness', methods=['GET', 'POST'])
@login_required
def illness():
    if request.method == 'POST':
        start_date = datetime.strptime(
            request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(
            request.form.get('end_date'), '%Y-%m-%d')
        if start_date > end_date:
            flash(
                'You selected a start date before your end date! Please try again.', category='danger')
            return redirect(url_for('ill.illness'))
        user = User.query.filter_by(
            id=session.get('user_id')).first()

        ill = Illness(start_date=start_date, end_date=end_date, user=user)
        db.session.add(ill)
        db.session.commit()
        flash('You successfully handed in your medical certificate.',
              category='success')
        return redirect(url_for('ill.illness'))
    return render_template('illness.html', user=current_user, roles_id=session.get('roles_id'))


@ill.route('/illness_cases', methods=['GET', 'POST'])
@login_required
@hr_role_required
def illness_cases():
    if request.method == 'POST':
        case_id = request.form.get('accept-button')
        case = Illness.query.filter_by(id=case_id).first()
        case.approved = True

        db.session.add(case)
        db.session.commit()
        return redirect(url_for('ill.illness_cases'))
    cases = Illness.query.all()
    return render_template('illness_cases.html', user=current_user, roles_id=session.get('roles_id'), cases=cases, User=User)
