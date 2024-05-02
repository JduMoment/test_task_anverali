import pytest

from test_task_anverali.libs.core import register_user
from test_task_anverali.models.user import User


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register(db_session):
    registration_data = {
        'email': 'test_user@example.com',
        'password': 'test_password1%',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890',
        'space_type': 'executor'
    }
    register_user(db_session, registration_data)
    user = db_session.query(User).filter_by(email=registration_data['email']).first()
    assert user is not None
    assert user.first_name == registration_data['first_name']
    assert user.last_name == registration_data['last_name']
    assert user.phone_number == registration_data['phone_number']


def test_register_invalid_data(client):
    registration_data = {
        'email': 'invalid_email',
        'password': 'short',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890'
    }
    response = client.post('/register', data=registration_data)
    assert response.status_code == 400


def test_login(db_session, client):
    registration_data = {
        'email': 'test_user@example.com',
        'password': 'test_password1%',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890',
        'space_type': 'executor'
    }
    register_user(db_session, registration_data)
    user = db_session.query(User).filter_by(email=registration_data['email']).first()
    assert User.check_pwd(user, 'test_password1%')


@pytest.mark.usefixtures('db_session')
def test_login_invalid_data(client):
    login_data = {
        'email': 'invalid_email',
        'password': 'short'
    }
    response = client.post('/login', data=login_data)
    assert response.status_code == 422
