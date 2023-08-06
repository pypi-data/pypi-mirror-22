=============================
Django TileStache
=============================

.. image:: https://badge.fury.io/py/django-tilestache.svg
    :target: https://badge.fury.io/py/django-tilestache

.. image:: https://travis-ci.org/george-silva/django-tilestache.svg?branch=master
    :target: https://travis-ci.org/george-silva/django-tilestache

.. image:: https://codecov.io/gh/george-silva/django-tilestache/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/george-silva/django-tilestache

Command and Control Center for Tilestache, inside a django app

Documentation
-------------

The full documentation is at https://django-tilestache.readthedocs.io.

Quickstart
----------

Install Django TileStache::

    pip install django-tilestache

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_tilestache.apps.DjangoTilestacheConfig',
        ...
    )

Add Django TileStache's URL patterns:

.. code-block:: python

    from django_tilestache import urls as django_tilestache_urls


    urlpatterns = [
        ...
        url(r'^', include(django_tilestache_urls)),
        ...
    ]

Features
--------

* TODO

Uploading new distros
---------------------

.. code-block:: bash
bumpversion --current-version x.x.x minor
make release
git push origin master --tags


Running Tests
-------------

Does the code actually work?

.. code-block:: python

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

0.1.0 (2017-04-24)
++++++++++++++++++

* First release on PyPI.


