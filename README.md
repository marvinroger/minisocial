# MiniSocial

[![Build Status](https://travis-ci.org/marvinroger/minisocial.svg?branch=master)](https://travis-ci.org/marvinroger/minisocial)

A (very) simple microblogging platform.

## Get

`git clone https://github.com/marvinroger/minisocial.git`

## Configuration

* Create Google OAuth 2.0 credentials with the `Google+ API` enabled

* Create a `project/secrets.py` with the following variables:

```python
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<key>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<secret>'
```

## Bootstrap

`cd minisocial && docker-compose up`

Django will listen on port 8000.
