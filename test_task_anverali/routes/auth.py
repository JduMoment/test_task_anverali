import hashlib

import flask_login
from flask import render_template, flash, url_for, redirect, Blueprint, request
from flask_login import login_user

from test_task_anverali.db import db_session
from test_task_anverali.models.user import User

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
        email = request.form['email']
        password = request.form['password']
        with db_session() as session:
            user = session.query(User).filter_by(email=email).first()
            if user and user.password == hashlib.sha256(password.encode()).hexdigest():
                login_user(user)
                flash('Login successful', 'success')
                return redirect(url_for('main.index')), 302
            else:
                flash('Invalid email or password', 'danger')
                return render_template('login.html'), 400
    except Exception as error:
        flash('Data validation failed', 'danger')
        return render_template('login.html'), 400


@auth_bp.post('/logout')
def logout():
    flask_login.logout_user()
    flash('You have logged out of your account', 'success')
    return redirect(url_for('auth.login')), 302

