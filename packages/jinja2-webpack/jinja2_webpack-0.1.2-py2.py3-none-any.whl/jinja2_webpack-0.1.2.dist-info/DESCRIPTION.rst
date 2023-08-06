========
Overview
========



Integration of webpack with jinja2

* Free software: BSD license

Installation
============

::

    pip install jinja2-webpack

Documentation
=============

https://python-jinja2-webpack.readthedocs.io/

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

0.1.0 (2017-05-28)
------------------

* First release on PyPI.


