# Footer

Footer suitable for external facing services, particularly those that need to fall in line with Portal styling. Default footer will be positioned absolutely at the bottom of the page. To overide this behaviour add 'hmlr-footer--static' to classes.

## Jinja invocation

    {% from 'components/footer/macro.html' import footer %}

    {{ footer({
      'classes': 'hmlr-footer--static',
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


    <Footer classes='hmlr-footer--static'>
      <a href='#'>Terms and conditions</a>
      <a href='#'>Accessibility statement</a>
      <Link to='wherever'>
    </Footer>

