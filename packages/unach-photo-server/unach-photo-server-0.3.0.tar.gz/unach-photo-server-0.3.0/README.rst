=============================
unach_photo_server
=============================

.. image:: https://badge.fury.io/py/unach-photo-server.svg
    :target: https://badge.fury.io/py/unach-photo-server

.. image:: https://travis-ci.org/javierhuerta/unach-photo-server.svg?branch=master
    :target: https://travis-ci.org/javierhuerta/unach-photo-server

.. image:: https://codecov.io/gh/javierhuerta/unach-photo-server/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/javierhuerta/unach-photo-server

Aplicación web encargada de conectar con los repositorios de fotografías dispersos en la unach y generar servicios web para consultar por las fotografías de usuarios.

Documentation
-------------

The full documentation is at https://unach-photo-server.readthedocs.io.

Quickstart
----------

Install unach_photo_server::

    pip install unach-photo-server

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'unach_photo_server.apps.UnachPhotoServerConfig',
        ...
    )

Add unach_photo_server's URL patterns:

.. code-block:: python

    from unach_photo_server import urls as unach_photo_server_urls


    urlpatterns = [
        ...
        url(r'^', include(unach_photo_server_urls)),
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
