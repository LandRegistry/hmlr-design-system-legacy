import os
import unittest
from unittest import mock

from flask import render_template_string
from freezegun import freeze_time

from demo.custom_extensions.cachebust_static_assets.main import CachebustStaticAssets, md5_for_file
from demo.main import app


class TestCachebustStaticAssets(unittest.TestCase):
    """These tests will only pass if STATIC_ASSETS_MODE is set to production. See unit_tests/__init__.py"""

    def setUp(self):
        self.app = app.test_client()

    @mock.patch("demo.custom_extensions.cachebust_static_assets.main.CachebustStaticAssets.init_app")
    def test_extension_alternative_init(self, mock_init_app):
        CachebustStaticAssets("foo")
        mock_init_app.assert_called_once_with("foo")

    def test_md5_for_file_generates_same_value_repeatedly(self):
        hash_one = md5_for_file("./README.md")
        hash_two = md5_for_file("./README.md")
        hash_three = md5_for_file("./README.md")
        self.assertEqual(hash_one, hash_two)
        self.assertEqual(hash_two, hash_three)

    def test_md5_for_different_files_generate_different_hashes(self):
        hash_one = md5_for_file("./README.md")
        hash_two = md5_for_file("./Dockerfile")
        self.assertNotEqual(hash_one, hash_two)

    def test_md5_for_file_generates_different_value_when_file_is_changed(self):
        filename = "./test_md5_for_file_generates_different_value_when_file_is_changed.txt"
        with open(filename, "w+") as file:
            file.write("Hello")
        hash_one = md5_for_file(filename)

        with open(filename, "a") as file:
            file.write(" World")

        hash_two = md5_for_file(filename)
        self.assertNotEqual(hash_one, hash_two)

        os.remove(filename)

    def test_url_for_adds_cache_query_string(self):
        filename = "demo/assets/dist/test.txt"
        with open(filename, "w+") as file:
            file.write("Hello")

        with app.test_request_context("/"):
            output = render_template_string("{{ url_for('static', filename='test.txt') }}")

        md5_value = md5_for_file(filename, hexdigest=True)

        self.assertIn("?cache={}".format(md5_value), output)

        os.remove(filename)

    @mock.patch(
        "demo.custom_extensions.cachebust_static_assets.main.md5_for_file",
        wraps=md5_for_file,
    )
    def test_repeated_url_for_calls_hits_cache_not_disk(self, mock_md5_for_file):
        filename = "demo/assets/dist/test.txt"
        with open(filename, "w+") as file:
            file.write("Hello")

        with app.test_request_context("/"):
            hash_one = render_template_string("{{ url_for('static', filename='test.txt') }}")
            hash_two = render_template_string("{{ url_for('static', filename='test.txt') }}")
            hash_three = render_template_string("{{ url_for('static', filename='test.txt') }}")

            self.assertEqual(mock_md5_for_file.call_count, 1)

        self.assertEqual(hash_one, hash_two)
        self.assertEqual(hash_two, hash_three)

        os.remove(filename)

    def test_hashed_url_for_only_runs_for_static_asset_routes(self):
        with app.test_request_context("/"):
            output = render_template_string("{{ url_for('components.index') }}")

        self.assertNotIn("?cache", output)

    @freeze_time("2017-01-18")
    def test_far_future_expiry_headers_for_css_file(self):
        filename = "demo/assets/dist/test.css"
        with open(filename, "w+") as file:
            file.write("Hello")

        response = self.app.get("/ui/test.css")

        expires = response.headers.get("Expires")
        self.assertEqual(expires, "Mon, 18 Jan 2027 10:12:00 GMT")

        response.close()

        os.remove(filename)

    @freeze_time("2017-01-18")
    def test_far_future_expiry_headers_for_txt_file(self):
        filename = "demo/assets/dist/test.txt"
        with open(filename, "w+") as file:
            file.write("Hello")

        response = self.app.get("/ui/test.txt")

        expires = response.headers.get("Expires")
        self.assertEqual(expires, "Wed, 18 Jan 2017 12:00:00 GMT")

        response.close()

        os.remove(filename)
