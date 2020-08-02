.. _overview:

========
Overview
========

**WikiSync** is a Python library that allows you to easily upload your iGEM wiki. It eliminates the need to manually upload each file, replace each URL and copy paste your source code into a web form. Building and deployment can now be as simple as a ``git push``, thanks to `Travis <https://travis-ci.com>`_.

**All you need are five lines of code:**

.. code-block:: python

    import igem_wikisync as sync

    sync.run(
        team='your_team_name',
        src_dir='source_directory',
        build_dir='build_directory'
    )

WikiSync goes through each media file or document in your wiki folder, and uploads them. It then goes through your source code (HTML and CSS files) and replaces all the URLs with those received after uploading files. It then uploads this modified source code as well. It also checks for broken links.

By automating this, allows you to leverage all the `features of modern code editing software <https://medium.com/@bretcameron/7-essential-features-of-visual-studio-code-for-web-developers-be77e235bf62>`_ like `Visual Studio Code <https://code.visualstudio.com>`_. You can `see how your wiki looks <https://www.youtube.com/watch?v=WzE0yqwbdgU>`_ as you code and when you're done, you can effortlessly push your code to iGEM servers, by running just one command.

It also seamlessly integrates with continuous integration  software, which allows your entire team to collaborate on the wiki, and finally upload it without any extra effort.

To get started, proceed to the :ref:`installation` instructions. Then, head over to the :ref:`usage-guide` or take a look at our :ref:`tutorial` for step-by-step examples meant to help you make deployment as easy as a git push.


Features
========

#. Uploads media and documents
#. Checks for broken links
#. Replaces links in source code (HTML and CSS)
#. Uploads modified source code
#. Keeps track of uploads and only uploads changes
#. Renames media and documents according to iGEM specifications

Other Advantages of Using WikiSync
----------------------------------

WikiSync allows you to leverage:

#. Modern IDEs like Visual Studio Code
#. Collaboration through `Github <https://github.com>`_.
#. Automatic deployment through `Travis CI <https://travis-ci.com>`_