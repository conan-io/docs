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
    # [env] is deprecated! Use [buildenv] instead
    env_var=value

    [tool_requires]
    tool1/0.1@user/channel
    tool2/0.1@user/channel, tool3/0.1@user/channel
    *: tool4/0.1@user/channel

Profile can be created with ``new`` option in :command:`conan profile`. And then edit it later.

.. code-block:: bash

    $ conan profile new mynewprofile --detect

Profile files can be used with ``-pr``/``--profile`` option in many commands like :command:`conan install` or :command:`conan create` commands.

.. code-block:: bash

    $ conan create . demo/testing -pr=myprofile

Profiles can be located in different folders. For example, the default *<userhome>/.conan/profiles*, and be referenced by absolute or
relative path:

.. code-block:: bash

    $ conan install . --profile /abs/path/to/profile   # abs path
    $ conan install . --profile ./relpath/to/profile   # resolved to current dir
    $ conan install . --profile ../relpath/to/profile  # resolved to relative dir
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
    [tool_requires]
    [env]

Use ``$PROFILE_DIR`` in your profile and it will be replaced with the absolute path to
the directory where the profile file is (this path will contain only forward slashes).
It is useful to declare relative folders:

.. code-block:: text

    [env]
    PATH=$PROFILE_DIR/dev_tools

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

