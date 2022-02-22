from cachelib import FileSystemCache
from flask import request
from flask_compress import Compress

compress = Compress()


class GzipStaticAssets(object):
    """Gzip compression with Flask-Compress"""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        app.config.setdefault("COMPRESS_MIMETYPES", ["text/css", "application/javascript"])
        app.config.setdefault("COMPRESS_CACHE_BACKEND", gzip_cache)
        app.config.setdefault("COMPRESS_CACHE_KEY", gzip_cache_key)

        compress.init_app(app)


def gzip_cache():
    """Set up a caching system for the gzipped assets"""
    cache = FileSystemCache(cache_dir=".cache/gzip")
    cache.clear()
    return cache


def gzip_cache_key(response):
    """Gzip cache key"""
    return request.path + response.headers.get("ETag", "")
