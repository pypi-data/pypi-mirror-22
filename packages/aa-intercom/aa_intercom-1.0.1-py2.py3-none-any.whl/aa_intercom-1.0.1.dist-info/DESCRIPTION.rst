===========
aa-intercom
===========
|travis|_ |pypi|_ |coveralls|_ |requiresio|_

Django integration for Intercom_ API

The **aa-intercom** package allows to

* upload user data to Intercom including the last seen feature
* push data to the Intercom API according to any event happening in your app

Installation
============
To use, add ``aa_intercom`` to your ``INSTALLED_APPS``, and then migrate the project.

Setting up models
-----------------
**aa-intercom** requires a few fields in the user model to be set. To make it work, you need to apply the
``aa_intercom.mixins.IntercomUserMixin`` to your custom user model (if you do not have your own custom user model set,
check the `documentation <https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#specifying-a-custom-user-model>`_).
The ``IntercomUserMixin.get_intercom_data()`` method can be overloaded to change the default user data sent to the Intercom API.

If you want to use the user last seen feature on Intercom, execute the following task right after the user logs in:
::

  from aa_intercom.tasks import push_account_last_seen_tasks
  push_account_last_seen_task.apply_async(args=[user.id], countdown=100)

Configuration
-------------
Another step is to add event types to project settings, for example:
::

  INTERCOM_EVENT_TYPES = (
    ("example", _("Example Type")),
    ("generic", _("Generic Type"))
  )

The last thing is to specify Intercom credentials in project settings:
::

  INTERCOM_API_ACCESS_TOKEN = "your access token"

Make sure, you have the ``CACHES`` set (see: `docs <https://docs.djangoproject.com/en/1.11/topics/cache/#setting-up-the-cache>`_),
and also as this app uses Celery_, you need to have it configured.

To provide id prefix for Intercom user id, set ``INTERCOM_ID_PREFIX`` to desired value.

Using the IntercomEvent model
-----------------------------
If you want to send any kind of event data to the Intercom API, create an instance of **IntercomEvent** filled with
desired information, for example:
::

  IntercomEvent.objects.create(
    user=request.user, type="generic", text_content=post.content,
    content_type=ContentType.objects.get_for_model(Post), object_id=post.id)

Then it will be automatically sent to the Intercom API. Unfortunately Intercom API has a tendency to go down often,
therefore to make sure all events will be sent, setup a cronjob running the ``resend_intercom_events`` command
which will push all remaining IntercomEvent objects to the API.

Sending unregistered user data
------------------------------
In case an upload of unregistered user data is needed, the ``aa_intercom.tasks.push_not_registered_user_data_task`` task
can be used (**email** and **name** keys are required), for example:
::

  push_not_registered_user_data_task.apply_async(args=[{
    "email": "test@arabel.la",
    "name": "Foo Bar",
    "pseudonym": "foobar"
  }])


Commands
========
* ``resend_intercom_events`` - resends all events (in case something went wrong, should be run chronically)

Support
=======
* Django 1.11
* Python 2.7, 3.6

.. |travis| image:: https://secure.travis-ci.org/ArabellaTech/aa-intercom.svg?branch=master
.. _travis: http://travis-ci.org/ArabellaTech/aa-intercom

.. |pypi| image:: https://img.shields.io/pypi/v/aa-intercom.svg
.. _pypi: https://pypi.python.org/pypi/aa-intercom

.. |coveralls| image:: https://coveralls.io/repos/github/ArabellaTech/aa-intercom/badge.svg?branch=master
.. _coveralls: https://coveralls.io/github/ArabellaTech/aa-intercom

.. |requiresio| image:: https://requires.io/github/ArabellaTech/aa-intercom/requirements.svg?branch=master
.. _requiresio: https://requires.io/github/ArabellaTech/aa-intercom/requirements/

.. _Intercom: http://intercom.com

.. _Celery: http://www.celeryproject.org/


