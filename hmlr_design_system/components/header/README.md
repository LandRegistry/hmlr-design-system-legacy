# Header

Header suitable for external facing services, particularly those that need to fall in line with Portal styling.

## Todos:
- Tweak React component to accept Router links instead of just string hrefs for the homepage URL

## Jinja invocation
```
{{ header({
  'homepageUrl': '/'
}) }}
```

## React invocation

```
<Header homepageUrl='/' />
```
