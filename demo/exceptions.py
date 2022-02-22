from flask import current_app, jsonify, render_template, request
from jinja2 import TemplateNotFound
from werkzeug.exceptions import HTTPException, default_exceptions

from demo.utils.content_negotiation_utils import request_wants_json


class ApplicationError(Exception):
    """Use this class when the application identifies there's been a problem and the client should be informed.

    This should only be used for absolute edge case exceptions.
    As a matter of course, exceptions should be caught and dealt with higher up
    in the flow and users should be given a decent onward journey.

    Consider security issues when writing messages - what information might you
    be revealing to potential attackers?

    Example:
        raise ApplicationError('Friendly message here', 'E102', 400)
    """

    def __init__(self, message, code=None, http_code=500, force_logging=False):
        """Create an instance of the error.

        Keyword arguments:

        http_code - handler methods will use this to determine the http code to set in the returned Response
        (default 500)

        force_logging - handler methods will use this to determine whether to log at debug or info, when
        the http code being returned is not 500 (500s are always considered error-level worthy) (default False)
        """
        Exception.__init__(self)
        self.message = message
        self.http_code = http_code
        self.code = code
        self.force_logging = force_logging


def unhandled_exception(e):
    """Handler method for exceptions that escape the route code without being caught.

    A consistent error page is returned.

    Due to the lack of information available to provide to the user, and the fact there was clearly
    no opportunity for cleanup or error handling in the processing code, this should be a never-event!
    """

    current_app.logger.exception("Unhandled Exception: %s", repr(e))

    http_code = 500

    try:
        # Negotiate based on the Accept header
        if request_wants_json():
            return jsonify({}), http_code
        else:
            return (
                render_template(
                    "errors/unhandled.html",
                    http_code=http_code,
                ),
                http_code,
            )
    except Exception:
        # Ultimate fallback handler, such as if jinja templates are missing
        return "Internal server error", 500


def http_exception(e):
    current_app.logger.exception("HTTP Exception at %s:  %s", request.full_path, repr(e))

    # Restrict error codes to a subset so that we don't inadvertently expose
    # internal system information via error codes
    if isinstance(e, HTTPException) and e.code in [500, 404, 403, 429]:
        http_code = e.code
    else:
        http_code = 500

    # Negotiate based on the Accept header
    if request_wants_json():
        return jsonify({}), http_code
    else:
        return (
            render_template(
                "errors/unhandled.html",
                http_code=http_code,
            ),
            http_code,
        )


def application_error(e):
    """Handler method for ApplicationErrors raised for to inform the user of a specific scenario."""

    # Determine whether to log at info|error, when the http code being returned is not 500
    # (500s are always considered live-log worthy, at error level)
    if e.http_code == 500:
        current_app.logger.exception(
            "Application Exception (message: %s, code: %s): %s",
            e.message,
            e.code,
            repr(e),
        )
    elif e.force_logging:
        current_app.logger.info(
            "Application Exception (message: %s, code: %s): %s",
            e.message,
            e.code,
            repr(e),
            exc_info=True,
        )
    else:
        current_app.logger.debug(
            "Application Exception (message: %s, code: %s): %s",
            e.message,
            e.code,
            repr(e),
            exc_info=True,
        )

    # ApplicationError allows developers to specify an HTTP code.
    # This will be written to the logs correctly, but we don't want to allow
    # this code through to the user as it may expose internal workings of the system
    # (See OWASP guidelines on error handling)
    if e.http_code in [500, 404, 403, 429]:
        http_code = e.http_code
    else:
        http_code = 500

    if request_wants_json():
        return jsonify({"message": e.message, "code": e.code}), http_code
    else:
        try:
            return (
                render_template(
                    "errors/application/{}.html".format(e.code),
                    description=e.message,
                    code=e.code,
                    http_code=http_code,
                    e=e,
                ),
                http_code,
            )
        except TemplateNotFound:
            return (
                render_template(
                    "errors/application.html",
                    description=e.message,
                    code=e.code,
                    http_code=http_code,
                ),
                http_code,
            )


def register_exception_handlers(app):
    app.register_error_handler(ApplicationError, application_error)
    app.register_error_handler(Exception, unhandled_exception)

    # Register all default HTTP exceptions from werkzeug
    for exception in default_exceptions:
        app.register_error_handler(exception, http_exception)

    app.logger.info("Exception handlers registered")
