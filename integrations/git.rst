
Git
___


|git_logo|

Project layout
==============


**Conan** uses plain text files, so it's perfectly suitable for the use of a version control system.

It's not required that ``conanfile`` is in your project root folder. You can create it in any directory. It's only needed that you take the place where ``conanbuildinfo.*`` files are generated into account, so that you can use them with your build system. 

Check :ref:`workflows section <workflows>` to know more about project layouts that naturally fit version control system,
as they locate all generated files in temporary out-of-source folders.

Committed files
===============

**Conan** generates some files than should not be committed. These file can change in different computers and should be re-generated with the **conan install** command.

We suggest committing ``conanfile.txt`` or ``conanfile.py`` and ignoring the rest.

So, if you are using **git**, you can append this to your ``.gitignore`` file:


.. code-block:: text

   conanbuildinfo.*
   conaninfo.txt


That's all! After a ``git clone`` or update, just execute the **conan install** command with the required settings and all the files will be generated, matching your configuration. 


conanfile.py
============

If you are creating a **conan** package:

- You can use the :ref:`url field <package_url>` to indicate the origin of your recipe. If a **github** repository is detected, the conan website will link your github issues page in conan's package page.
- You can use **git** to :ref:`obtain your sources<retrieve_source>` (requires the git client in the path)

.. |git_logo| image:: ../images/git_logo.png
