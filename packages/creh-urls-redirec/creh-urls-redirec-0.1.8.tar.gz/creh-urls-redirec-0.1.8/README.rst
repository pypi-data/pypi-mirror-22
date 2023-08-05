=====
Creh Urls
=====

Creh-urls is a simple Django app redirect inactive urls in web page.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. creh-urls can be obtained directly from PyPI, and can be installed with pip:

    pip install creh-urls

1. Add "urls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'urls',
        ...
    ]

2. Run "python manage.py migrate" to create the log models.

3. Use

    MIDDLEWARE_CLASSES = (
    ...
    'urls.middleware.UrlRedirectMiddleware',
    ...
    )