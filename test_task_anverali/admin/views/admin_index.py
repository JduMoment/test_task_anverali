from flask_admin import AdminIndexView

from test_task_anverali.admin.mixins import AccessMixin


class AdminHomeView(AccessMixin, AdminIndexView):
    pass
