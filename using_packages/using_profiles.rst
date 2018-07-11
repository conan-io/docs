.. _using_profiles:

Using profiles
--------------

So far we have used the default settings stored in ``~/.conan/profiles/default`` and defined as command line arguments.

However, configurations can be large, settings can be very different, and we might want to switch easily between different configurations
with different settings, options, etc. The best way to do it is using profiles.

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
   :caption: *clang_3.5*

    [settings]
    os=Macos
    arch=x86_64
    compiler=clang
    compiler.version=3.5
    compiler.libcxx=libstdc++11
    build_type=Release

    [env]
    CC=/usr/bin/clang
    CXX=/usr/bin/clang++

You can store them in the default profile folder or anywhere in you project and you can use it instead of command line arguments:

.. code-block:: bash

    $ conan create demo/testing -pr=clang_3.5

If we continue with the example of Poco, we could have a handy profile to help us build our project with the desired configuration and avoid
the usage of all the command line arguments when installing the dependency packages.

A profile to install dependencies as **shared** and in **debug** mode will look like this:

.. code-block:: text
   :caption: *debug_shared*

    include(default)

    [settings]
    build_type=Debug

    [options]
    Poco:shared=True
    Poco:enable_apacheconnector=False
    OpenSSL:shared=True

With this we could just install using the profile:

.. code-block:: bash

    $ conan install . -pr=debug_shared

We could also create a new profile to use a different compiler version and store it in our project directory:

.. code-block:: text
   :caption: *poco_clang_3.5*

    include(clang_3.5)

    [options]
    Poco:shared=True
    Poco:enable_apacheconnector=False
    OpenSSL:shared=True

Installation will be as easy as:

.. code-block:: bash

    $ conan install . -pr=./poco_clang_3.5

.. seealso::

    Read more about :ref:`profiles` for full reference.
