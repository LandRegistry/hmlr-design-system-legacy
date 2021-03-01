import unittest
from unittest import mock

from flask import render_template_string

from demo.custom_extensions.jinja_markdown_filter.main import JinjaMarkdownFilter
from demo.main import app


class TestJinjaMarkdownFilter(unittest.TestCase):
    def setup_method(self, method):
        self.app = app.test_client()

    def check_rendering(self, markdown_to_html):
        for markdown in markdown_to_html:
            with app.test_request_context("/"):
                assert render_template_string(
                    "{{contents|markdown}}", contents=markdown
                ).strip() == markdown_to_html.get(markdown)

    @mock.patch("demo.custom_extensions.jinja_markdown_filter.main.JinjaMarkdownFilter.init_app")
    def test_extension_alternative_init(self, mock_init_app):
        JinjaMarkdownFilter("foo")
        mock_init_app.assert_called_once_with("foo")

    def test_render_returns_govuk_html_for_headings(self):
        markdown_to_html = {
            "# 1": '<h1 class="govuk-heading-xl">1</h1>',
            "## 2": '<h2 class="govuk-heading-l">2</h2>',
            "### 3": '<h3 class="govuk-heading-m">3</h3>',
            "#### 4": '<h4 class="govuk-heading-s">4</h4>',
            "##### 5": '<h5 class="govuk-heading-s">5</h5>',
            "###### 6": '<h6 class="govuk-heading-s">6</h6>',
        }

        self.check_rendering(markdown_to_html)

    def test_render_returns_govuk_html_for_lists(self):
        markdown_to_html = {
            "- Foo\n- Bar\n- Wibble": '<ul class="govuk-list govuk-list--bullet">'
            "<li>Foo</li>\n<li>Bar</li>\n<li>Wibble</li>\n</ul>",
            "1. Foo\n2. Bar\n3. Wibble": '<ol class="govuk-list govuk-list--number">'
            "<li>Foo</li>\n<li>Bar</li>\n<li>Wibble</li>\n</ol>",
        }

        self.check_rendering(markdown_to_html)

    def test_render_returns_govuk_html_for_hrule(self):
        markdown_to_html = {
            "---": '<hr class="govuk-section-break govuk-section-break--xl govuk-section-break--visible">',
        }

        self.check_rendering(markdown_to_html)

    def test_render_returns_govuk_html_for_paragraph(self):
        markdown_to_html = {
            "Foo\n\nBar\n\nWibble": '<p class="govuk-body">Foo</p><p class="govuk-body">Bar</p><p class="govuk-body">Wibble</p>',
        }

        self.check_rendering(markdown_to_html)

    def test_render_returns_govuk_html_for_link(self):
        markdown_to_html = {
            "[Foo](http://foo.com)": '<p class="govuk-body"><a class="govuk-link" href="http://foo.com">Foo</a></p>',
            '[Foo](http://foo.com "Title here")': '<p class="govuk-body"><a class="govuk-link" href="http://foo.com" title="Title here">Foo</a></p>',
        }

        self.check_rendering(markdown_to_html)
