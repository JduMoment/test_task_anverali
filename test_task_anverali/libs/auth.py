from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user


def login_required_page(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Вы должны войти в аккаунт', 'danger')
            return redirect(url_for('auth.login')), 301
        return f(*args, **kwargs)

    return decorated_function
