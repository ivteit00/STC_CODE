from datetime import date, datetime, timedelta
from functools import wraps
from .models import User, Role
from flask import url_for, redirect, flash
from flask_login import current_user


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
