.. _reference_config_files_default_profile:

profiles/default
================

The **default** profile file is located in the Conan user home *profiles* directory, e.g., *[CONAN_HOME]/profiles/default*.

Introduction to profiles
------------------------

Conan profiles allow users to set a complete configuration set for **settings**, **options**,
**environment variables** (for build time and runtime context), **requirements** (and tool requirements), and
**configuration variables** in a file.

They have this structure:

.. code-block:: text

    [settings]
    setting=value

    [options]
    MyLib:shared=True

    [buildenv]
    env_var=value

    [tool_requires]
    tool1/0.1@user/channel
    tool2/0.1@user/channel, tool3/0.1@user/channel
    *: tool4/0.1@user/channel


Profiles can be created with ``detect`` option in :command:`conan profile`, and edited later.

.. code-block:: bash

    $ conan profile detect --name myprofile
    Found apple-clang 12.0
    Detected profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=Macos

    WARN: This profile is a guess of your environment, please check it.
    WARN: The output of this command is not guaranteed to be stable and can change in future Conan versions
    Saving detected profile to /Users/myuser/.conan2/profiles/myprofile


Profile files can be used with ``-pr``/``--profile`` option in many commands like :command:`conan install` or
:command:`conan create` commands.

.. code-block:: bash

    $ conan create . demo/testing -pr=myprofile

.. note::

    Remember that ``-pr``/``--profile`` refers to ``host`` context by default. You can use ``-pr:h``/``-pr:b`` to use
    host/build context respectively.


Profiles can be located in different folders. For instance, the default *[CONAN_HOME]/profiles* could be referenced by absolute or
relative path:

.. code-block:: bash

    $ conan install . -pr /abs/path/to/profile   # abs path
    $ conan install . -pr ./relpath/to/profile   # resolved to current dir
    $ conan install . -pr ../relpath/to/profile  # resolved to relative dir
    $ conan install . -pr profile  # resolved to [CONAN_HOME]/profiles/profile

Listing existing profiles in the *profiles* folder can be done like this:

.. code-block:: bash

    $ conan profile list
    Profiles found in the cache:
    default
    myprofile1
    myprofile2
    ...

You can also show profile's content:

.. code-block:: bash

    $ conan profile show
    Host profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=Macos

    Build profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=Macos


.. tip::

    You can manage your profiles and share them using :ref:`reference_commands_conan_config_install`.


Profile patterns
----------------

Profiles also support patterns definition, so you can override some settings, configuration and environment variables
for some specific package:

.. code-block:: text
    :caption: *[CONAN_HOME]/profiles/zlib_with_clang*

    [settings]
    # Only for zlib
    zlib:compiler=clang
    zlib:compiler.version=3.5
    zlib:compiler.libcxx=libstdc++11
    # For the all the dependency tree
    compiler=gcc
    compiler.version=4.9
    compiler.libcxx=libstdc++11

    [buildenv]
    # For the all the dependency tree
    *:MYVAR=my_var

    [conf]
    # Only for zlib
    zlib:tools.build:compiler_executables={'c': '/usr/bin/clang', 'cpp': '/usr/bin/clang++'}


Your build tool will locate **clang**/**clang++** compiler only for the **zlib** package and **gcc** (default one)
for the rest of your dependency tree.

They accept patterns too, like ``-s *@myuser/*``, which means that packages that have the username "myuser" will use
clang 3.5 as compiler, and gcc otherwise:

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


.. _profiles_buildenv:

[buildenv]
++++++++++

Available since: `1.35.0 <https://github.com/conan-io/conan/releases/tag/1.35.0>`_

.. important::

    The use of this ``[buildenv]`` section requires using the ``VirtualBuildEnv`` generator in your recipe,
    or putting the configuration ``tools.env.virtualenv:auto_use=True`` in your profile.


This profile section is aimed to be the replacement of the legacy ``[buildenv]`` one. It's more powerful, and it is able to
apply some additional operators to each variable declared when you're composing profiles or even local variables:

* ``+=`` == ``append``: appends values at the end of the existing value.
* ``=+`` == ``prepend``: puts values at the beginning of the existing value.
* ``=!`` == ``unset``: gets rid of any variable value.

Another essential point to mention is the possibility of defining variables as `PATH` ones by simply putting ``(path)`` as
the prefix of the variable. It is useful to automatically get the append/prepend of the `PATH` in different systems
(Windows uses ``;`` as separation, and UNIX ``:``).


.. code-block:: text
    :caption: *[CONAN_HOME]/profiles/myprofile*

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

See more information about the new environments in the :ref:`reference_tools_env` reference.

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

    You can see more information about configurations in :ref:`global.conf section <reference_config_files_global_conf>`.


Profile composition
-------------------

You can specify multiple profiles in the command line. The applied configuration will be the composition
of all the profiles applied in the order they are specified.

If, for example, you want to apply a :ref:`tool require<reference_conanfile_attributes_build_requires>`, like a ``cmake``
installer to your dependency tree, it won't be very practical adding the `cmake` installer reference, e.g,
``cmake/3.16.3`` to all your profiles where you could need to inject ``cmake`` as a tool require.

You can specify both profiles instead:

.. code-block:: text
   :caption: *[CONAN_HOME]/profiles/cmake_316*

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

    [conf]
    zlib:tools.build:compiler_executables={'c': '/usr/bin/clang', 'cpp': '/usr/bin/clang++'}


Profile templates
-----------------

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



.. _build_profiles_and_host_profiles:

Build profiles and host profiles
--------------------------------

All the commands that take a profile as an argument, from Conan v1.24 are starting to accept two profiles with
command line arguments ``-pr:h``/``--profile:host`` and ``-pr:b``/``--profile:build``. If both profiles are
provided, Conan will build a graph with some packages associated with the ``host`` platform and some build
requirements associated to the ``build`` platform. There are two scenarios where this feature is
extremely useful:

* :ref:`tutorial_other_tool_requires_packages`
* :ref:`consuming_packages_cross_building_with_conan`

The default build profile in Conan 1.X is not defined by default, and needs to be specified in command line.
However, it is also possible to define a default one in ``global.conf`` configuration file with:

.. code-block:: text
   :caption: *global.conf*

    core:default_build_profile=default
    core:default_profile=linux_armv8

The default host profile can be defaulted as well using this configuration method.


.. seealso::

    - Check the section :ref:`consuming_packages_tool_requires` to read more about its usage in a profile
