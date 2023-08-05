django-jsonsuit
===============

|image| |image| |image|

Django goodies to dress JSON data in a suit.

Documentation
-------------

The full documentation is at https://tooreht.github.io/django-jsonsuit.

Quickstart
----------

Install django-jsonsuit:

::

    pip install django-jsonsuit

Add it to your ``INSTALLED_APPS``:

.. code:: sourcecode

    INSTALLED_APPS = (
        ...
        'jsonsuit.apps.JSONSuitConfig',
        ...
    )

Usage
-----

In a form or model admin, enable a JSON suit for a particular field:

.. code:: python

    from jsonsuit.widgets import JSONSuit

    class JSONForm(forms.ModelForm):
      class Meta:
        model = Test
        fields = '__all__'
        widgets = {
          'myjsonfield': JSONSuit(),
        }

    class JSONAdmin(admin.ModelAdmin):
      form = JSONForm

Enable JSON suit for every JSONField of a model:

.. code:: python

    from django.contrib.postgres.fields import JSONField

    class JSONAdmin(admin.ModelAdmin):
      formfield_overrides = {
        JSONField: {'widget': JSONSuit }
      }

Features
--------

-  TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Project dependencies:

-  `prism <http://prismjs.com/>`__
-  `vanilla-js <http://vanilla-js.com/>`__

Project documentation:

-  `MkDocs <http://www.mkdocs.org/>`__

Tools used in rendering this package:

-  `Cookiecutter <https://github.com/audreyr/cookiecutter>`__
-  `cookiecutter-djangopackage <https://github.com/pydanny/cookiecutter-djangopackage>`__

.. |image| image:: https://badge.fury.io/py/django-jsonsuit.svg
.. |image| image:: https://travis-ci.org/tooreht/django-jsonsuit.svg?branch=master
.. |image| image:: https://codecov.io/gh/tooreht/django-jsonsuit/branch/master/graph/badge.svg



History
-------

Version 0.1.0 (2017-05-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  First release on PyPI.


