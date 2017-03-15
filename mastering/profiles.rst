Profiles
=========

So far we have used the default settings stored in ``conan.conf`` and defined as command line arguments.

However, configurations can be large, settings can be very different, and we might want to switch easily between different configurations with different settings, options, etc.

Profiles are text files, that can be stored in different locations, as for example the default ``<userhome>/.conan/profiles`` folder.

They would contain the desired configuration, for example assume the following file is named ``myprofile``:

.. code-block:: text

   [settings]
   compiler=clang
   compiler.version=3.5
   compiler.libcxx=libstdc++11

   [options]
   MyLib:shared=True
   
   [env]
   CC=/usr/bin/clang
   CXX=/usr/bin/clang++

And you can use it instead of command line arguments as:

.. code-block:: bash

  $ conan test_package -pr=myprofile


You can list and show existing profiles with the ``conan profile`` command:

.. code-block:: bash

   $ conan profile list
   > myprofile1
   > myprofile2
   $ conan profile show myprofile1
   > Profile myprofile1
   > [settings]
   > ...