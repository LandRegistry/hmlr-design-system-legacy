import misaka


class GovRenderer(misaka.HtmlRenderer):
    def paragraph(self, content):
        return '<p class="govuk-body">{0}</p>'.format(content)

    def link(self, content, link, title):
        return '<a class="govuk-link" href="{0}"{1}>{2}</a>'.format(
            link, ' title="{}"'.format(title) if title else "", content
        )

    def header(self, content, level):
        """Custom renderer to map Markdown heading levels to gov.uk heading classes

        See https://github.com/hoedown/hoedown/blob/master/src/html.c for reference
        on what methods are available to override
        """
        heading_levels = {
            1: "govuk-heading-xl",
            2: "govuk-heading-l",
            3: "govuk-heading-m",
            4: "govuk-heading-s",
            5: "govuk-heading-s",
            6: "govuk-heading-s",
        }

        return '<h{0} class="{1}">{2}</h{0}>'.format(level, heading_levels.get(level), content)

    def list(self, content, is_ordered, is_block):
        """Custom renderer to output lists with the gov.uk classes"""
        return '<{0} class="govuk-list govuk-list--{1}">{2}</{0}>'.format(
            "ol" if is_ordered else "ul", "number" if is_ordered else "bullet", content
        )

    def hrule(self):
        return '<hr class="govuk-section-break govuk-section-break--xl govuk-section-break--visible">'
