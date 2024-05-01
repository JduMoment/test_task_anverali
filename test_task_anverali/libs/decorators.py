from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Вы должны войти в аккаунт', 'danger'), 403
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_function


