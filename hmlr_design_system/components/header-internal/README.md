# Header

Header suitable for internal services.

## Todos:
- Tweak React component to accept Router links instead of just string hrefs for the homepage URL

## Jinja invocation

    {{ header({
      'homepageUrl': '/',  
      'headerTitle': 'Application processing',
      'inner': {   
        'classes': 'left-aligned'   
      }   
    }) }}   
 

Align the text of the header by adding 'left-aligned' or 'right-aligned' classes to the inner options. By default the header will align to the content of main column an a two column layout

## React invocation


    <Header homepageUrl='/', headerTitle='Application processing' />


## Full list of props/options

| Name   |      Type      |  Description |
|----------|:-------------:|------:|
| headerTitle |  String | **Required**. String to used as the site heading |
| homepageUrl |  String |  If set the header title will act as a link to the url specified |

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
