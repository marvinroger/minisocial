# MiniSocial

A (very) simple microblogging platform.

## Configuration

* Create Google OAuth 2.0 credentials with the `Google+ API` enabled

* Create a `project/secrets.py` with the following variables:

```python
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<key>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<secret>'
```

## Bootstrap

`docker build --name minisocial . && docker run -p 80:80 minisocial`
