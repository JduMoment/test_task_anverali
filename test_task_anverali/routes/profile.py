from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_login import current_user
import logging

from test_task_anverali.db import db_session
from test_task_anverali.libs.auth import login_required_page
from test_task_anverali.libs.db_requests import update_custom_fields, get_user_settings, change_space_type


logger = logging.getLogger('opensearch')

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])
@login_required_page
def profile():
    with db_session() as session:
        user = current_user.__dict__
        space_type = user.get('space_type')
        template = f"{space_type}_profile.html"
        try:
            return render_template(template,
                                   user=user,
                                   user_info=get_user_settings(session, user_id=current_user.id, space_type=space_type)), 200
        except Exception as error:
            logger.error('Error while getting user profile data: %s', error, exc_info=True)
            flash('Something went wrong. Please, try again.', 'danger')
            return render_template('base.html'), 500


@profile_bp.route('/profile', methods=['POST'])
def change_role():
    with db_session() as session:
        change_space_type(session, current_user.id, current_user.space_type)
    return redirect(url_for('profile.profile')), 302


@profile_bp.route('/profile/update', methods=['POST'])
def update_profile():
    try:
        user_id = current_user.id
        user_space_type = current_user.space_type
        with db_session() as session:
            update_custom_fields(
                db_session=session,
                user_id=user_id,
                space_type=user_space_type,
                experience=request.form.get('experience'),
                about=request.form.get('about')
            )
        flash('Profile has been updated successfully', 'success')
        redirect(url_for('profile.profile')), 302
    except Exception as error:
        logger.error('Error while getting user profile data: %s', error, exc_info=True)
        flash('Something went wrong. Please, try again.', 'danger')
        return render_template('base.html'), 500
    return redirect(url_for('profile.profile')), 302
