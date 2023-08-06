========
Overview
========



Utilities to help manage S3 buckets

* Free software: BSD license

Installation
============

::

    pip install s3manage

Documentation
=============

https://s3manage.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2017-05-26)
------------------

* First release on PyPI.


