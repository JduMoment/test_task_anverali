from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from test_task_anverali.admin.views.admin_index import AdminHomeView
from test_task_anverali.admin.views.role import RoleView, UserRoleView
from test_task_anverali.admin.views.user import UserView
from test_task_anverali.conf import config
from test_task_anverali.db import Session
from test_task_anverali.models.user import User
from test_task_anverali.routes.auth import auth_bp
from test_task_anverali.routes.home import main_bp
from test_task_anverali.routes.user import user_bp
from test_task_anverali.routes.profile import profile_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

admin = Admin(
    app,
    name='freelance',
    index_view=AdminHomeView(),
)

admin.add_view(RoleView(Session()))
admin.add_view(UserRoleView(Session()))
admin.add_view(UserView(Session()))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):
    return Session().query(User).get(id)


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(profile_bp)
