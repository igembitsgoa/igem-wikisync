========
Tutorial
========

.. contents:: Table of Contents

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
