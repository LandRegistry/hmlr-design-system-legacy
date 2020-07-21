class SecurityHeaders(object):
    """Set some security related headers

    See https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#tab=Headers
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        app.config.setdefault("X_FRAME_OPTIONS", "DENY")
        app.config.setdefault("STRICT_TRANSPORT_SECURITY", "max-age=31536000")  # 1 year
        app.config.setdefault("X_XSS_PROTECTION", "1; mode=block")
        app.config.setdefault("X_CONTENT_TYPE_OPTIONS", "nosniff")
        app.config.setdefault("REFERRER_POLICY", "no-referrer-when-downgrade")

        @app.after_request
        def security_headers(response):
            response.headers["X-Frame-Options"] = app.config.get("X_FRAME_OPTIONS")
            response.headers["Strict-Transport-Security"] = app.config.get("STRICT_TRANSPORT_SECURITY")
            response.headers["X-XSS-Protection"] = app.config.get("X_XSS_PROTECTION")
            response.headers["X-Content-Type-Options"] = app.config.get("X_CONTENT_TYPE_OPTIONS")
            response.headers["Referrer-Policy"] = app.config.get("REFERRER_POLICY")

            return response
