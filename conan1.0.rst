.. _conan_1_0:


Upgrading to conan 1.0
======================

If you were using a 0.X conan version, there are some things to consider while upgrading. They are reflected in the :ref:`changelog<changelog>`., but this section summarizes the most important changes here:


Command line changes
--------------------

There has been a few things that will break existing usage (compared to 0.30). Most of them are in command line arguments, so they are relatively easy to fix. The most important one is that now most commands require the path to the conanfile folder or file, instead of using ``--path`` and ``--file`` arguments. Specifically, :command:`conan install`, :command:`conan export` and :command:`conan create` will be the ones most affected:

.. code-block:: bash

    # instead of --path=myfolder --file=myconanfile.py, now you can do:
    $ conan install . # Note the "." is now mandatory
    $ conan install folder/myconanfile.txt
    $ conan install ../myconanfile.py
    $ conan info .
    $ conan create . user/channel
    $ conan create . Pkg/0.1@user/channel
    $ conan create mypkgconanfile.py Pkg/0.1@user/channel
    $ conan export . user/channel
    $ conan export . Pkg/0.1@user/channel
    $ conan export myfolder/myconanfile.py Pkg/0.1@user/channel

This behavior aligns with the :command:`conan source`, :command:`conan build`, :command:`conan package` commands, that all use the same arguments to locate the *conanfile.py* containing the logic to be run.

Now all commands read: :command:`command <origin-conanfile> ...`

Also, all arguments to command line now use dash instead of underscore:

.. code-block:: bash

    $ conan build .. --source-folder=../src  # not --source_folder

Deprecations/removals
---------------------

- scopes were completely removed in conan 0.30.X
- ``self.conanfile_directory`` has been removed. Use ``self.source_folder``, ``self.build_folder``, etc. instead
- ``self.cpp_info``, ``self.env_info`` and ``self.user_info`` scope has been reduced to only the ``package_info()`` method
- ``gcc`` and ``ConfigureEnvironment`` were already removed in conan 0.30.1
- ``werror`` doesn't exist anymore. Now it is the builtin behavior.
- Command ``test_package`` has been removed. Use :command:`conan create` and :command:`conan test` instead.
- ``CMake`` helper only allows now (from conan 0.29). the ``CMake(self)`` syntax
- :command:`conan package_files` command was replaced in conan 0.28 by :command:`conan export-pkg` command.


Settings and profiles. Gcc/CLang versioning
-------------------------------------------

gcc and clang compilers have modified their versioning approach, from gcc > 5 and clang > 4, 
the minors are really bugfixes, and then they have binary compatibility. To adapt to this,
conan now includes major version in the *settings.yml* default settings file:

.. code-block:: yaml

    gcc:
        version: ["4.1", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9",
                  "5", "5.1", "5.2", "5.3", "5.4",
                  "6", "6.1", "6.2", "6.3", "6.4",
                  "7", "7.1", "7.2"]

Most package creators want to use the major-only settings, like ``-s compiler=gcc -s compiler.version=5``,
instead of specifying the minors too.

The default profile detection and creation has been modified accordingly, but if you have a default
profile you may want to update it to reflect this:

.. code-block::text

    [settings]
    os=Linux
    compiler=gcc
    compiler.version=7 #instead of 7.2


Conan associated tools (conan-package-tools, conan.cmake) have been upgraded to accomodate this new defaults.





New features
------------

- Cross-compilation support with new default settings in settings.yml: ``os_build``, ``arch_build``, ``os_target``, ``arch_target``.
  They are automatically removed from the ``package_id`` computation, or kept if they
  are the only ones defined (as it happens usually with dev-tools packages). It is possible to keep them too with the ``self.info.include_build_settings()`` method (call it in your ``package_id()`` method).

.. important::

  Please **don't** use cross-build settings ``os_build``, ``arch_build`` for standard packages and libraries.
  They are only useful for packages that are used via ``build_requires``, like ``cmake_installer`` or ``mingw_installer``.


- Model and utilities for Windows subsystems

.. code-block:: bash

    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]

This subsetting can be used by build helpers as ``CMake``, to act accordingly.





