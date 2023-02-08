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
    arch=x86_64
    build_type=Release
    os=Macos

    [options]
    MyLib:shared=True

    [buildenv]
    VAR1=value

    [tool_requires]
    tool1/0.1@user/channel
    *: tool4/0.1@user/channel

    [conf]
    tools.build:jobs=2


Profiles can be created with ``detect`` option in :ref:`conan profile <reference_commands_profile>` command,
and edited later.

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

    $ conan create . -pr=myprofile


Profiles can be located in different folders. For instance, the default *[CONAN_HOME]/profiles* could be referenced by absolute or
relative path:

.. code-block:: bash

    $ conan install . -pr /abs/path/to/myprofile   # abs path
    $ conan install . -pr ./relpath/to/myprofile   # resolved to current dir
    $ conan install . -pr ../relpath/to/myprofile  # resolved to relative dir
    $ conan install . -pr myprofile  # resolved to [CONAN_HOME]/profiles/myprofile

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


.. seealso::

    - Manage your profiles and share them using :ref:`reference_commands_conan_config_install`.
    - Check the command :ref:`conan profile <reference_commands_profile>`.


Sections in profiles
--------------------

These are the available sections in profiles:

[settings]
++++++++++

List of settings available from settings.yml:

.. code-block:: text
    :caption: *myprofile*

    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=Macos


[options]
++++++++++

List of options available from your recipe and its dependencies:

.. code-block:: text
    :caption: *myprofile*

    [options]
    my_pkg_option=True
    zlib:shared=True


[tool_requires]
+++++++++++++++

List of ``tool_requires`` required by your recipe or its dependencies:

.. code-block:: text
    :caption: *myprofile*

    [tool_requires]
    cmake/3.25.2
    zlib:cmake/3.20.6


.. seealso::

    Read more about tool requires in this section: :ref:`consuming_packages_tool_requires`.


.. _reference_config_files_profiles_buildenv:

[buildenv]
++++++++++

List of environment variables that will be injected to the environment every time the ConanFile
``run(cmd, env="conanbuild")`` method is invoked (build time context and automatically run by :ref:`conan_tools_env_virtualbuildenv`).

Besides that, it is able to apply some additional operators to each variable declared
when you're composing profiles or even local variables:

* ``+=`` == ``append``: appends values at the end of the existing value.
* ``=+`` == ``prepend``: puts values at the beginning of the existing value.
* ``=!`` == ``unset``: gets rid of any variable value.

Another essential point to mention is the possibility of defining variables as `PATH` ones by simply putting ``(path)`` as
the prefix of the variable. It is useful to automatically get the append/prepend of the `PATH` in different systems
(Windows uses ``;`` as separation, and UNIX ``:``).


.. code-block:: text
    :caption: *myprofile*

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



.. _reference_config_files_profiles_runenv:

[runenv]
++++++++++

List of environment variables that will be injected to the environment every time the ConanFile
``run(cmd, env="conanrun")`` method is invoked (build time context and automatically run by :ref:`conan_tools_env_virtualrunenv`).


All the operators/patterns explained for :ref:`reference_config_files_profiles_buildenv` applies to this one in the same way:

.. code-block:: text
    :caption: *myprofile*

    [runenv]
    MyVar1=My Value; other
    MyVar1+=MyValue12
    MyPath1=(path)/some/path11
    MyPath1=+(path)/other path/path12
    mypkg*:PATH=!


[conf]
++++++

List of user/tools configurations. They can also be used in :ref:`reference_config_files_global_conf` too.
**Profile values will have priority over globally defined ones in global.conf**, and can be defined as:

.. code-block:: text
    :caption: *myprofile*

    [conf]
    tools.microsoft.msbuild:verbosity=Diagnostic
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10


Profile patterns
----------------

Profiles also support patterns definition, so you can override some settings, configuration variables, etc.
for some specific packages:

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
