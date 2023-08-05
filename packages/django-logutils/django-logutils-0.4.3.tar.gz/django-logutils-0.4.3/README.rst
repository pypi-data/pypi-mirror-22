=============================
django-logutils
=============================

.. image:: https://badge.fury.io/py/django-logutils.png
    :target: https://badge.fury.io/py/django-logutils

.. image:: https://travis-ci.org/jsmits/django-logutils.png?branch=master
    :target: https://travis-ci.org/jsmits/django-logutils

.. image:: https://readthedocs.org/projects/django-logutils/badge/?version=latest
    :target: https://readthedocs.org/projects/django-logutils/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/jsmits/django-logutils/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/jsmits/django-logutils?branch=master

Various logging-related utilities for Django projects. For now, it provides
a LoggingMiddleware class and an EventLogger class.

Documentation
-------------

http://django-logutils.readthedocs.org

Quickstart
----------

Install django-logutils::

    pip install django-logutils

LoggingMiddleware
-----------------

LoggingMiddleware is middleware class for Django, that logs extra
request-related information. To use it in your Django projects, add it to
your ``MIDDLEWARE_CLASSES`` setting::

    MIDDLEWARE_CLASSES = (
        ...
        'django_logutils.middleware.LoggingMiddleware',
        ...
    )

The extra information consists of:

- event (default: 'request')

- remote ip address: the remote ip address of the user doing the request.

- user email: the email address of the requesting user, if available

- request method: post or get

- request url path

- response status code

- content length of the response body

- request time

N.B.: event can be overriden by using the ``LOGUTILS_LOGGING_MIDDLEWARE_EVENT``
setting in your project.

The log message itself is a string composed of the remote ip address, the user
email, the request method, the request url, the status code, the content
length of the body and the request time. Additionally, a dictionary with the
log items are added as an extra keyword argument when sending a logging
statement.

If settings.DEBUG is True or the request time is more than 1 second, two
additional parameters are added to the logging dictionary: ``nr_queries`` that
represents the number of queries executed during the request-response cycle
and ``sql_time`` that represents the time it took to execute those queries.
Slow requests are also raised to a loglevel of ``WARNING``.

N.B.: the time threshold for slow requests can be overriden by using the
``LOGUTILS_REQUEST_TIME_THRESHOLD`` setting in your project.

EventLogger
-----------

The EventLogger class makes it easy to create dictionary-based logging
statements, that can be used by log processors like Logstash. Log events can be
used to track metrics and/or to create visualisations.

Here's an example of how you can use it::

    >>> from django_logutils.utils import EventLogger
    >>> log_event = EventLogger('my_logger')
    >>> log_event('my_event', {'action': 'push_button'})

Development
-----------

Install the test requirements::

    $ pip install -r requirements/test.txt

Run the tests to check everything is fine::

    $ make test

To run the tests and opening the coverage html in your browser::

    $ make coverage

To run flake8 and pylint, do::

    $ make lint

To generate the documentation, do::

    $ make docs
