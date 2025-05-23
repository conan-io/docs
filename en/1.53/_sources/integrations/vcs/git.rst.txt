
|git_logo| Git
______________

**Conan** uses plain text files, ``conanfile.txt`` or ``conanfile.py``, so it's perfectly
suitable for the use of any version control system. We use and highly recommend :command:`git`.

Check :ref:`workflows section <workflows>` to learn more about project layouts that naturally fit version control systems.


Temporary files
===============

**Conan** generates some files that should not be committed, as *conanbuildinfo.\** and *conaninfo.txt*.
These files can change in different computers and are re-generated with the :command:`conan install` command.

However, these files are typically generated in the **build tree** not in the source tree, so they
will be naturally disregarded. Just take care in case you have created the **build** folder inside
your project (we do this in several examples in the documentation). In this case, you should add it to your *.gitignore* file:

.. code-block:: text
   :caption: *.gitignore*

   ...
   build/

Package creators
================

Check :ref:`scm feature<scm_feature>` to learn more about managing the libraries source code with Git.

If you are creating a **Conan** package:

- You can use the :ref:`url field <package_url>` to indicate the origin of your package recipe. If you are using an
  external package recipe, this url should point to the package recipe repository **not** to the external source origin.
  If a **github** repository is detected, the Conan website will link your github issues page from your Conan's package page.
- You can use :command:`git` to :ref:`obtain your source<method_source>` (requires the git client in the path) when creating
  external package recipes.



.. |git_logo| image:: ../../images/conan-git_logo.png
