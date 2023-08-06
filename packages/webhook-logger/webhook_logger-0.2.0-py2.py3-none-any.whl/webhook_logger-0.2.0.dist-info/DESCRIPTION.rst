=====================
Python Webhook Logger
=====================

.. image:: https://img.shields.io/pypi/v/webhook-logger.svg
    :target: https://pypi.python.org/pypi/webhook-logger

.. image:: https://img.shields.io/travis/founders4schools/python-webhook-logger.svg
    :target: https://travis-ci.org/founders4schools/python-webhook-logger

.. image:: https://readthedocs.org/projects/python-webhook-logger/badge/?version=latest
    :target: https://python-webhook-logger.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/founders4schools/python-webhook-logger/shield.svg
    :target: https://pyup.io/repos/github/founders4schools/python-webhook-logger/
    :alt: Updates

.. image:: https://codecov.io/gh/founders4schools/python-webhook-logger/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/founders4schools/python-webhook-logger


A Python logging toolbox to send logs over Webhooks.


* Free software: MIT license
* Documentation: https://python-webhook-logger.readthedocs.io.


Features
--------

* Framework agnostic, just tied to Python logging module
* Integration with Django supported
* Optional filtering feature to only submit some logs
* Styling of Slack messages depending on the logging level
* Uses requests under the hood to make it testable

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.2.0 (2017-05-22)
------------------

* Added docs
* The color Formatter is now optional

0.1.2 (2017-05-18)
------------------

* First release on PyPI with Slack logging features


