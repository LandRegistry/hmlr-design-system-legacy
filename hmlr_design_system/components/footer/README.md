# Footer

Footer suitable for external facing services, particularly those that need to fall in line with Portal styling.

## Jinja invocation
    {% from 'components/footer/macro.html' import footer %}
    
    {{ footer({
      'meta': {
        'items': [
          {
            'text': 'Terms and conditions',
            'href': '#'
          },
          {
            'text': 'Accessibility statement',
            'href': '#'
          }
        ]
      }
    }) }}


## React invocation

Links should be passed as children. Note that the component accepts regular links as well as react-router Link elements or similar.


    <Footer>
      <a href='#'>Terms and conditions</a>
      <a href='#'>Accessibility statement</a>
      <Link to='wherever'>
    </Footer>

