import misaka
from jinja2 import Markup
from demo.custom_extensions.jinja_markdown_filter.gov_renderer import GovRenderer


class JinjaMarkdownFilter(object):
    """Markdown filter for Jinja templates"""
    render_markdown = misaka.Markdown(GovRenderer(), extensions=('autolink',))

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.filters['markdown'] = self.markdown_filter(app)

    def markdown_filter(self, app):
        def render(value):
            return Markup(self.render_markdown(value))

        return render
