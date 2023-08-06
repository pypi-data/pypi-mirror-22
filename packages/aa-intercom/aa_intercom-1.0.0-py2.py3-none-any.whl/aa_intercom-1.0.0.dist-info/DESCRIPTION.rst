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

Another step is to provide own ``IntercomEvent`` model. Create a model which will inherit from
``aa_intercom.models.AbstractIntercomEvent``, and also implement the ``get_intercom_data()`` method (the returned value should depend on
event type). Sample ``IntercomEvent`` model (taken from **test_project/models.py**):

::

  class IntercomEvent(AbstractIntercomEvent):
    TYPE_EXAMPLE_EVENT = "example_event"
    TYPE_GENERIC = "generic"

    LABEL_EXAMPLE_EVENT = _("example event")
    LABEL_GENERIC = _("generic event")

    EVENT_TYPES = (
        (TYPE_EXAMPLE_EVENT, LABEL_EXAMPLE_EVENT),
        (TYPE_GENERIC, LABEL_GENERIC)
    )

    type = models.CharField(max_length=100, choices=EVENT_TYPES)

    def get_intercom_data(self):
        data = super(IntercomEvent, self).get_intercom_data()
        if self.type == IntercomEvent.TYPE_EXAMPLE_EVENT:
            data["metadata"] = {
                "text_content": self.text_content,
                # anything more you want
            }
        elif self.type in [
            IntercomEvent.TYPE_GENERIC,
            # some other types can be added
        ]:
            data["metadata"] = {
                "text_content": self.text_content,  # text, depending on the object
                # type of content (topic, session, what to do, etc)
                "type": self.content_type.name if self.content_type else "",
                "id": self.object_id if self.object_id else "",  # id of object from type
            }
        else:
            raise UnsupportedIntercomEventType

        return data

To make your custom models work properly, you need to connect all ``post_save`` signals, for example (in your models.py):
::

  from aa_intercom.signals import account_post_save, intercom_event_push_to_intercom_post_save
  from django.db.models.signals import post_save

  post_save.connect(account_post_save, sender=UserModel)
  post_save.connect(intercom_event_push_to_intercom_post_save, sender=IntercomEvent)

And then specify the event model name in settings, for example:

::

  INTERCOM_EVENT_MODEL = "test_project.IntercomEvent"

If you want to use the user last seen feature on Intercom, execute the following task right after the user logs in:
::

  from aa_intercom.tasks import push_account_last_seen_tasks
  push_account_last_seen_task.apply_async(args=[user.id], countdown=100)

Configuration
-------------
The last thing is to specify Intercom credentials in your settings file
::

  INTERCOM_API_ACCESS_TOKEN = "your access token"

Make sure, you have the ``CACHES`` set (see: `docs <https://docs.djangoproject.com/en/1.11/topics/cache/#setting-up-the-cache>`_),
and also as this app uses Celery_, you need to have it configured.

To provide id prefix for Intercom user id, set ``INTERCOM_ID_PREFIX`` to desired value.

Using the IntercomEvent model
-----------------------------
After you have created your own **IntercomEvent** model, you are able to send any kind of event data to the Intercom API
in a convenient way. All you need to do is to create an instance of **IntercomEvent** filled with desired data, for example:
::

  IntercomEvent.objects.create(
    user=request.user, type=IntercomEvent.TYPE_POST_ADDED, text_content=post.content,
    content_type=Post, object_id=post.id)

Then if you have set the ``post_save`` signal correctly, the event should be pushed to the Intercom API.

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

Django Admin
------------
If you wish to have an overview over the events, you can also add a Django admin model for your ``IntercomEvent`` model,
for example (taken from **test_project/admin.py**):
::

  class IntercomEventAdmin(admin.ModelAdmin):
      readonly_fields = ("id", "user", "type", "text_content", "created", "modified", "content_type", "object_id",
                         "content_object", "is_sent")

      list_display = ("id", "user", "type", "is_sent", "created")
      list_filter = ("id", "user", "type", "is_sent")

      def has_add_permission(self, request):
          return False

  admin.site.register(IntercomEvent, IntercomEventAdmin)

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


