from flask import redirect, render_template, abort
from flask_admin import BaseView
from flask_login import current_user


class AccessMixin(BaseView):
    _redirect_url = "/login"

    def is_accessible(self):
        roles = ['admin']

        roles += getattr(self.__class__, '_add_roles', [])
        roles = list(set(roles))

        if not current_user.is_authenticated:
            return False

        if not current_user.has_one_of_role(roles):
            return abort(403)

        return True

    def inaccessible_callback(self, *_, **__):
        return redirect(self._redirect_url)
