Django Foundation Formtags
==========================

.. image:: https://travis-ci.org/chrisdev/django-foundation-formtags.svg?branch=master
    :target: https://travis-ci.org/chrisdev/django-foundation-formtags

.. image:: https://pyup.io/repos/github/chrisdev/django-foundation-formtags/shield.svg
     :target: https://pyup.io/repos/github/chrisdev/django-foundation-formtags/
     :alt: Updates

Django template tags to work with Zurb Foundation forms


Getting Started
---------------

Create a virtualenv::

    $ virtualenv my-env

At the command line::

    $ pip install django-foundation-formtags


Usage
-----

To start use django-foundation-forms in a project you must include in your settings::

    INSTALLED_APPS = (
        'foundation_formtags',
    )

In the template load foundation tags by::

    {% load foundation_formtags %}

To use the django-form-foundation filter::

    <form class="form" action="{{ url }}" method="POST">
        {% csrf_token %}
        {{ form|as_foundation }}
    </form>

To use the django-form-foundation field tags::

    <form class="form" action="{{ url }}" method="POST">
        {% csrf_token %}
        {% render_field form.name %}

        {% render_field form.subject %}

        {% render_field form.message %}
    </form>


Contributing
------------

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.


* Free software: BSD license
* Documentation: https://django-foundation-formtags.readthedocs.org.



History
========

0.0.8 (2017-05-09)
-------------------

* Make it Compatible with Django 1.11

0.0.7 (2016-09-25)
-------------------

* Make Compatible with Django 1.10
* Minimum version is now Django 1.8. For earlier versions of Django use 0.0.6

0.0.6 (2016-08-05)
------------------

Fix for checkbox rendering and New error class for Non field errors in Foundation 6 

0.0.5 (2016-07-12)
---------------------

* First release on PyPI.


