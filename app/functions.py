from datetime import date, datetime, timedelta
from functools import wraps
from .models import User, Role
from flask import url_for, redirect, flash
from flask_login import current_user

from .models import Vacation


def hr_role_required(func):
    """Wrapper to restrict access only for hr role"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check if the user has the hr role
        if current_user.roles_id == 3 or current_user.roles_id == '3':
            return func(*args, **kwargs)
        return redirect(url_for('views.home'))
    return wrapper


def chef_role_required(func):
    """Wrapper to restrict access only for chef role"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check if the user has the chef role
        if current_user.roles_id == 2 or current_user. roles_id == '2':
            return func(*args, **kwargs)
        return redirect(url_for('views.home'))
    return wrapper


def chef_or_hr_role_required(func):
    """Wrapper to restrict access only for chef and hr role"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check if the user has the chef or hr role
        if current_user.roles_id == 3 or current_user.roles_id == '3':
            return func(*args, **kwargs)
        if current_user.roles_id == 2 or current_user. roles_id == '2':
            return func(*args, **kwargs)
        return redirect(url_for('views.home'))
    return wrapper


def create_message(req: Vacation) -> str:
    """Function that creates individual vacation message."""
    start_date = req.start_date
    end_date = req.end_date
    message = "Your vacation request start date: %s, end date: %s has been rejected. Please contact your supervisor for more details." % (
        start_date, end_date)
    return message
