import hashlib

from flask import Blueprint, render_template, redirect, url_for, request, flash
from marshmallow import ValidationError

from test_task_anverali.libs.core import add_user
from test_task_anverali.routes.schemas import RegisterSchema

user_bp = Blueprint('users', __name__)


@user_bp.route('/register', methods=['GET'])
def show_registration_form():
    """Display the registration form.
    ---
    get:
        description: Show registration form.
        responses:
            200:
                description: Render the registration template.
    """
    return render_template('registration.html'), 200


@user_bp.route('/register', methods=['POST'])
def register():
    """Registration form and processing.
    ---
    post:
        description: Process registration data.
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
              description: The user's password that must include at least one number and has a minimum length of 6 characters.
        responses:
            302:
                description: Redirect to login page if registration successful.
            400:
                description: Render registration form with error message if registration fails.
    """
    try:
        user_data = request.form
        schema = RegisterSchema()
        validated_data = schema.load(user_data)

        password = validated_data.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        args = {**request.form, 'password': hashed_password}
        add_user(**args)
        flash('Registration has been completed successfully', 'success')
        return redirect(url_for('auth.login')), 302
    except ValidationError as e:
        if 'email' in e.messages:
            flash('Email validation failed', 'danger')
        if 'password' in e.messages:
            flash('Password validation failed', 'danger')
        return render_template('registration.html', errors=e.messages), 400
    except Exception as error:
        flash('Something went wrong', 'danger')
        return render_template('base.html', errors=error), 500

