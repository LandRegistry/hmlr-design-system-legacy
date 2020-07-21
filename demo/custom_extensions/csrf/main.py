from flask import flash, redirect, request

from flask_wtf.csrf import CSRFError, CSRFProtect

csrf = CSRFProtect()


class CSRF(object):
    """Thin wrapper around Flask CSRF

    Set some defaults for the flask-wtf csrf protection and
    handle the CSRFError exception more gracefully
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Default to only expiring the token when the user's session expires
        # rather than 1 hour which is the default from flask-wtf
        app.config.setdefault("WTF_CSRF_TIME_LIMIT", None)

        global csrf
        csrf.init_app(app)

        app.register_error_handler(CSRFError, handle_csrf_error)


def handle_csrf_error(e):
    flash("The form you were submitting has expired. Please try again.", "error")
    return redirect(request.path)
