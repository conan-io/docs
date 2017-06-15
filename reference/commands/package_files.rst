.. _conan_package_files_command:

conan package_files
===================

.. code-block:: bash

	$  conan package_files [-h] [--path PATH] [--profile PROFILE]
                           [--options OPTIONS] [--settings SETTINGS] [-f]
                           reference


Creates a package binary from given precompiled artifacts in user folder, skipping the package recipe
``build()`` and ``package()`` methods.



.. code-block:: bash

    positional arguments:
      reference             package recipe reference e.g.,
                            MyPackage/1.2@user/channel

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Get binaries from this path, relative to current or
                            absolute
      --profile PROFILE, -pr PROFILE
                            Profile for this package
      --options OPTIONS, -o OPTIONS
                            Options for this package. e.g., -o PkgName:with_qt=true
      --settings SETTINGS, -s SETTINGS
                            Settings for this package e.g., -s compiler=gcc
      -f, --force           Overwrite existing package if existing


Note that this is **not** the normal or recommended flow for creating conan packages, as packages created this way will not have a reproducible build from sources. This command is intended only when it is not possible to build the packages from sources.

To create packages this way, a recipe must already exist for it. Typically this recipe will be simple, without ``build()`` and ``package()`` methods, though the ``package_info()`` method is still necessary to be able to automatically provide information for consumers. The command ``conan new <ref> --bare`` will create a simple recipe that could be used in combination with the ``package_files`` command. Check this :ref:`How to package existing binaries <existing_binaries>`





**Example**:

- Create a package from a directory containing the binaries for Windows/x86/Release:

Having these files:

.. code-block:: text


    Release_x86/lib/libmycoollib.a
    Release_x86/lib/other.a
    Release_x86/include/mylib.h
    Release_x86/include/other.h

Run:

.. code-block:: bash

    $ conan package_files Hello/0.1@lasote/stable -s os=Windows -s arch=x86 -s build_type=Relase --path=Release_x86

