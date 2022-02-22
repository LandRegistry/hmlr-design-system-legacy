import gzip
import os
import unittest
from unittest import mock

from flask_compress import Compress
from werkzeug.datastructures import Headers

from demo.custom_extensions.gzip_static_assets.main import GzipStaticAssets, gzip_cache, gzip_cache_key
from demo.main import app


class TestGzipStaticAssets(unittest.TestCase):
    """These tests will only pass if STATIC_ASSETS_MODE is set to production. See unit_tests/__init__.py"""

    def setUp(self):
        self.client = app.test_client()

    @mock.patch("demo.custom_extensions.gzip_static_assets.main.GzipStaticAssets.init_app")
    def test_extension_alternative_init(self, mock_init_app):
        GzipStaticAssets("foo")
        mock_init_app.assert_called_once_with("foo")

    def test_setting_up_cache_directory(self):
        cache = gzip_cache()

        # Check that the directory exists
        self.assertTrue(os.path.exists(".cache/gzip"))

        # And that it's empty. Note - don't use os.listdir because the FileSystemCache actually stores
        # a count of the files in a file! So the number of files on disk will always be 1 more than the number
        # of cache entries that we might expect
        file_count = len(cache._list_dir())
        self.assertEqual(file_count, 0)

    def test_gzip_cache_key_format(self):
        with app.test_request_context("/foo?cachebuster=123"):
            response = mock.MagicMock(headers=Headers([("ETag", "bar")]))
            key = gzip_cache_key(response)

        self.assertEqual(key, "/foobar")

    def test_gzipped_response(self):
        # Create test file
        filename = "demo/assets/dist/gzip-test.css"
        file_contents = "* { content: 'Test. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip.'; }"  # noqa: E501
        with open(filename, "w+") as test_file:
            test_file.write(file_contents)

        response = self.client.get("/ui/gzip-test.css", headers=Headers([("Accept-encoding", "gzip")]))

        # Check the response reports itself as gzip
        self.assertEqual(response.content_encoding, "gzip")

        # And that we haven't just received the original contents
        self.assertNotEqual(response.data, file_contents)

        # Unzip it, check the contents is the same as the original
        self.assertEqual(gzip.decompress(response.data).decode("utf-8"), file_contents)

        response.close()
        os.remove(filename)

    def test_html_is_not_gzipped(self):
        response = self.client.get("/")

        self.assertIsNone(response.content_encoding)
        self.assertIn("<!DOCTYPE html>", response.data.decode("utf-8"))

    # @mock.patch.object(Compress, 'compress', wraps=Compress.compress)
    def test_repeated_requests_returns_cached_value(self):
        # Start with a clean cache
        cache = gzip_cache()
        cache.clear()

        # Create test file
        filename = "demo/assets/dist/gzip-test.css"
        file_contents = "* { content: 'Test. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip. Padded out to trigger gzip.'; }"  # noqa: E501
        with open(filename, "w+") as test_file:
            test_file.write(file_contents)

        compress_instance = Compress()
        with mock.patch.object(Compress, "compress", wraps=compress_instance.compress) as mock_compress:
            # Do a first request to get the gzipped response
            response = self.client.get("/ui/gzip-test.css", headers=Headers([("Accept-encoding", "gzip")]))

            # Check that flask-compress was invoked
            self.assertEqual(mock_compress.call_count, 1)

            # Check the response reports itself as gzip
            self.assertEqual(response.content_encoding, "gzip")

            response.close()

            # Do a second request to get the gzipped response
            response = self.client.get("/ui/gzip-test.css", headers=Headers([("Accept-encoding", "gzip")]))

            # Check that flask-compress was *not* invoked again
            self.assertEqual(mock_compress.call_count, 1)

            # Check the response reports itself as gzip
            self.assertEqual(response.content_encoding, "gzip")

            response.close()

        os.remove(filename)
