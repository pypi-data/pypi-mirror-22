=============================
unach_photo
=============================

.. image:: https://badge.fury.io/py/unach-photo.svg
    :target: https://badge.fury.io/py/unach-photo

.. image:: https://travis-ci.org/javierhuerta/unach-photo.svg?branch=master
    :target: https://travis-ci.org/javierhuerta/unach-photo

.. image:: https://codecov.io/gh/javierhuerta/unach-photo/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/javierhuerta/unach-photo

Aplicación Django cliente para conectar con repositorios de fotografías de personas relacionadas a la unach.

Documentation
-------------

The full documentation is at https://unach-photo.readthedocs.io.

Quickstart
----------

Install unach_photo::

    pip install unach-photo

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'unach_photo.apps.UnachPhotoConfig',
        ...
    )

Add unach_photo's URL patterns:

.. code-block:: python

    from unach_photo import urls as unach_photo_urls


    urlpatterns = [
        ...
        url(r'^', include(unach_photo_urls)),
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

0.1.0 (2017-05-15)
++++++++++++++++++

* First release on PyPI.


