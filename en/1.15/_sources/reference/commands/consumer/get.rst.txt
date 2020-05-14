
.. _conan_get:

conan get
=========

.. code-block:: bash

    $ conan get [-h] [-r REMOTE] [-raw] reference [path]

Gets a file or list a directory of a given reference or package.

.. code-block:: text

    positional arguments:
      reference             package recipe reference
      path                  Path to the file or directory. If not specified will
                            get the conanfile if only a reference is specified and
                            a conaninfo.txt file contents if the package is also
                            specified

    optional arguments:
      -h, --help            show this help message and exit
      -p PACKAGE, --package PACKAGE
                            Package ID [DEPRECATED: use full reference instead]
      -r REMOTE, --remote REMOTE
                            Get from this specific remote
      -raw, --raw           Do not decorate the text


**Examples**:

- Print the conanfile.py from a remote package:

  .. code-block:: bash

      $ conan get zlib/1.2.8@conan/stable -r conan-center


- List the files for a local package recipe:

  .. code-block:: bash

      $ conan get zlib/1.2.11@conan/stable .

      Listing directory '.':
       CMakeLists.txt
       conanfile.py
       conanmanifest.txt

- Print a file from a recipe folder:

  .. code-block:: bash

      $ conan get zlib/1.2.11@conan/stable conanmanifest.txt

- Print the conaninfo.txt file for a binary package:

  .. code-block:: bash

      $ conan get zlib/1.2.11@conan/stable:2144f833c251030c3cfd61c4354ae0e38607a909

  .. code-block:: text

      [settings]
          arch=x86_64
          build_type=Release
          compiler=apple-clang
          compiler.version=8.1
          os=Macos

      [requires]


      [options]
          # ...

- List the files from a binary package in a remote:

  .. code-block:: bash

      $ conan get zlib/1.2.11@conan/stable:2144f833c251030c3cfd61c4354ae0e38607a909 . -r conan-center

      Listing directory '.':
       conan_package.tgz
       conaninfo.txt
       conanmanifest.txt
