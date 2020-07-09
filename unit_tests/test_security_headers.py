import unittest
from unittest import mock

from demo.custom_extensions.security_headers.main import SecurityHeaders
from demo.main import app


class TestSecurityHeaders(unittest.TestCase):

    def setup_method(self, method):
        self.app = app.test_client()

    @mock.patch('demo.custom_extensions.security_headers.main.SecurityHeaders.init_app')
    def test_extension_alternative_init(self, mock_init_app):
        SecurityHeaders('foo')
        mock_init_app.assert_called_once_with('foo')

    def test_headers_present(self):
        response = self.app.get('/')

        expected_headers = [
            'X-Frame-Options',
            'Strict-Transport-Security',
            'X-XSS-Protection',
            'X-Content-Type-Options'
        ]

        for header in expected_headers:
            self.assertIn(header, response.headers)
