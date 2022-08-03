"""
User decorators
"""
from functools import wraps

from flask import current_app, flash, redirect, request, url_for
from flask_login import config, current_user


def admin_required(func):
    """User must be an admin for get access to the particular page
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        if current_app.config.get("LOGIN_DISABLED"):
            return func(*args, **kwargs)
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        if not current_user.is_admin:
            flash("Эта страница доступна только админам")
            return redirect(url_for("index"))
        return func(*args, **kwargs)

    return decorated_view
