# Header

Header suitable for internal services.

## Todos:
- Tweak React component to accept Router links instead of just string hrefs for the homepage URL

## Jinja invocation

    {{ headerInternal({
      'homepageUrl': '/',
      'headerTitle': 'Application processing'
    }) }}


## React invocation

    <HeaderInternal homepageUrl='/', headerTitle='Application processing' />


## Full list of props/options

| Name   |      Type      |  Description |
|----------|:-------------:|------:|
| headerTitle |  String | **Required**. String to used as the site heading |
| homepageUrl |  String |  If set the header title will act as a link to the url specified |

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
