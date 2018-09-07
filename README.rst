=============================
acdh-django-sirad
=============================

.. image:: https://badge.fury.io/py/acdh-django-sirad.svg
    :target: https://badge.fury.io/py/acdh-django-sirad

parse a SIARD-ARCHIV and generates a django-app out of it. Also imports the data from the SIARD-ARCHIV_ into your django app.


Quickstart
----------

Install django_charts::

    pip install acdh-django-sirad

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'sirad',
        ...
    )

unzip your SIARD-ARCHIV into a folder called 'legacy_data' located in your application's root directory.

Then run `python manage.py start_sirad_app <name_of_your_app>`

This will create - like django's default `startapp` command a new application called <name_of_your_app>.

Register your new app in `INSTALLED_APPS`

To import the data from your SIARD-ARCHIV run `python manage.py populate_sirad app <name_of_your_app>`


Be aware the the created app was build to work within djangobaseproject_

.. _SIARD-ARCHIV: http://www.eark-project.com/resources/specificationdocs/32-specification-for-siard-format-v20
.. _djangobaseproject: https://github.com/acdh-oeaw/djangobaseproject
