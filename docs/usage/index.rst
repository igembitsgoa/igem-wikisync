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

And that's all! You're all set to deploy your wiki to iGEM!

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

Configuration Options
---------------------

.. admonition:: Under construction.
    
    Coming up in a few days.

.. # TODO: Add config options


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

.. # TODO: WikiSync can generate travis config

.. admonition:: Under construction.

    Coming up in a few days.


Examples
--------

In this section, common use cases have been illustrated. If you need a more in-depth explanation, please head over to our :ref:`tutorial` where we explain everything you need to know.

A Basic Example
===============

If you'd like to test the functionality first, make a test folder with just a few files and try to upload that. The following example demonstrates that in more detail.

#1 **Start with the following directory structure:**

.. parsed-literal::
    wiki/
        src/
            Test/
                index.html              # homepage
                css/
                    style.css           # custom styles
                    igem-reset.css      # Resets styles that iGEM injects
                js/
                    main.js             # custom JS + iGEM reset
                assets/
                    img/
                        logo.jpg
                        background.jpg  
                Description/
                    index.html          # Description page
        build/
            # this will be filled by WikiSync
        wikisync.py

The source code is inside ``wiki/src/Test/`` instead of just ``wiki/src/`` so that any existing content on your wiki is not affected.

You can find a zipped version of this code `here <https://downgit.github.io/#/home?url=https://github.com/igembitsgoa/igem-wikisync-resources/tree/master/basic-example>`_.

#2 **Let's look at individual files now:**

``src/Test/index.html``:

.. code-block:: html
    :linenos:
    :emphasize-lines: 5,6,12,13,17,22
    
    <html lang="en">

    <head>
        <title>Testing iGEM WikiSync</title>
        <link rel="stylesheet" href="css/igem-reset.css">
        <link rel="stylesheet" href="css/style.css">
    </head>

    <body>
        <h1>iGEM Example Wiki</h1>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="./Description/">Description</a></li>
        </ul>
        <div class="container">
            <br><br>
            <img src="./assets/img/logo.png" alt="iGEM Logo" height=200 width=200>
            <br><br>
            <h1>Welcome to iGEM 2020!</h1>
            <p>This is a sample page, designed for a demonstration for iGEM WikiSync.</p>
        </div>
        <script src="./js/main.js"></script>
    </body>

    </html>

``src/Test/css/style.css``:

.. code-block:: css
    :linenos:
    :emphasize-lines: 3

    body {
        background-color: #f7feff;
        background-image: url(../assets/img/background.png);
    }

``wikisync.py`` is the same as shown in the `snippet above <#wikisync-snippet>`_. 


#3 **Export your credentials and run** ``wikisync.py``

This is described `above <#wikisync-snippet>`_. You should now see the following output:

.. admonition:: Under construction.
    
    Coming up in a few days.

..  # TODO: insert output here

#4 **Let's look at the files WikiSync has written in** ``build/`` **now:**

``build/Test/index.html``:

.. code-block:: html
    :linenos:
    :emphasize-lines: 3,4,10,11,15,20

    <html lang="en"><head>
        <title>Testing iGEM WikiSync</title>
        <link href="https://2020.igem.org/Template:BITSPilani-Goa_India/Test/css/igem-resetCSS?action=raw&amp;ctype=text/css" rel="stylesheet"/>
        <link href="https://2020.igem.org/Template:BITSPilani-Goa_India/Test/css/styleCSS?action=raw&amp;ctype=text/css" rel="stylesheet"/>
    </head>

    <body>
        <h1>iGEM Example Wiki</h1>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="https://2020.igem.org/Team:BITSPilani-Goa_India/Test/Description">Description</a></li>
        </ul>
        <div class="container">
            <br/><br/>
            <img alt="iGEM Logo" height="200" src="https://2020.igem.org/wiki/images/5/5a/T--BITSPilani-Goa_India--assets--img--logo.png" width="200"/>
            <br/><br/>
            <h1>Welcome to iGEM 2020!</h1>
            <p>This is a sample page, designed for a demonstration for iGEM WikiSync.</p>
        </div>
        <script src="https://2020.igem.org/Template:BITSPilani-Goa_India/Test/js/mainJS?action=raw&amp;ctype=text/javascript"></script>


    </body></html>


``build/Test/css/style.css``:

.. code-block:: css
    :linenos:
    :emphasize-lines: 3

    body {
        background-color: #f7feff;
        background-image: url(https://2020.igem.org/wiki/images/d/dc/T--BITSPilani-Goa_India--assets--img--background.png);
    }

There are a few things to note here:

#. All the files have been uploaded and their URLs substituted in the code.
#. The filenames have been changed according to iGEM specification. 
#. HTML files have been uploaded at ``igem.org/Team:`` but CSS and JS files have been uploaded at ``igem.org/Template:``, and appended with the required URL parameters.
#. A file called ``upload_map.yml`` should have appeared in your directory. Read more about it `here <#tracking-changes>`_.
#. A file called ``wikisync.cookies`` should have appeared in your directory. Read more about it `here <#cookies>`_ and make sure you add it to your ``.gitignore``.
#. A file called ``wikisync.log`` should have appeared in your directory. Read more about it `here <#logging>`_.
