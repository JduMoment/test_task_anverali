from flask_admin.contrib.sqla import ModelView

from test_task_anverali.admin.mixins import AccessMixin
from test_task_anverali.models.user import User


class UserView(AccessMixin, ModelView):

    def __init__(self, session):
        super().__init__(
            User,
            session,
            name='User Settings',
            category='User Data'
        )
