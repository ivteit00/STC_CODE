from datetime import date, datetime, timedelta
from functools import wraps
from .models import User, Role
from flask import url_for, redirect, flash
from flask_login import current_user


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


def hr_role_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.roles_id == 3 or current_user.roles_id == '3':
            return func(*args, **kwargs)
        return redirect(url_for('views.home'))
    return wrapper


def chef_role_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.roles_id == 2 or current_user. roles_id == '2':
            return func(*args, **kwargs)
        return redirect(url_for('views.home'))
    return wrapper


def chef_or_hr_role_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.roles_id == 3 or current_user.roles_id == '3':
            return func(*args, **kwargs)
        if current_user.roles_id == 2 or current_user. roles_id == '2':
            return func(*args, **kwargs)
        return redirect(url_for('views.home'))
    return wrapper
