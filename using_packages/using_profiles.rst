.. _using_profiles:

Using profiles
--------------

So far we have used the default settings stored in ``~/.conan/profiles/default`` and defined as command line arguments.

However, configurations can be large, settings can be very different, and we might want to switch easily between different configurations
with different settings, options, etc.. The best way to this is using profiles.

A profile file contains a predefined set of ``settings``, ``options``, ``environment variables``, and ``build_requires`` and has this
structure:

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

Options allow definition with wildcards, to apply same option value to many packages:

.. code-block:: text

    [options]
    *:shared=True

They would contain the desired configuration, for example:

.. code-block:: text
   :caption: myprofile

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

    $ conan create demo/testing -pr=myprofile

You can use ``$PROFILE_DIR`` in your profile and it will be replaced with the absolute path to the profile file.
It is useful to declare relative folders:

.. code-block:: text

   [env]
   PYTHONPATH=$PROFILE_DIR/my_python_tools

.. note::

    If you specify a profile in a conan command, like `conan create` or `conan install` the base profile ``~/.conan/profiles/default`` won't
    be applied.

If we continue with the example of Poco, we could have a handy profile to help us build our project with the desired configuration and avoid
the ussage of all the command line arguments when installing the dependency packages.

A profile to build our depenencies as **shared** and and in **debug** mode will look like this:

.. code-block:: text
   :caption: *poco_debug_shared_profile*


    [settings]
    build_type=Debug

    [options]
    Poco:shared=True
    OpenSSL:shared=True

With this we could just install using the profile:

.. code-block:: bash

    $ conan install . -pr=poco_debug_shared_profile

We could also create a new profile to use a different compiler in a different OS, even use release as build type and store it in our project
directory:

.. code-block:: text
   :caption: *poco_apple_clang*


    [settings]
    os=Macos
    arch=x86_64
    compiler=apple-clang
    compiler.version=8.1
    compiler.libcxx=libc++
    build_type=Release

    [options]
    *:shared=True

Installation will be as easy as:

.. code-block:: bash

    $ conan install . -pr=./poco_apple_clang

.. seealso::

    Read more about :ref:`profiles` for full reference.
