# Header

## Todos:
- Tweak React component to accept Router links instead of just string hrefs for the homepage URL

## Jinja invocation

    {% from 'components/header/macro.html' import header %}
    
    {{ header({
      'homepageUrl': '/'
    }) }}


## React invocation

    <Header homepageUrl='/' />

