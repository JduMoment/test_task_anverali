import os

from test_task_anverali.db import db_session
from test_task_anverali.models.user import User, UserRole
from test_task_anverali.models.roles import Role
from test_task_anverali.models.users_customer_settings import UserCustomerSettings
from test_task_anverali.models.user_executor_settings import UserExecutorsSettings


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
            if kwargs.get('space_type') == 'executor':
                user_settings = UserExecutorsSettings(user_id=user.id)
            elif kwargs.get('space_type') == 'customer':
                user_settings = UserCustomerSettings(user_id=user.id)
            session.add(user_settings)
        session.commit()


def update_custom_fields(user_id, space_type, experience=None, about=None):
    with db_session() as session:
        if space_type == 'executor':
            user = session.query(UserExecutorsSettings).filter_by(user_id=user_id).first()
        elif space_type == 'customer':
            user = session.query(UserCustomerSettings).filter_by(user_id=user_id).first()
        user.experience = experience
        user.about_me = about
        session.commit()
        return user


def get_user_settings(user_id, space_type):
    with db_session() as session:
        if space_type == 'executor':
            about = session.query(UserExecutorsSettings.about_me, UserExecutorsSettings.experience).filter_by(user_id=user_id).first()
        elif space_type == 'customer':
            about = session.query(UserCustomerSettings.about_me).filter_by(user_id=user_id).first()
            experience = None
    return dict(about=about, experience=experience)
