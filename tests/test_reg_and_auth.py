import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from test_task_anverali.db import ModelBase
from test_task_anverali.routes import app
from test_task_anverali.models.user import User

engine = create_engine('postgresql+psycopg2://postgres:pass@localhost:5432/test')

Session = sessionmaker(bind=engine)


@pytest.fixture(scope='module')
def db_session():
    with Session() as session:
        yield session


@pytest.fixture(scope='module')
def client():
    app.testing = True
    ModelBase.metadata.create_all(engine)
    with app.test_client() as client:
        yield client
    ModelBase.metadata.drop_all(engine)


@pytest.mark.usefixtures('db_session')
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.usefixtures('db_session')
def test_register(client):
    registration_data = {
        'email': 'test_user@example.com',
        'password': 'test_password1%',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890',
        'space_type': 'executor'
    }
    response = client.post('/register', data=registration_data)
    assert response.status_code == 302
    with Session() as session:
        user = session.query(User).filter_by(email=registration_data['email']).first()
        assert user is not None
        assert user.first_name == registration_data['first_name']
        assert user.last_name == registration_data['last_name']
        assert user.phone_number == registration_data['phone_number']


@pytest.mark.usefixtures('db_session')
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


@pytest.mark.usefixtures('db_session')
def test_login(client):
    registration_data = {
        'email': 'test_user@example.com',
        'password': 'test_password1%',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890',
        'space_type': 'executor'
    }
    client.post('/register', data=registration_data)
    login_data = {
        'email': 'test_user@example.com',
        'password': 'test_password1%'
    }
    response = client.post('/login', data=login_data)
    assert response.status_code == 302
    assert response.headers['Location'] == '/'


@pytest.mark.usefixtures('db_session')
def test_login_invalid_data(client):
    login_data = {
        'email': 'invalid_email',
        'password': 'short'
    }
    response = client.post('/login', data=login_data)
    assert response.status_code == 422
