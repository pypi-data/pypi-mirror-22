===========
aa-intercom
===========
|travis|_ |pypi|_ |coveralls|_ |requiresio|_

Django integration for Intercom_ API

Installation
============

To use you need to add ``aa_intercom`` to your ``INSTALLED_APPS``, and then migrate the project.

Setting up user model
---------------------
**aa-intercom** requires a few fields in the user model to be set. To make it work, you need to apply the ``aa_intercom.mixins.IntercomUserMixin`` to your custom user model (if you do not have your own custom user model set, check the `documentation <https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#specifying-a-custom-user-model>`_).

Configuration
-------------
The last thing is to specify Intercom credentials

::

  INTERCOM_APP_ID = "app id"
  INTERCOM_ID_PREFIX = ""
  INTERCOM_API_ACCESS_TOKEN = "your access key"

Make sure, you have the ``CACHES`` set (see: `docs <https://docs.djangoproject.com/en/1.11/topics/cache/#setting-up-the-cache>`_),
and also as this app uses Celery_, you need to have it configured.

Commands
========
**aa-intercom** provides a few useful management commands, which should be run chronically:

* ``resend_intercom_events`` - resends all events in case something went wrong
* ``update_intercom_users`` - push all users to the Intercom API

Support
=======
* Django 1.11
* Python 2.7, 3.6

.. |travis| image:: https://secure.travis-ci.org/ArabellaTech/aa-intercom.svg
.. _travis: http://travis-ci.org/ArabellaTech/aa-intercom

.. |pypi| image:: https://img.shields.io/pypi/v/aa-intercom.svg
.. _pypi: https://pypi.python.org/pypi/aa-intercom

.. |coveralls| image:: https://coveralls.io/repos/github/ArabellaTech/aa-intercom/badge.svg
.. _coveralls: https://coveralls.io/github/ArabellaTech/aa-intercom

.. |requiresio| image:: https://requires.io/github/ArabellaTech/aa-intercom/requirements.svg
.. _requiresio: https://requires.io/github/ArabellaTech/aa-intercom/requirements/

.. _Intercom: http://intercom.com

.. _Celery: http://www.celeryproject.org/


