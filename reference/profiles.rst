.. _profiles:

Profiles
=========

Profiles allows users to set a complete configurateion set for **settings**, **options**, **environment variables**, and **build
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

Profile files can be used with ``-pr``/``--profile`` option in :command:`conan install` and :command:`conan create` commands.

.. code-block:: bash

    $ conan create demo/testing -pr=myprofile

Profiles can be located in different folders, for example, the default ``<userhome>/.conan/profiles``, and be referenced by absolute or
relative path:

.. code-block:: bash

    $ conan install --profile /abs/path/to/profile  # abs path
    $ conan install --profile ./relpath/to/profile  # resolved to current dir
    $ conan install --profile profile  # resolved to user/.conan/profiles/profile

Listing existing profiles can be done like this:

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

Use ``$PROFILE_DIR`` in your profile and it will be replaced with the absolute path to the profile file. It is useful to declare relative
folders:

.. code-block:: text

    [env]
    PYTHONPATH=$PROFILE_DIR/my_python_tools

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

In a profile you can declare variables that will be replaced automatically by conan before the profile is applied. The variables have to be
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

If you are working with Linux and you usually work with ``gcc`` compiler, but you have installed ``clang`` compiler and want to install some
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

- Execute conan install command passing the ``--profile`` or ``-pr`` parameter:

.. code-block:: bash

   conan install --profile clang

Without profiles you would have needed to set the CC and CXX variables in the environment to point to your clang compiler and use ``-s``
parameters to specify the settings:

.. code-block:: bash

   export CC=/usr/bin/clang
   export CXX=/usr/bin/clang++
   conan install -s compiler=clang -s compiler.version=3.5 -s compiler.libcxx=libstdc++11

A profile can also be used in :command:`conan create` and :command:`conan info`:

.. code-block:: bash

   $ conan create demo/testing --profile clang

.. seealso::

    - Check the section :ref:`build_requires` to read more about its ussage in a profile.
    - Check :ref:`conan_profile_command` for full reference.
    - Check :ref:`default_profile` for full reference.
    - Related section: :ref:`cross_building`.
