.. _profiles:

Profiles
========

A profile text file has to be located in ``.conan/profiles/`` directory.
It's a text file that contains a predefined set of ``settings``, ``options``, ``environment variables``` and ``scopes`` and has this structure:

.. code-block:: text

   [settings]
   setting=value

   [options]
   MyLib:shared=True

   [env]
   env_var=value
   
   [scopes]
   scope=value


Profiles are useful for change global settings without specifying multiple "-s" and "-o"parameters in ``conan install`` or ``conan test`` command.

For example, if you are working with Linux and you usually work with ``gcc`` compiler, but you have installed ``clang`` 
compiler and want to install some package for ``clang`` compiler, you could do:

- Create a ``.conan/profiles/clang`` file:

.. code-block:: text

   [settings]
   compiler=clang
   compiler.version=3.5
   compiler.libcxx=libstdc++11
   
   [env]
   CC=/usr/bin/clang
   CXX=/usr/bin/clang++

   
- Execute conan install command passing the ``--profile`` or ``-pr`` parameter:


.. code-block:: bash

   conan install --profile clang

   

Without profiles you would have needed to set the CC and CXX variables in the environment to point to your clang compiler and use ``-s`` parameters to specify the settings:


.. code-block:: bash
   
   export CC=/usr/bin/clang
   export CXX=/usr/bin/clang++
   conan install -s compiler=clang -s compiler.version=3.5 -s compiler.libcxx=libstdc++11


A profile can also be used in ``conan test_package`` and ``info`` command:

.. code-block:: bash

   $ conan test_package --profile clang


Profiles can be located in different folders, and be referenced by absolute or relative path:

.. code-block:: bash

   $ conan install --profile /abs/path/to/profile  # abs path
   $ conan install --profile ./relpath/to/profile  # resolved to current dir
   $ conan install --profile profile  # resolved to user/.conan/profiles/profile

You can use ``$PROFILE_DIR`` in your profile and it will be replaced with the absolute path to the profile file.
It is useful to declare relative folders:

.. code-block:: text

   [env]
   PYTHONPATH=$PROFILE_DIR/my_python_tools
   

Package settings and env vars
.............................

Profiles also support **package settings** and **package environment variables** definition, so you can override some settings or env vars for some specific package:


- Create a ``.conan/profiles/zlib_with_clang`` file:

.. code-block:: text

   [settings]
   zlib:compiler=clang
   zlib:compiler.version=3.5
   zlib:compiler.libcxx=libstdc++11
   compiler=gcc
   compiler.version=4.9
   compiler.libcxx=libstdc++11
   
   [env]
   zlib:CC=/usr/bin/clang
   zlib:CXX=/usr/bin/clang++
   
- Your build tool will locate **clang** compiler only for the **zlib** package and **gcc** (default one) for the rest of your dependency tree.

