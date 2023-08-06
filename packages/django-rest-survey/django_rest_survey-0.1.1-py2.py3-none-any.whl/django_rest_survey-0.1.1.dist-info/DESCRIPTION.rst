=============================
Django REST Survey
=============================

.. image:: https://badge.fury.io/py/django-rest-survey.svg
    :target: https://badge.fury.io/py/django-rest-survey

.. image:: https://travis-ci.org/george-silva/django-rest-survey.svg?branch=master
    :target: https://travis-ci.org/george-silva/django-rest-survey

.. image:: https://codecov.io/gh/george-silva/django-rest-survey/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/george-silva/django-rest-survey

Dynamic and custom surveys for any objects in your database

Documentation
-------------

The full documentation is at https://django-rest-survey.readthedocs.io.

Quickstart
----------

Install Django REST Survey::

    pip install django-rest-survey

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rest_survey.apps.RestSurveyConfig',
        ...
    )

Add Django REST Survey's URL patterns:

.. code-block:: python

    from rest_survey import urls as rest_survey_urls


    urlpatterns = [
        ...
        url(r'^', include(rest_survey_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2017-06-06)
++++++++++++++++++

* First release on PyPI.


