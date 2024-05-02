from flask_admin.contrib.sqla import ModelView

from test_task_anverali.admin.mixins import AccessMixin
from test_task_anverali.models import UserRole
from test_task_anverali.models.roles import Role


class RoleView(AccessMixin, ModelView):

    def __init__(self, session):
        super().__init__(
            Role,
            session,
            name='Role Settings',
            category='User Data'
        )


class UserRoleView(AccessMixin, ModelView):

    column_list = ('user', 'role')

    def __init__(self, session):
        super().__init__(
            UserRole,
            session,
            name='UserRole Settings',
            category='User Data'
        )

