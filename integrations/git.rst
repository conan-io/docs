
Git
___


|git_logo|

Project layout
==============


**Conan** uses plain text files, so its perfectly suitable for the use of a control version system.

Its not required that ``conanfile`` is in your project root folder. You can create it at any directory. Its only needed that you take in account the place where ``conanbuildinfo.*`` files are generated, so you can use them with your build system. 


Committed files
===============

**Conan** generates some files than should not be committed. These file can change in different computers and should be re-generated with **conan install** command.

We suggest committing ``conanfile.txt`` and ``conanfile.py`` and ignore the rest.

So, if you are using **git** you can append this to your ``.gitignore`` file:


.. code-block:: text

   conanbuildinfo.*
   conaninfo.txt


That's all! After a ``git clone`` or update just execute **conan install** command with the required settings and all the files will be generated matching your configuration. 


conanfile.py
============

If you are creating a **conan** package:

- You can use the :ref:`url field <package_url>` to indicate the origin of your recipe. If a **github** repository is detected, conan website will link your github issues page in conan's package page.
- You can use **git** to :ref:`obtain your sources<retrieve_source>` (requires git client in path)

.. |git_logo| image:: ../images/git_logo.png
