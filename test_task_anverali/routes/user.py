import logging

from flask import Blueprint, render_template, redirect, url_for, request, flash
from marshmallow import ValidationError

from test_task_anverali.db import db_session
from test_task_anverali.libs.db_requests import register_user
from test_task_anverali.routes.schemas import RegisterSchema

logger = logging.getLogger('opensearch')

user_bp = Blueprint('users', __name__)


@user_bp.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('registration.html'), 200


@user_bp.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.form
        schema = RegisterSchema()
        validated_data = schema.load(user_data)

        with db_session() as session:
            register_user(session, validated_data)
        flash('Регистрация прошла успешно', 'success')
        return redirect(url_for('auth.login')), 302
    except ValidationError as e:
        if 'email' in e.messages:
            flash('Некорректная почта', 'danger')
        if 'password' in e.messages:
            flash('Некорректный пароль', 'danger')
        return render_template('registration.html', errors=e.messages), 400
    except Exception as error:
        logger.error('Error during registration %s', error, exc_info=True)
        flash('Что-то пошло не так. Пожалуйста, попробуйте еще раз', 'danger')
        return render_template('base.html', errors=error), 500
