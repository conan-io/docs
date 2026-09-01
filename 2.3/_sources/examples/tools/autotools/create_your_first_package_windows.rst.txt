.. _examples_tools_autotools_create_first_package_windows:

Create your first Conan package with Autotools in Windows (msys2)
=================================================================

.. warning::

  This example is intended for the Windows OS, using the ``msys2`` subsystem to run the autotools build system.
  The support is **limited**, the ``AutotoolsDeps`` generator still doesn't work for Windows, so the ``test_package``
  in the default template will fail.

  Note this example is building with the MSVC compiler, not with MinGW/gcc. Even if the build system is autotools,
  the example is targeting the MSVC compiler, and the resulting package will be binary compatible and can be used
  from other packages using MSVC with other build systems. It is not necessary to force MinGW/gcc to use some
  open source dependencies that use autotools, and ConanCenter builds all of them with MSVC.


In the :ref:`Create your first Conan package with Autotools<examples_tools_autotools_create_first_package>`
tutorial, the autotools integrations are presented. Please read first that section, to understand them, as this
section will only introduce the Windows/msys2 specific issues.

We will use the same the :command:`conan new` command to create a "Hello World" C++ library example project:

.. code-block:: bash

    $ conan new autotools_lib -d name=mypkg -d version=0.1

Check the above tutorial to understand the created files.

Besides these files, we will create a profile file:

.. code-block:: ini
    :caption: msys2_profile

    include(default)

    [conf]
    tools.microsoft.bash:subsystem=msys2
    tools.microsoft.bash:path=C:\ws\msys64\usr\bin\bash
    tools.build:compiler_executables={"c": "cl", "cpp": "cl"}


Note that you might need to adapt the path to the ``bash`` system of ``msys2``.

In the package recipe *conanfile.py* we will have:

.. code-block:: python

    win_bash = True

This is very important, it tells Conan that when this package is to be built, it has to launch a ``bash`` shell to 
execute the build in it.

.. note::

  It is not necessary, and in fact it is not recommended for most cases to be already running inside an ``msys2``
  terminal. Conan will automatically run the build subprocess for autotools in the defined bash shell.

  If already running in a bash shell, it is necessary to activate the ``tools.microsoft.bash:activate=True`` conf.


Let's build the package from sources with the current default configuration, making sure to deactivate the ``test_package``,
because otherwise it will fail.

.. code-block:: bash

    # Deactivating the test_package, as AutotoolsDeps doesn't work yet.
    $ conan create . -pr=msys2_profile -tf=""

    ...
    mypkg/0.1: package(): Packaged 1 '.h' file: mypkg.h
    mypkg/0.1: package(): Packaged 1 '.la' file: libmypkg.la
    mypkg/0.1: package(): Packaged 1 '.lib' file: mypkg.lib
    mypkg/0.1: Created package revision fa661758835cf6f7f311c857447393cc
    mypkg/0.1: Package '9bdee485ef71c14ac5f8a657202632bdb8b4482b' created

We can now validate that the recipe and the package binary are in the cache:


.. code-block:: bash

    $  conan list mypkg:*
    Found 1 pkg/version recipes matching mypkg in local cache
    Local Cache
      mypkg
        mypkg/0.1
          revisions
            6e85b0c27c7fbc8eddc1994dbb543b52 (2024-04-30 18:29:44 UTC)
              packages
                9bdee485ef71c14ac5f8a657202632bdb8b4482b
                  info
                    settings
                      arch: x86_64
                      build_type: Release
                      compiler: msvc
                      compiler.cppstd: 14
                      compiler.runtime: dynamic
                      compiler.runtime_type: Release
                      compiler.version: 193
                      os: Windows
                    options
                      shared: False


Note how the binary is a ``compiler=msvc`` one.

.. seealso::

    - :ref:`GNU built-in integrations reference<conan_tools_gnu>`.
