========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| 
        | |coveralls|
    * - package
      - | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/igem-wikisync/badge/?style=flat
    :target: https://readthedocs.org/projects/igem-wikisync
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/igembitsgoa/igem-wikisync.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/igembitsgoa/igem-wikisync

.. .. |requires| image:: https://requires.io/github/igembitsgoa/igem-wikisync/requirements.svg?branch=master
..     :alt: Requirements Status
..     :target: https://requires.io/github/igembitsgoa/igem-wikisync/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/github/igembitsgoa/igem-wikisync/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/igembitsgoa/igem-wikisync

.. |commits-since| image:: https://img.shields.io/github/commits-since/igembitsgoa/igem-wikisync/v0.0.0a9.svg
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
