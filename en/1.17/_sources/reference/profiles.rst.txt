.. _profiles:

Profiles
=========

Profiles allows users to set a complete configuration set for **settings**, **options**, **environment variables**, and **build
requirements** in a file. They have this structure:

.. code-block:: text

    [settings]
    setting=value

    [options]
    MyLib:shared=True

    [env]
    env_var=value

    [build_requires]
    Tool1/0.1@user/channel
    Tool2/0.1@user/channel, Tool3/0.1@user/channel
    *: Tool4/0.1@user/channel

Profile can be created with ``new`` option in :command:`conan profile`. And then edit it later.

.. code-block:: bash

    $ conan profile new mynewprofile --detect

Profile files can be used with ``-pr``/``--profile`` option in :command:`conan install` and :command:`conan create` commands.

.. code-block:: bash

    $ conan create . demo/testing -pr=myprofile

Profiles can be located in different folders. For example, the default *<userhome>/.conan/profiles*, and be referenced by absolute or
relative path:

.. code-block:: bash

    $ conan install . --profile /abs/path/to/profile  # abs path
    $ conan install . --profile ./relpath/to/profile  # resolved to current dir
    $ conan install . --profile profile  # resolved to user/.conan/profiles/profile

Listing existing profiles in the *profiles* folder can be done like this:

.. code-block:: bash

    $ conan profile list
    default
    myprofile1
    myprofile2
    ...

You can also show profile's content:

.. code-block:: bash

    $ conan profile show myprofile1
    Configuration for profile myprofile1:

    [settings]
    os=Windows
    arch=x86_64
    compiler=Visual Studio
    compiler.version=15
    build_type=Release
    [options]
    [build_requires]
    [env]

Use ``$PROFILE_DIR`` in your profile and it will be replaced with the absolute path to
the directory where the profile file is (this path will contain only forward slashes).
It is useful to declare relative folders:

.. code-block:: text

    [env]
    PYTHONPATH=$PROFILE_DIR/my_python_tools

.. tip::

    You can manage your profiles and share them using :ref:`conan_config_install`.

Package settings and env vars
-----------------------------

Profiles also support **package settings** and **package environment variables** definition, so you can override some settings or
environment variables for some specific package:

.. code-block:: text
   :caption: *.conan/profiles/zlib_with_clang*

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

Your build tool will locate **clang** compiler only for the **zlib** package and **gcc** (default one) for the rest of your dependency tree.

.. note::

    If you want to override existing system environment variables, you should use the ``key=value`` syntax. If you need to pre-pend to the
    system environment variables you should use the syntax ``key=[value]`` or ``key=[value1, value2, ...]``. A typical example is the
    ``PATH`` environment variable, when you want to add paths to the existing system PATH, not override it, you would use:

    .. code-block:: text

        [env]
        PATH=[/some/path/to/my/tool]

Profile composition
-------------------

You can specify multiple profiles in the command line. The applied configuration will be the composition
of all the profiles applied in the order they are specified.

If, for example, you want to apply a :ref:`build require<build_requires>`, like a ``cmake`` installer to your dependency tree, 
it won't be very practical adding the `cmake` installer reference, e.g  ``cmake_installer/3.9.0@conan/stable`` to all your profiles where you could
need to inject ``cmake`` as a build require.

You can specify both profiles instead:

.. code-block:: text
   :caption: *.conan/profiles/cmake_39*

    [build_requires]
    cmake_installer/3.9.0@conan/stable

.. code-block:: bash

   $ conan install . --profile clang --profile cmake_39

Profile includes
----------------

You can include other profiles using the ``include()`` statement. The path can be relative to the current profile, absolute, or a profile
name from the default profile location in the local cache.

The ``include()`` statement has to be at the top of the profile file:

.. code-block:: text
   :caption: *gcc_49*

    [settings]
    compiler=gcc
    compiler.version=4.9
    compiler.libcxx=libstdc++11

.. code-block:: text
   :caption: *myprofile*

    include(gcc_49)

    [settings]
    zlib:compiler=clang
    zlib:compiler.version=3.5
    zlib:compiler.libcxx=libstdc++11

    [env]
    zlib:CC=/usr/bin/clang
    zlib:CXX=/usr/bin/clang++

Variable declaration
--------------------

In a profile you can declare variables that will be replaced automatically by Conan before the profile is applied. The variables have to be
declared at the top of the file, after the ``include()`` statements.

.. code-block:: text
   :caption: *myprofile*

   include(gcc_49)
   CLANG=/usr/bin/clang

   [settings]
   zlib:compiler=clang
   zlib:compiler.version=3.5
   zlib:compiler.libcxx=libstdc++11

   [env]
   zlib:CC=$CLANG/clang
   zlib:CXX=$CLANG/clang++

The variables will be inherited too, so you can declare variables in a profile and then include the profile in a different one, all the
variables will be available:

.. code-block:: text
   :caption: *gcc_49*

   GCC_PATH=/my/custom/toolchain/path/

   [settings]
   compiler=gcc
   compiler.version=4.9
   compiler.libcxx=libstdc++11

.. code-block:: text
   :caption: *myprofile*

   include(gcc_49)

   [settings]
   zlib:compiler=clang
   zlib:compiler.version=3.5
   zlib:compiler.libcxx=libstdc++11

   [env]
   zlib:CC=$GCC_PATH/gcc
   zlib:CXX=$GCC_PATH/g++

Examples
--------

If you are working with Linux and you usually work with **gcc** compiler, but you have installed **clang** compiler and want to install some
package for ``clang`` compiler, you could do:

- Create a ``.conan/profiles/clang`` file:

.. code-block:: text

   [settings]
   compiler=clang
   compiler.version=3.5
   compiler.libcxx=libstdc++11

   [env]
   CC=/usr/bin/clang
   CXX=/usr/bin/clang++

- Execute an install command passing the :command:`--profile` or :command:`-pr` parameter:

.. code-block:: bash

   $ conan install . --profile clang

Without profiles you would have needed to set CC and CXX variables in the environment to point to your clang compiler and use :command:`-s`
parameters to specify the settings:

.. code-block:: bash

    $ export CC=/usr/bin/clang
    $ export CXX=/usr/bin/clang++
    $ conan install -s compiler=clang -s compiler.version=3.5 -s compiler.libcxx=libstdc++11

A profile can also be used in :command:`conan create` and :command:`conan info`:

.. code-block:: bash

    $ conan create . demo/testing --profile clang

.. seealso::

    - Check the section :ref:`build_requires` to read more about its usage in a profile.
    - Check :ref:`conan_profile` and :ref:`default_profile` for full reference.
    - Related section: :ref:`cross_building`.
