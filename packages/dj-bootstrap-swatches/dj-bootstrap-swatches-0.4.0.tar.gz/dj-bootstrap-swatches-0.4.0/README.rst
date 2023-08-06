=============================
Django Bootstrap Swatches
=============================

.. image:: https://badge.fury.io/py/dj-bootstrap-swatches.svg
    :target: https://badge.fury.io/py/dj-bootstrap-swatches

.. image:: https://travis-ci.org/bwarren2/dj-bootstrap-swatches.svg?branch=master
    :target: https://travis-ci.org/bwarren2/dj-bootstrap-swatches

.. image:: https://codecov.io/gh/bwarren2/dj-bootstrap-swatches/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bwarren2/dj-bootstrap-swatches

A swatch page for Bootstrap styling

Documentation
-------------

The full documentation is at https://dj-bootstrap-swatches.readthedocs.io.

Quickstart
----------

Install Django Bootstrap Swatches::

    pip install dj-bootstrap-swatches

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_bootstrap_swatches.apps.DjBootstrapSwatchesConfig',
        ...
    )

Add Django Bootstrap Swatches's URL patterns:

.. code-block:: python

    from dj_bootstrap_swatches import urls as dj_bootstrap_swatches_urls


    urlpatterns = [
        ...
        url(r'^bootswatch/', include(dj_bootstrap_swatches_urls)),
        ...
    ]

Per "Two Scoops of Django" design patterns, the default swatch page tries to extend a base template called `base.html` and a block called `content`.  If this isn't your practice, you'll need to adjust things to fit.

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
