import bcrypt

from test_task_anverali.db import Session
from test_task_anverali.models.user import User
from test_task_anverali.models.users_customer_settings import UserCustomerSettings
from test_task_anverali.models.users_executor_settings import UserExecutorsSettings


def add_user(db_session: Session, **kwargs):
    user = User(**kwargs)
    db_session.add(user)
    db_session.flush()
    if user.space_type == 'executor':
        user_settings = UserExecutorsSettings(user_id=user.id)
    else:
        user_settings = UserCustomerSettings(user_id=user.id)
    db_session.add(user_settings)


def update_user(db_session: Session, user_id, **kwargs):
    user = db_session.query(User).filter_by(id=user_id).first()
    if not user:
        return

    for key, value in kwargs.items():
        setattr(user, key, value)


def change_space_type(db_session: Session, user_id, space_type):
    settings_class = UserCustomerSettings if space_type == 'executor' else UserExecutorsSettings
    existence_check = db_session.query(settings_class.user_id).filter_by(user_id=user_id).one_or_none()
    if existence_check is None:
        user_settings = settings_class(user_id=user_id)
        db_session.add(user_settings)
    update_user(db_session, user_id, space_type='customer' if space_type == 'executor' else 'executor')


def update_custom_fields(db_session: Session, user_id, space_type, experience=None, about=None):
    table_for_update = UserExecutorsSettings if space_type == 'executor' else UserCustomerSettings
    user = db_session.query(table_for_update).filter_by(user_id=user_id).first()
    user.experience = experience
    user.about_me = about
    db_session.commit()


def get_user_settings(db_session: Session, user_id, space_type):
    if space_type == 'executor':
        return db_session.query(UserExecutorsSettings.about_me, UserExecutorsSettings.experience).filter_by(user_id=user_id).first()
    elif space_type == 'customer':
        return db_session.query(UserCustomerSettings.about_me).filter_by(user_id=user_id).first()


def register_user(db_session, user_data):
    password = user_data.get('password')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    del user_data['password']

    add_user(
        db_session,
        **{**user_data, 'hash_password': hashed_password.decode(), 'salt': salt.decode()},
    )
