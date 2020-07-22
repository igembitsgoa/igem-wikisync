========
Overview
========

.. start-badges

.. image:: https://img.shields.io/readthedocs/igem-wikisync?logo=Read%20The%20Docs&style=for-the-badge
    :target: https://readthedocs.org/projects/igem-wikisync
    :alt: Documentation Status

.. image:: https://img.shields.io/travis/com/igembitsgoa/igem-wikisync?logo=travis&style=for-the-badge
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/igembitsgoa/igem-wikisync

.. image:: https://img.shields.io/requires/github/igembitsgoa/igem-wikisync?style=for-the-badge
    :alt: Requirements Status

.. image:: https://img.shields.io/coveralls/github/igembitsgoa/igem-wikisync?logo=coveralls&style=for-the-badge
    :alt: Coverage Status
    :target: https://coveralls.io/r/igembitsgoa/igem-wikisync

.. image:: https://img.shields.io/github/commits-since/igembitsgoa/igem-wikisync/v0.0.0a9?logo=github&style=for-the-badge
    :alt: Commits since latest release
    :target: https://github.com/igembitsgoa/igem-wikisync/


.. end-badges

Automatically deploy iGEM Wikis.

* Free software: MIT license

Installation
============

::

    pip install igem-wikisync

You can also install the in-development version with::

    pip install https://github.com/igembitsgoa/igem-wikisync/archive/master.zip


Documentation
=============


https://igem-wikisync.readthedocs.io/


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
