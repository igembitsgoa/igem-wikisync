.. _usage-guide:

===========
Usage Guide
===========

.. contents:: Table of Contents

.. # TODO: media must be in assets/

Getting Started
---------------

WikiSync runs through a Python script in your root directory, and looks for your iGEM username and password in your terminal session as environment variables. 

.. note::

    In this guide, we assume a familiarity and level of comfort with Python and command line software. If that doesn't sound like you, head over to our :ref:`tutorial` where we explain everything you need to know.

In the Python script, it requires three parameters as input: 

#. ``src_dir``: Folder where your source code exists.
#. ``build_dir``: Folder where WikiSync will save the modified code before uploading.
#. ``team``: Your team name registered with iGEM.

Let's assume your wiki folder has the following structure:
    
.. parsed-literal::
    wiki/
        index.html
        css/                
            home.css
            content.css
        js/
            main.js
            content.js
        assets/
            img/
                logo.jpg
            video/
                intro.mp4
        Description/    
            index.html
        Design/
            index.html

#. Since WikiSync saves the modified source code before uploading, the directory structure needs to change a little:

    .. parsed-literal::
        wiki/
            src/
                index.html
                # ... all the content from above
            build/
                # this is where modified code will be stored

#. Now, add the Python script, ``wikisync.py``:

    .. _wikisync-snippet:
    
    .. code-block:: python

        import igem_wikisync as sync

        sync.run(
            team='your_team_name',
            src_dir='source_directory',     # 'src' in this case
            build_dir='build_directory'     # 'build' in this case
        )

#. Export the following environment variables:

    .. parsed-literal::
        IGEM_USERNAME=youriGEMusername
        IGEM_PASSWORD=youriGEMpassword


#. Run wikisync.py by executing:

    .. code-block:: bash

        python3 wikisync.py

.. caution::
    We use environment variables for credentials so that they're not accidentally committed to Git. If you're using a bash script to export your credentials, please remember to add it to ``.gitignore``.

And that's all! Your wiki has been deployed to iGEM!

Read on to see how WikiSync performs optimizations by storing cookies and uploading only the files that have changed. 

.. _cookies:

Maintaining a Session
---------------------

WikiSync stores cookies so you don't have to login on every run. This reducing network overhead and also makes the overall operation faster.

Cookies are stored in a file called ``wikisync.cookies`` in the directory where WikiSync is run.

.. caution::
    It is strongly recommended that you add ``wikisync.cookies`` to ``.gitignore``.

.. _tracking-changes:

Keeping Track of Changes
------------------------

After each run of WikiSync, it creates a file called ``upload_map.yml`` in the directory where it was run. This is a list of files it has encountered and uploaded till now, along with their URLs and MD5 hashes. This ensures that existing files are not uploaded again, but their URLs still can be substituted in the code. MD5 hashes allow it to check for changes within existing files, so it can upload the modified versions.

This is also useful in case connection to iGEM servers is lost while uploading. WikiSync saves the intermediate state in the upload map, so you can resume from that point when the internet connection is restored.

The upload map can (and should) be tracked by a version control system, to allow `continuous integration`_ and deployment through `Travis <https://travis-ci.com>`_. This also helps you get a bird's eye view of the upload operation without having to read the log.

The upload map should never be edited manually. If this file is deleted/damaged, WikiSync will upload each file again, which can overload the iGEM servers unnecessarily. This can be especially troublesome when all the teams try to upload their content, close to the Wiki Freeze.

Tracking Broken Links
---------------------

As your wiki grows into several pages and hundreds of links spread across them, it can be hard to find broken links. WikiSync tries to make this easier by checking for broken (internal) links. This functionality is enabled by default to enforce good practice, but it can be disabled. Look at the configuration options to know more about this.

.. note::
    Broken link warnings can be silenced by passing ``silence_warnings=True`` in the call to ``wikisync.run()``.

.. _logging:

Logging
-------

WikiSync prints a log of all the operations it carries out, allowing you to oversee them. This log is present in the ``wikisync.log`` file. You can search for specific events using the following keywords:

.. admonition:: Under construction.
    
    Coming up in a few days.

.. # TODO: Improve logs

This file doesn't contain any sensitive information, and can be committed to git.

.. _continuous-integration:

Continuous Integration
----------------------
Since WikiSync can upload your entire wiki automatically, this job can now be fully integrated into your version control system itself. `Travis CI <https://travis-ci.com>`_ can now deploy to iGEM just as easily as it can deploy to Github Pages. 

.. note::

    In this guide, we assume a familiarity and level of comfort with version control systems and continuous integration. If that doesn't sound like you, head over to our :ref:`tutorial` where we explain everything you need to know.

Please find here `a Travis configuration <https://gist.github.com/ballaneypranav/7b5ad1024f9ad2edc721e59c917c915d>`_ file that you can directly include in your project

You'll also need to add ``GITHUB_USERNAME``, ``IGEM_USERNAME`` and ``IGEM_PASSWORD`` along with ``GITHUB_TOKEN`` as environment variables on Travis. We will have more details on the process up here soon.

.. TODO: Write more about this.


