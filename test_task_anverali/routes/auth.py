import logging

import flask_login
from flask import render_template, flash, url_for, redirect, Blueprint, request
from flask_login import login_user
from marshmallow import ValidationError

from test_task_anverali.db import db_session
from test_task_anverali.models.user import User
from test_task_anverali.routes.schemas import LoginSchema

logger = logging.getLogger('opensearch')

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html'), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        validated_data = LoginSchema().load(request.form)
        email = validated_data['email']
        password = validated_data['password']
        with db_session() as session:
            user = session.query(User).filter_by(email=email).first()
            if user and user.check_pwd(password):
                login_user(user)
                flash('Вы вошли в аккаунт', 'success')
                return redirect(url_for('main.index')), 302
            flash('Неверный логин или пароль', 'danger')
            return render_template('login.html'), 200
    except ValidationError as e:
        if 'email' in e.messages:
            flash('Произошла ошибка проверки email', 'danger')
        if 'password' in e.messages:
            flash('Произошла ошибка проверки пароля', 'danger')
        return render_template('login.html'), 422

    except Exception as error:
        logger.error('Error during login: %s', error, exc_info=True)
        flash('Произошла ошибка во время входа', 'danger')
        return render_template('login.html'), 500


@auth_bp.post('/logout')
def logout():
    flask_login.logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('auth.login')), 302
