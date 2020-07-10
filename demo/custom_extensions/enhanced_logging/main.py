import uuid
from pathlib import Path

import requests
from flask import g, request

from flask_logconfig import LogConfig


def before_request():
    # Sets the transaction trace id on the global object if provided in the HTTP header from the caller.
    # Generate a new one if it has not. We will use this in log messages.
    g.trace_id = request.headers.get("X-Trace-ID", uuid.uuid4().hex)
    # We also create a session-level requests object for the app to use with the header pre-set, so other APIs
    # will receive it. These lines can be removed if the app will not make requests to other LR APIs!
    g.requests = requests.Session()
    g.requests.headers.update({"X-Trace-ID": g.trace_id})


class EnhancedLogging(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Ensure that the traceid is parsed/propagated on every request
        app.before_request(before_request)

        # Let's get the app's base package name so we can set the correct formatter, filter and logger names
        app_module_name = Path(__file__).resolve().parents[2].parts[-1]

        logconfig = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {"()": app_module_name + ".custom_extensions.enhanced_logging.formatters.JsonFormatter"},
                "content_security_policy": {
                    "()": app_module_name + ".custom_extensions.enhanced_logging"
                    ".formatters.ContentSecurityPolicyFormatter"
                },
            },
            "filters": {
                "contextual": {"()": app_module_name + ".custom_extensions.enhanced_logging.filters.ContextualFilter"}
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "filters": ["contextual"],
                    "stream": "ext://sys.stdout",
                },
                "content_security_policy": {
                    "class": "logging.StreamHandler",
                    "formatter": "content_security_policy",
                    "filters": ["contextual"],
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                app.logger.name: {"handlers": ["console"], "level": app.config["FLASK_LOG_LEVEL"], },
                "content_security_policy": {
                    "handlers": ["content_security_policy"],
                    "level": app.config["FLASK_LOG_LEVEL"],
                },
            },
        }

        app.config.update(LOGCONFIG=logconfig)

        logger = LogConfig()

        logger.init_app(app)
