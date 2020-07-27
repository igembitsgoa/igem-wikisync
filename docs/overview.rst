.. _overview:

========
Overview
========

**WikiSync** is a Python library that allows you to easily upload your iGEM wiki. There's no need anymore to manually upload each file, replace your URLs and copy paste your source code into a web form. Building and deployment can now be as simple as a ``git push``, thanks to `Travis <https://travis-ci.com>`_.

All you need are five lines of code:

.. code-block:: python

    import igem_wikisync as sync

    sync.run(
        team='your_team_name',
        src_dir='source_directory',
        build_dir='build_directory'
    )

Under the `existing iGEM wiki infrastucture <https://2020.igem.org/Resources/Wiki_Editing_Help>`_, you're required to upload every image, document or video individually, and create each page by typing code in a text box in your web browser. This presents serious challenges as your wiki grows into several pages with dozens of images. 

Creating a team wiki can be quite challenging, specially for a someone new to programming.  Modern code editors like `Visual Studio Code <https://code.visualstudio.com>`_ offer `several features <https://medium.com/@bretcameron/7-essential-features-of-visual-studio-code-for-web-developers-be77e235bf62>`_ to make it easier and writing code inside a web browser deprives you from using them. Even if you write code on a code editor instead of the iGEM webpage, you still need to copy-paste all your files every time you make changes. Doing this over and over for several months can quickly become an annoyance and divert focus away from your actual project.

Features
========

WikiSync automates the entire deployment process by allowing you to develop your wiki locally, so you can `look at your wiki as you code <https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer>`_. When you're done, you can effortlessly push your code to iGEM servers, by running just one command.

WikiSync also checks for broken links and keeps track of previously uploaded files. It goes through each file in your wiki source folder and uploads all images and documents. It then reads all your code, changes URLs to those recieved from iGEM and finally uploads the modified code as well. This allows your entire team to collaborate on platforms such as Github, which can then `automatically deploy to iGEM servers using Travis <travis guide link>`_.

Please head over to the :ref:`usage-guide` to get started, or take a look at our :ref:`tutorial` for step-by-step examples meant to help you make deployment as easy as a ``git push``.

Installation
============

::

    pip install igem-wikisync



Documentation
=============


https://igem-wikisync.readthedocs.io/

