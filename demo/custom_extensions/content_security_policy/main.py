from flask import g, url_for
from flask.wrappers import Response

from demo.custom_extensions.content_security_policy import reporting


class ContentSecurityPolicy(object):
    """Content security policy

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
        https://www.owasp.org/index.php/Content_Security_Policy_Cheat_Sheet
        https://content-security-policy.com/
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Default config
        app.config.setdefault("CONTENT_SECURITY_POLICY_MODE", "full")

        # Build up the content security policy header
        self.csp = (
            "default-src 'self';"
            "script-src 'self' www.google-analytics.com %(govuk_script_hashes)s;"
            "connect-src 'self' www.google-analytics.com;"
            "img-src 'self' www.google-analytics.com;"
            "font-src 'self' data:;"  # GOV.UK template loads it's fonts with a data URI
            "block-all-mixed-content;"
            # "require-sri-for script style;"  # Desirable, but disabled until browsers implement this
            "report-uri %(report_uri)s;"
        )

        # sha hashes for govuk script tags
        # If the script blocks in the govuk template are changed, these will
        # need to be updated. Easiest way is to delete these hashes, and then
        # pull the new ones from Chrome's dev console (It calculates them for you)
        govuk_script_hashes = [
            "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
            "'sha256-G29/qSW/JHHANtFhlrZVDZW1HOkCDRc78ggbqwwIJ2g='",
        ]

        # Register a blueprint containing a simple route to log CSP violations
        app.register_blueprint(reporting.reporting, url_prefix="/content-security-policy-report/")

        try:
            # If we've got flask_wtf's CSRF protection enabled, we need to exempt the reporting blueprint
            csrf = app.extensions["csrf"]
        except KeyError:
            # If the CSRF extension isn't enabled just carry on
            pass
        else:
            csrf.exempt(reporting.reporting)

        @app.after_request
        def after_request(response):
            if isinstance(response, ResponseWithoutCSP):
                return response

            csp = self.csp % {
                "report_uri": url_for("reporting.report", trace_id=g.trace_id),
                "govuk_script_hashes": " ".join(govuk_script_hashes),
            }

            if app.config["CONTENT_SECURITY_POLICY_MODE"] == "report-only":
                response.headers["Content-Security-Policy-Report-Only"] = csp
            else:
                response.headers["Content-Security-Policy"] = csp

            return response


class ResponseWithoutCSP(Response):
    """Return this type of Response from your views if you want to withhold the CSP

    Uses cases for this so far include:
        - Withholding CSP from views which return a PDF. When Chrome renders these it puts them in an html page
          which violates the CSP

    NOTE:
    The CSP is here for a reason, don't withhold it just because it makes development easier
    (e.g. using inline styles etc)
    """
