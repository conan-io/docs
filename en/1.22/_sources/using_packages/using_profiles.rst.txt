.. _using_profiles:

Using profiles
--------------

So far, we have used the default settings stored in ``~/.conan/profiles/default`` and defined custom values for some of them as command line arguments.

However, in large projects, configurations can get complex, settings can be very different, and we need an easy way to switch between different configurations with different settings, options etc.
An easy way to switch between configurations is by using profiles.

A profile file contains a predefined set of ``settings``, ``options``, ``environment variables``, and ``build_requires`` specified in the following structure:

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

Options allow the use of wildcards letting you apply the same option value to many packages. For example:

.. code-block:: text

    [options]
    *:shared=True

Here is an example of a configuration that a profile file may contain:

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

A profile file can be stored in the default profile folder, or anywhere else in your project file structure. To use the configuration specified in a profile file, pass in the file as a command line argument as shown in the example below:

.. code-block:: bash

    $ conan create . demo/testing -pr=clang_3.5

Continuing with the example of Poco, instead of passing in a long list of command line arguments, we can define a handy profile that defines them all and pass that to the command line when installing the project dependencies.

A profile to install dependencies as **shared** and in **debug** mode would look like this:

.. code-block:: text
   :caption: *debug_shared*

    include(default)

    [settings]
    build_type=Debug

    [options]
    poco:shared=True
    poco:enable_apacheconnector=False
    openssl:shared=True

To install dependencies using the profile file, we would use:

.. code-block:: bash

    $ conan install .. -pr=debug_shared

We could also create a new profile to use a different compiler version and store that in our project directory. For example:

.. code-block:: text
   :caption: *poco_clang_3.5*

    include(clang_3.5)

    [options]
    poco:shared=True
    poco:enable_apacheconnector=False
    openssl:shared=True

To install dependencies using this new profile, we would use:

.. code-block:: bash

    $ conan install .. -pr=../poco_clang_3.5

You can specify multiple profiles in the command line. The applied configuration will be the composition
of all the profiles applied in the order they are specified:

.. code-block:: bash

    $ conan install .. -pr=../poco_clang_3.5 -pr=my_build_tool1 -pr=my_build_tool2

.. seealso::

    Read more about :ref:`profiles` for full reference. There is a Conan command, :ref:`conan_profile`,
    that can help inspecting and managing profiles. Profiles can be also shared and installed with the
    :ref:`conan_config_install` command.
