Inspecting Packages
===================

You can inspect the uploaded packages and also the packages in the local cache by running the
:command:`conan get` command.

- List the files of a local recipe folder:

  .. code-block:: bash

      $ conan get zlib/1.2.11@ .

      Listing directory '.':
       conandata.yml
       conanfile.py
       conanmanifest.txt

- Print the *conaninfo.txt* file of a binary package:

  .. code-block:: bash

      $ conan get zlib/1.2.11@:2144f833c251030c3cfd61c4354ae0e38607a909

- Print the *conanfile.py* from a remote package:

  .. code-block:: bash

      $ conan get zlib/1.2.11@ -r conan-center

  .. code-block:: python

      import os
      import stat
      from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
      from conans.errors import ConanException


      class ZlibConan(ConanFile):
          name = "zlib"
          version = "1.2.11"
          url = "https://github.com/conan-io/conan-center-index"
          homepage = "https://zlib.net"


          #...

Check the :ref:`conan get command<conan_get>` command reference and more examples.
