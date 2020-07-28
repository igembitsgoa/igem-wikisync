.. _overview:

========
Overview
========

**WikiSync** is a Python library that allows you to easily upload your iGEM wiki. There's no need anymore to manually upload each file, replace each URL and copy paste your source code into a web form. Building and deployment can now be as simple as a ``git push``, thanks to `Travis <https://travis-ci.com>`_.

**All you need are five lines of code:**

.. code-block:: python

    import igem_wikisync as sync

    sync.run(
        team='your_team_name',
        src_dir='source_directory',
        build_dir='build_directory'
    )

Creating a team wiki can be quite challenging, specially for a someone new to programming. Under the `existing iGEM wiki infrastucture <https://2020.igem.org/Resources/Wiki_Editing_Help>`_, you're required to upload every image, document or video individually, and create each page by typing code in a text box in your web browser. 

As your wiki grows into several pages with dozens images, it becomes hard to manage all the components due to lack of simple features like syntax highlighting. Besides, in this age of automation, who likes to sit and upload a hundred pictures, anyway?

Modern code editors like `Visual Studio Code <https://code.visualstudio.com>`_ offer `several features <https://medium.com/@bretcameron/7-essential-features-of-visual-studio-code-for-web-developers-be77e235bf62>`_ to make programming easier and writing code inside a web browser deprives you from using them. Even if you write code on a code editor instead of the iGEM webpage, you still need to copy-paste all your files every time you make changes. 

Doing this over and over for several months can be time taking and divert focus away from your actual project.

WikiSync automates the entire deployment process and allows you to leverage all the features of modern IDEs. You can `see how your wiki looks <https://www.youtube.com/watch?v=WzE0yqwbdgU>`_ as you code and when you're done, you can effortlessly push your code to iGEM servers, by running just one command.

Please head over to the :ref:`usage-guide` to get started, or take a look at our :ref:`tutorial` for step-by-step examples meant to help you make deployment as easy as a ``git push``.


Features
========

#. Uploads media and documents
#. Checks for broken links
#. Replaces links in source code
#. Uploads modified source code
#. Keeps track of uploads and only upload changes
#. Renames media and documents according to iGEM specifications

Other Advantages of Using WikiSync
----------------------------------
#. Allows you to leverage modern IDEs like Visual Studio Code
#. Collaboration through `Github <https://github.com>`_
#. Automatic deployment through `Travis CI <https://travis-ci.com>`_