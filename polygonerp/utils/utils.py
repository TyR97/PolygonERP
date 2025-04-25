import functools
from flask import g, redirect, url_for

"""
Authentication decorators for access control.
"""
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.is_admin:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view






