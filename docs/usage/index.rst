.. _usage-guide:

===========
Usage Guide
===========

.. contents:: Table of Contents

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

#. Since WikiSync needs to output the modified source code before uploading, we need to modify the directory structure a little:

    .. parsed-literal::
        wiki/
            src/
                index.html
                # ... all the content from above
            build/
                # this is where modified code will be stored

#. Now, we add the Python script, ``wikisync.py``, with the following lines of code:

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

.. warning::
    We use environment variables for credentials so that they're not committed to Git by mistake. If you're using a bash script to store your credentials, please remember to add it to ``.gitignore``.

And that's all! You're all set to deploy your wiki to iGEM!

If you'd like to test the functionality first, make a test folder with just a few files and try to upload that. Take a look at the following example for that.

Basic Example
-------------



