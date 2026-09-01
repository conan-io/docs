Inspecting Packages
===================

You can inspect the uploaded packages and also the packages in the local cache by running the
:command:`conan get` command.

- List the files of a local recipe folder:

  .. code-block:: bash

      $ conan get zlib/1.2.8@conan/stable .

      Listing directory '.':
       CMakeLists.txt
       conanfile.py
       conanmanifest.txt

- Print the *conaninfo.txt* file of a binary package:

  .. code-block:: bash

      $ conan get zlib/1.2.11@conan/stable -p 09512ff863f37e98ed748eadd9c6df3e4ea424a8

- Print the *conanfile.py* from a remote package:

  .. code-block:: bash

      $ conan get zlib/1.2.8@conan/stable -r conan-center

  .. code-block:: python

      from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
      from conans.util import files
      from conans import __version__ as conan_version
      import os


      class ZlibConan(ConanFile):
          name = "zlib"
          version = "1.2.8"
          ZIP_FOLDER_NAME = "zlib-%s" % version

          #...

Check the :ref:`conan get command<conan_get>` command reference and more examples.
