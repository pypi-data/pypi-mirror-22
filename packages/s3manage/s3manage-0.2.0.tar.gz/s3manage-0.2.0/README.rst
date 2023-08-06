========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/s3manage/badge/?style=flat
    :target: https://readthedocs.org/projects/s3manage
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/greg-hellings/s3manage.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/greg-hellings/s3manage

.. |requires| image:: https://requires.io/github/greg-hellings/s3manage/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/greg-hellings/s3manage/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/greg-hellings/s3manage/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/greg-hellings/s3manage

.. |version| image:: https://img.shields.io/pypi/v/s3manage.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/s3manage

.. |commits-since| image:: https://img.shields.io/github/commits-since/greg-hellings/s3manage/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/greg-hellings/s3manage/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/s3manage.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/s3manage

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/s3manage.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/s3manage

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/s3manage.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/s3manage


.. end-badges

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
