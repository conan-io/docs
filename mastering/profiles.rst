.. _profiles:


Profiles
=========

So far we have used the default settings stored in ``conan.conf`` and defined as command line arguments.

However, configurations can be large, settings can be very different, and we might want to switch easily between different configurations with different settings, options, etc.

Profiles can be located in different folders, as for example the default ``<userhome>/.conan/profiles``, and be referenced by absolute or relative path:

.. code-block:: bash

   $ conan install --profile /abs/path/to/profile  # abs path
   $ conan install --profile ./relpath/to/profile  # resolved to current dir
   $ conan install --profile profile  # resolved to user/.conan/profiles/profile


A profile file contains a predefined set of ``settings``, ``options``, ``environment variables``` and ``scopes`` and has this structure:

.. code-block:: text

   [settings]
   setting=value

   [options]
   MyLib:shared=True

   [env]
   env_var=value

   [scopes]
   scope=value


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

You can use ``$PROFILE_DIR`` in your profile and it will be replaced with the absolute path to the profile file.
It is useful to declare relative folders:

.. code-block:: text

   [env]
   PYTHONPATH=$PROFILE_DIR/my_python_tools


Package settings and env vars
-----------------------------

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


Profile includes
----------------

You can include other profiles using the ``include()`` sentence. The paths can be relative to the current profile, absolute,
or a profile name from the default profile location in the local cache.

The ``include()`` sentence has to be at the top of the profile file:


**gcc_49.txt**

.. code-block:: text

   compiler=gcc
   compiler.version=4.9
   compiler.libcxx=libstdc++11


**myprofile.txt**
.. code-block:: text

   include(gcc_49.txt)

   [settings]
   zlib:compiler=clang
   zlib:compiler.version=3.5
   zlib:compiler.libcxx=libstdc++11

   [env]
   zlib:CC=/usr/bin/clang
   zlib:CXX=/usr/bin/clang++


Variable declaration
--------------------

In a profile you can declare variables that will be replaced automatically by conan before the profile is applied.
The variables have to be declared at the top of the file, after the include() statements.

e.j

.. code-block:: text

   include(gcc_49)
   CLANG=/usr/bin/clang

   [settings]
   zlib:compiler=clang
   zlib:compiler.version=3.5
   zlib:compiler.libcxx=libstdc++11

   [env]
   zlib:CC=$CLANG/clang
   zlib:CXX=$CLANG/clang++


Examples
--------

If you are working with Linux and you usually work with ``gcc`` compiler, but you have installed ``clang``
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



.. seealso:: - :ref:`Howtos/Cross Building <cross_building>`
             - :ref:`Reference/Commands/conan profile <conan_profile_command>`
             - :ref:`Reference/Commands/conan install <conan_install_command>`
             - :ref:`Reference/Commands/conan test_package <conan_test_package_command>`