They accept patterns too, like ``-s *@myuser/*``, which means that packages that have the username "myuser" will use clang 3.5 as compiler, and gcc otherwise:

.. code-block:: text

    [settings]
    *@myuser/*:compiler=clang
    *@myuser/*:compiler.version=3.5
    *@myuser/*:compiler.libcxx=libstdc++11
    compiler=gcc
    compiler.version=4.9
    compiler.libcxx=libstdc++11

Also `&` can be specified as the package name. It will apply only to the consumer conanfile (.py or .txt).
This is a special case because the consumer conanfile might not declare a `name` so it would be impossible to reference it.

.. code-block:: text

    [settings]
    &:compiler=gcc
    &:compiler.version=4.9
    &:compiler.libcxx=libstdc++11

.. note::

    If you want to override existing system environment variables, you should use the ``key=value`` syntax. If you need to pre-pend to the
    system environment variables you should use the syntax ``key=[value]`` or ``key=[value1, value2, ...]``. A typical example is the
    ``PATH`` environment variable, when you want to add paths to the existing system PATH, not override it, you would use:

    .. code-block:: text

        [env]
        PATH=[/some/path/to/my/tool]

.. _profiles_buildenv:

[buildenv]
++++++++++

Available since: `1.35.0 <https://github.com/conan-io/conan/releases/tag/1.35.0>`_

.. important::

    The use of this ``[buildenv]`` section requires using the ``VirtualBuildEnv`` generator in your recipe,
    or putting the configuration ``tools.env.virtualenv:auto_use=True`` in your profile.


This profile section is aimed to be the replacement of the legacy ``[env]`` one. It's more powerful, and it is able to
apply some additional operators to each variable declared when you're composing profiles or even local variables:

* ``+=`` == ``append``: appends values at the end of the existing value.
* ``=+`` == ``prepend``: puts values at the beginning of the existing value.
* ``=!`` == ``unset``: gets rid of any variable value.

Another essential point to mention is the possibility of defining variables as `PATH` ones by simply putting ``(path)`` as
the prefix of the variable. It is useful to automatically get the append/prepend of the `PATH` in different systems
(Windows uses ``;`` as separation, and UNIX ``:``).


.. code-block:: text
    :caption: *.conan/profiles/myprofile*

    [buildenv]
    # Define a variable "MyVar1"
    MyVar1=My Value; other

    # Append another value to "MyVar1"
    MyVar1+=MyValue12

    # Define a PATH variable "MyPath1"
    MyPath1=(path)/some/path11

    # Prepend another PATH to "MyPath1"
    MyPath1=+(path)/other path/path12

    # Unset the variable "PATH" for all the packages matching the pattern "mypkg*"
    mypkg*:PATH=!


Then, the result of applying this profile is:

* ``MyVar1``: ``My Value; other MyValue12``
* ``MyPath1``:
    * Unix: ``/other path/path12:/some/path11``
    * Windows: ``/other path/path12;/some/path11``
* ``mypkg*:PATH``: ``None``


See more information about the new environments in the :ref:`conan_tools_env` reference.


.. _profiles_runenv:

[runenv]
++++++++++

Available since: `1.53.0 <https://github.com/conan-io/conan/releases/tag/1.53.0>`_

.. important::

    The use of this ``[runenv]`` section requires using the ``VirtualRunEnv`` generator in your recipe.

This profile section allows defining environment variables that will be injected to the
environment every time the ConanFile ``run(cmd, env="conanrun")`` method is invoked. You can use the same
operators explained for the :ref:`profiles_buildenv` section and also define `PATH`
variables.

.. _profiles_tools_conf:

Tools configurations
--------------------

.. important::

    This feature is still **under development**, while it is recommended and usable and we will try not to break them in future releases,
    some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.

Tools configurations can also be used in profile files and *global.conf* one. Profile values will have priority over globally defined ones in *global.conf*, and can be defined as:

.. code-block:: text

    [settings]
    ...

    [conf]
    tools.microsoft.msbuild:verbosity=Diagnostic
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10

.. seealso::

    You can see more information about configurations in :ref:`global.conf section <global_conf>`.


Profile composition
-------------------

You can specify multiple profiles in the command line. The applied configuration will be the composition
of all the profiles applied in the order they are specified.

If, for example, you want to apply a :ref:`tool require<build_requires>`, like a ``cmake`` installer to your dependency tree,
it won't be very practical adding the `cmake` installer reference, e.g  ``cmake/3.16.3`` to all your profiles where you could
need to inject ``cmake`` as a tool require.

You can specify both profiles instead:

.. code-block:: text
   :caption: *.conan/profiles/cmake_316*

    [tool_requires]
    cmake/3.16.3

.. code-block:: bash

   $ conan install . --profile clang --profile cmake_316

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


.. _build_profiles_and_host_profiles:

Build profiles and host profiles
--------------------------------


All the commands that take a profile as an argument, from Conan v1.24 are starting to accept two profiles with
command line arguments ``-pr:h``/``--profile:host`` and ``-pr:b``/``--profile:build``. If both profiles are
provided, Conan will build a graph with some packages associated with the ``host`` platform and some build
requirements associated to the ``build`` platform. There are two scenarios where this feature is
extremely useful:

* :ref:`create_installer_packages`
* :ref:`cross_building`

The default build profile in Conan 1.X is not defined by default, and needs to be specified in command line.
However, it is also possible to define a default one in ``global.conf`` configuration file with:

.. code-block:: text
   :caption: *global.conf*

    core:default_build_profile=default
    core:default_profile=linux_armv8

The default host profile can be defaulted as well using this configuration method.


Profile templates
-----------------

.. important::

    This feature is still **under development**, while it is recommended and usable and we will try not to break them in future releases,
    some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.


From Conan 1.38 it is possible to use **jinja2** template engine for profiles. This feature is
enabled by naming the profile file with the ``.jinja`` extension. When Conan loads a profile with
this extension, immediately parses and renders the template, which must result in a standard
text profile.

Some of the capabilities of the profile templates are:

- Using the platform information, like obtaining the current OS is possible because the
  Python ``platform`` module is added to the render context.:

  .. code:: jinja

     [settings]
     os = {{ {"Darwin": "Macos"}.get(platform.system(), platform.system()) }}

- Reading environment variables can be done because the Python ``os`` module is added
  to the render context.:

  .. code:: jinja

     [settings]
     build_type = {{ os.getenv("MY_BUILD_TYPE") }}

- Defining your own variables and using them in the profile:

  .. code:: jinja

     {% set a = "FreeBSD" %}
     [settings]
     os = {{ a }}

- Joining and defining paths, including referencing the current profile directory. For
  example, defining a toolchain which file is located besides the profile can be done.
  Besides the ``os`` Python module, the variable ``profile_dir`` pointing to the current profile
  folder is added to the context.

  .. code:: jinja

       [conf]
       tools.cmake.cmaketoolchain:toolchain_file = {{ os.path.join(profile_dir, "toolchain.cmake") }}

- Including or importing other files from ``profiles`` folder:

  .. code-block:: jinja
     :caption: profile_vars.jinja

     {% set a = "Debug" %}

  .. code-block:: jinja
     :caption: profile1.jinja

     {% import "profile_vars.jinja" as vars %}
     [settings]
     build_type = {{ vars.a }}

- Any other feature supported by *jinja2* is possible: for loops, if-else, etc. This
  would be useful to define custom per-package settings or options for multiple packages
  in a large dependency graph.

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
