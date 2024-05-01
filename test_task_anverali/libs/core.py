import os

from test_task_anverali.db import db_session
from test_task_anverali.models.user import User, UserRole
from test_task_anverali.models.roles import Role
from test_task_anverali.models.users_customer_settings import UserCustomerSettings
from test_task_anverali.models.users_executor_settings import UserExecutorsSettings


DATABASE_URL = os.getenv('DATABASE_URL')


def add_user(**kwargs):
    with db_session() as session:
        user = User(**kwargs)
        session.add(user)
        session.flush()
        if user.space_type == 'executor':
            user_settings = UserExecutorsSettings(user_id=user.id)
        elif user.space_type == 'customer':
            user_settings = UserCustomerSettings(user_id=user.id)
        session.add(user_settings)
        session.commit()


def get_user_roles(user_id):
    with db_session() as session:
        user_roles_query = session.query(Role.name).join(UserRole).filter(UserRole.user_id == user_id)
        return [role.name for role in user_roles_query]


def is_admin(user_id):
    return 'admin' in get_user_roles(user_id)


def update_user(user_id, **kwargs):
    with db_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
        session.commit()


def change_space_type(user_id, space_type):
    with db_session() as session:
        settings_class = UserCustomerSettings if space_type == 'executor' else UserExecutorsSettings
        existence_check = session.query(settings_class.user_id).filter_by(user_id=user_id).one_or_none()
        if existence_check is None:
            user_settings = settings_class(user_id=user_id)
            session.add(user_settings)
        update_user(user_id, space_type='customer' if space_type == 'executor' else 'executor')
        session.commit()


def update_custom_fields(user_id, space_type, experience=None, about=None):
    table_for_update = UserExecutorsSettings if space_type == 'executor' else UserCustomerSettings
    with db_session() as session:
        user = session.query(table_for_update).filter_by(user_id=user_id).first()
        user.experience = experience
        user.about_me = about
        session.commit()


def get_user_settings(user_id, space_type):
    with db_session() as session:
        if space_type == 'executor':
            info = session.query(UserExecutorsSettings.about_me, UserExecutorsSettings.experience).filter_by(user_id=user_id).first()
        elif space_type == 'customer':
            info = session.query(UserCustomerSettings.about_me).filter_by(user_id=user_id).first()
    return info
