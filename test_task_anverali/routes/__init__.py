import os

import sentry_sdk
from flasgger import Swagger
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from test_task_anverali.conf import config
from test_task_anverali.db import Session
from test_task_anverali.models.user import User, UserRole
from test_task_anverali.models.roles import Role
from test_task_anverali.routes.auth import auth_bp
from test_task_anverali.routes.home import main_bp
from test_task_anverali.routes.user import user_bp
from test_task_anverali.routes.profile import profile_bp
from test_task_anverali.admin.user import CustomAdminView


app = Flask(__name__)

swagger = Swagger(app, template={
    'swagger': '2.0',
    'info': {
        'title': 'Freelance',
        'version': '1.0',
        'description': 'Freelance service'
    },
    'basePath': '/',
    'schemes': ['http']
})
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='freelance', template_mode='bootstrap4')
admin.add_view(CustomAdminView(User, Session()))
admin.add_view(CustomAdminView(Role, Session()))
admin.add_view(CustomAdminView(UserRole, Session()))


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):
    return Session().query(User).get(id)


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(profile_bp)
