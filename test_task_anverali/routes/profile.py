from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_login import current_user

from test_task_anverali.libs.decorators import login_required
from test_task_anverali.libs.core import update_user, update_custom_fields, get_user_settings, change_space_type

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])
def profile():
    user = current_user.__dict__
    space_type = user.get('space_type')
    template = f"{space_type}_profile.html"
    try:
        return render_template(template,
                               user=user,
                               user_info=get_user_settings(current_user.id, space_type)), 200
    except Exception as e:
        flash('Something went wrong. Please, try again.', 'danger')
        return render_template('base.html'), 500


@profile_bp.route('/profile', methods=['POST'])
def change_role():
    change_space_type(current_user.id, current_user.space_type)
    return redirect(url_for('profile.profile')), 302


@profile_bp.route('/profile/update', methods=['POST'])
def update():
    try:
        user_id = current_user.id
        user_space_type = current_user.space_type
        update_custom_fields(
            user_id=user_id,
            space_type=user_space_type,
            experience=request.form.get('experience'),
            about=request.form.get('about')
        )
        flash('Profile has been updated successfully', 'success')
        redirect(url_for('profile.profile')), 302
    except Exception as e:
        flash('Something went wrong. Please, try again.', 'danger')
        return render_template('base.html'), 500
    return redirect(url_for('profile.profile')), 302
