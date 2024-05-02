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
    """Display the login form.
    ---
    get:
        description: Show login form.
        responses:
            200:
                description: Render the login template.
    """
    return render_template('login.html'), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login form and processing.
    ---
    post:
        description: Process login data.
        consumes:
            - application/x-www-form-urlencoded
        parameters:
            - in: formData
              name: email
              type: string
              required: true
              description: The user's email address.
            - in: formData
              name: password
              type: string
              required: true
              description: The user's password.
        responses:
            302:
                description: Redirect to home page if successful.
            200:
                description: Render login form with error message if login fails.
            422:
                description: Data validation failed.
    """
    try:
        validated_data = LoginSchema().load(request.form)
        email = validated_data['email']
        password = validated_data['password']
        with db_session() as session:
            user = session.query(User).filter_by(email=email).first()
            if user and user.check_pwd(password):
                login_user(user)
                flash('Login successful', 'success')
                return redirect(url_for('main.index')), 302
    except ValidationError as e:
        if 'email' in e.messages:
            flash('Email validation failed', 'danger')
        if 'password' in e.messages:
            flash('Password validation failed', 'danger')
        return render_template('login.html'), 422

    except Exception as error:
        logger.error('Error during login: %s', error, exc_info=True)
        flash('Data validation failed', 'danger')
        return render_template('login.html'), 500


@auth_bp.post('/logout')
def logout():
    flask_login.logout_user()
    flash('You have logged out of your account', 'success')
    return redirect(url_for('auth.login')), 302

