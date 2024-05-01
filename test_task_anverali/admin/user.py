from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from flask_login import current_user
from flask import redirect, url_for

from test_task_anverali.libs.core import is_admin


from test_task_anverali.models.user import UserRole


class InlineRoleModelForm(InlineFormAdmin):
    form_label = 'Roles'

    def __init__(self):
        super(InlineRoleModelForm, self).__init__(UserRole)


class UsersView(ModelView):
    column_hide_backrefs = False
    column_list = ('email', 'active', 'roles')


class CustomAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and is_admin(current_user.id)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.show_login_form'))

