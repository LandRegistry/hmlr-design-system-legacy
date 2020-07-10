import json
import unittest
from unittest import mock

from demo.custom_extensions.content_security_policy.main import ContentSecurityPolicy, ResponseWithoutCSP
from demo.main import app


class TestContentSecurityPolicy(unittest.TestCase):
    def setup_method(self, method):
        self.app = app.test_client()

    @mock.patch("demo.custom_extensions.content_security_policy.main.ContentSecurityPolicy.init_app")
    def test_extension_alternative_init(self, mock_init_app):
        ContentSecurityPolicy("foo")
        mock_init_app.assert_called_once_with("foo")

    def test_reporting_mode(self):
        app.config["CONTENT_SECURITY_POLICY_MODE"] = "report-only"

        response = self.app.get("/")
        self.assertIn("script-src", response.headers["Content-Security-Policy-Report-Only"])

    def test_full_mode(self):
        app.config["CONTENT_SECURITY_POLICY_MODE"] = "full"

        response = self.app.get("/")
        self.assertIn("script-src", response.headers["Content-Security-Policy"])

    @mock.patch("demo.custom_extensions.content_security_policy.reporting.logger.error")
    def test_report_route(self, mock_logger):
        response = self.app.post(
            "/content-security-policy-report/?trace_id=Hello",
            data=json.dumps({"csp-report": {"foo": "bar"}}),
            content_type="application/json",
        )

        mock_logger.assert_called_once_with("CSP violation", extra={"content_security_policy_report": {"foo": "bar"}})

        self.assertEqual(response.status_code, 204)

    def test_exemptions(self):
        with app.test_request_context("/"):
            app.preprocess_request()

            response = ResponseWithoutCSP(response="Foo")
            response = app.process_response(response)

            self.assertNotIn("Content-Security-Policy", response.headers)
