from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_login import current_user

from test_task_anverali.libs.decorators import login_required
from test_task_anverali.libs.core import update_user, update_custom_fields, get_user_settings

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = current_user.__dict__
    user_info = get_user_settings(current_user.id, current_user.space_type)
    if user.get('space_type') == 'executor':
        return render_template('executor_profile.html',
                               user=user,
                               user_info=user_info), 200
    elif user.get('space_type') == 'customer':
        return render_template('customer_profile.html',
                               user=user,
                               user_info=user_info), 200
    else:
        flash('Something went wrong. Please, try again.', 'danger')
        return render_template('base.html'), 500


@profile_bp.route('/profile', methods=['POST'])
@login_required
def change_role():
    user = current_user.space_type
    if user == 'executor':
        update_user(current_user.id, space_type='customer')
    elif user == 'customer':
        update_user(current_user.id, space_type='executor')
    return redirect(url_for('profile.profile')), 302


@profile_bp.route('/profile/update', methods=['POST'])
def update():
    try:
        user_id = current_user.id
        user_space_type = current_user.space_type
        user_data = request.form
        update_custom_fields(
            user_id=user_id,
            space_type=user_space_type,
            experience=user_data.get('experience'),
            about=user_data.get('about_me')
        )
        flash('Profile has been updated successfully', 'success')
        redirect(url_for('profile.profile')), 302
    except Exception as e:
        flash('Something went wrong. Please, try again.', 'danger')
        return render_template('base.html'), 500
    return redirect(url_for('profile.profile')), 302