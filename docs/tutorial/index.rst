.. _tutorial:

========
Tutorial
========

.. contents:: Table of Contents

.. note::

    We'll soon put up more detailed tutorials. For the time being, please go through the following and reach out for any queries at ballaneypranav@gmail.com.


Uploading a Test Folder
------------------------

If you'd like to test the functionality first, make a test folder with just a few files and try to upload that. The following example demonstrates that in more detail.

#1 **Start with the following directory structure:**

.. parsed-literal::
    wiki/
        src/
            WS-basic/                   # just so that your main wiki is not affected
                index.html              # homepage
                css/
                    style.css           # custom styles
                    igem-reset.css      # Resets styles that iGEM injects
                js/
                    main.js             # custom JS + iGEM reset
                Description/
                    index.html          # Description page
            assets/                     # everything else must be in the assets folder
                WS-basic/               # just so that your main wiki is not affected
                    img/
                        logo.jpg
                        background.jpg  
        build/
            # this will be filled by WikiSync
        wikisync.py

The source code is inside ``wiki/src/WS-basic/`` instead of just ``wiki/src/`` so that any existing content on your wiki is not affected. Similarly, images are inside ``assets/WS-basic/img/`` instead of just ``assets/img``.

Please download a zipped version of this code `here <https://downgit.github.io/#/home?url=https://github.com/igembitsgoa/igem-wikisync-resources/tree/master/basic-example>`_.

#2 **Let's look at individual files now:**

``src/WS-basic/index.html``:

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

``src/WS-basic/css/style.css``:

.. code-block:: css
    :linenos:
    :emphasize-lines: 3

    body {
        background-color: #f7feff;
        background-image: url(../assets/img/background.png);
    }


#3 **Create ``wikisync.py``**:

.. code-block:: python

    import igem_wikisync as sync

    sync.run(
        team='your_team_name', 
        src_dir='source_directory'      # folder where your wiki is stored
        build_dir='build_directory'     # folder where WikiSync will temporarily store your wiki before uploading
    )

#4 **Export your credentials as environment variables**:

On Windows Powershell:

    .. code-block:: bash

        $env:IGEM_USERNAME = 'youriGEMusername'
        $env:IGEM_PASSWORD = 'youriGEMpassword'
    
You can verify by running:

    .. code-block:: bash

        Get-ChildItem Env:IGEM_USERNAME

On Mac or Linux:

    .. code-block:: bash

        export IGEM_USERNAME=youriGEMusername
        export IGEM_PASSWORD=youriGEMpassword
    
You can verify by running:

    .. code-block:: bash

        echo $IGEM_USERNAME



#5 **Run** ``wikisync.py``::

    python wikisync.py

You should now see the following output:

.. code-block:: console

    > python wikisync.py
    Done! Successfully uploaded:
        2 assets
        2 HTML files
        2 stylesheets
        1 JS scripts
    Please look at the log for more details.

#6 **Let's look at the files WikiSync has written in** ``build/`` **now:**

``build/WS-basic/index.html``:

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


``build/WS-basic/css/style.css``:

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
#. A file called ``upload_map.yml`` should have appeared in your directory. Read more about it the section about :ref:`tracking-changes`.
#. A file called ``wikisync.cookies`` should have appeared in your directory. Read more about in the section about :ref:`cookies` and make sure you add it to your ``.gitignore``.
#. A file called ``wikisync.log`` should have appeared in your directory. Read more about it in the section about :ref:`logging`.

.. note:: 

    We're working on some more tutorials. They will be up soon.


Collaborating with your Team using Github
-----------------------------------------

Git: https://www.youtube.com/watch?v=USjZcfj8yxE&t=217s

Github: https://www.youtube.com/watch?v=nhNq2kIvi9s

Continuous Deployment with Travis
---------------------------------

Travis: https://www.youtube.com/watch?v=g0KsiCj3CgQ&t=1s

You'll also need to add ``GITHUB_USERNAME``, ``IGEM_USERNAME`` and ``IGEM_PASSWORD`` along with ``GITHUB_TOKEN`` as environment variables on Travis. We will have more details on the process up here soon.

Please read the :ref:`continuous-integration` section in the :ref:`usage-guide` for now. We will have this tutorial up soon.

Testing before Deployment with Github Pages
-------------------------------------------

