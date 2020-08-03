.. _installation:

============
Installation
============

WikiSync is a Python package, so it can be installed like any other.

Execute the following at the command line::

    pip install igem-wikisync

WikiSync is supported only on Python 3.5+.

We've tested WikiSync on several operating systems across all supported Python versions. However, it's still in development and as we wait for iGEM teams to adopt it and provide feedback, we request you to kindly keep your copy of the software updated. You can do that by running the following command before you use WikiSync.

::
        
    pip install -U igem-wikisync

If you don't have ``pip`` installed, please click `here <https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py>`_ for instructions. 

.. .. _known-issues:

.. Known Issues
.. ------------

.. SSL error:

.. * Check pyopenssl installation with --force-reinstall

.. * Install python3.6 using deadsnakes ppa

.. * Check location of installed pyopenssl without :code:`--force-reinstall` and ensure that the location is present in :code:`$PATH`
