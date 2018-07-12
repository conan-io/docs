.. _conan_1_0:


Upgrading to conan 1.0
======================

This section summarizes the most important changes you need to consider when upgrading to Conan v1.0 from version 0.x. For a full list of changes and considerations, please refer to the :ref:`changelog<changelog>`.


Command line changes
--------------------

There are a few breaking changes (compared to v0.30), however, most of them are in command line arguments so they are quite easy to fix. The most significant change  is that now, instead of using ``--path`` ``--file`` arguments, most commands now require the path to the conanfile folder or file. Specifically, :command:`conan install`, :command:`conan export` and :command:`conan create` will be the ones most affected:

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

This behavior aligns with the :command:`conan source`, :command:`conan build`, :command:`conan package` commands, that all use the same arguments to locate the *conanfile.py* file containing the logic to be run.

Now, all commands read: :command:`command <origin-conanfile> ...`

In addition, all command line arguments now use a dash instead of an underscore:

.. code-block:: bash

    $ conan build .. --source-folder=../src  # not --source_folder

Deprecations/removals
---------------------

- scopes were completely removed in conan 0.30.X
- ``self.conanfile_directory`` has been removed. Instead, use ``self.source_folder``, ``self.build_folder``, etc.
- ``self.cpp_info``, ``self.env_info`` and ``self.user_info`` scope are now only included the ``package_info()`` method
- ``gcc`` and ``ConfigureEnvironment`` were removed in conan 0.30.1
- ``werror`` doesn't exist anymore. It is now built-in behavior.
- The ``test_package`` command has been removed. Instead, use :command:`conan create` and :command:`conan test`.
- From Conan v0.29, the``CMake`` helper only supports the ``CMake(self)`` syntax
- In Conan v0.28, the :command:`conan package_files` command was replaced by the :command:`conan export-pkg` command.


Settings and profiles. GCC/CLang versioning
-------------------------------------------

The GCC and Clang compilers have modified their versioning approach. From GCC version 5 and above and Clang version 4 and above, minor versions are really bug fixes, and then, they have binary compatibility. To adapt to this, Conan now includes a major version in the *settings.yml* default settings file:

.. code-block:: yaml

    gcc:
        version: ["4.1", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9",
                  "5", "5.1", "5.2", "5.3", "5.4",
                  "6", "6.1", "6.2", "6.3", "6.4",
                  "7", "7.1", "7.2"]

Most package creators want to use the major-only settings, like ``-s compiler=gcc -s compiler.version=5``,
instead of specifying the minors too.

The default profile detection and creation has been modified accordingly, however, if you have a default profile you may want to update it to reflect this:

.. code-block:: text

    [settings]
    os=Linux
    compiler=gcc
    compiler.version=7 #instead of 7.2

Conan associated tools (conan-package-tools, conan.cmake) have been upgraded to accomodate these new defaults.

New features
------------

- Cross-compilation support with new default settings in *settings.yml*: ``os_build``, ``arch_build``, ``os_target``, ``arch_target``.
  These are automatically removed from the ``package_id`` computation, or kept if they are the only ones defined (as usually happens with dev-tools packages). You can also keep them with the ``self.info.include_build_settings()`` method (call it in your ``package_id()`` method).

.. important::

    **Do not** use cross-build settings ``os_build`` and ``arch_build`` for standard packages and libraries.
  They are only useful for packages that are used via ``build_requires``, like ``cmake_installer`` or ``mingw_installer``.


- Model and utilities for Windows subsystems

.. code-block:: bash

    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]

This subsetting can be used by build helpers such as ``CMake`` to act accordingly.





