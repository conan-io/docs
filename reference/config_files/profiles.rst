.. _reference_config_files_profiles:

profiles
========

Introduction to profiles
------------------------

Conan profiles allow users to set a complete configuration set for **settings**, **options**,
**environment variables** (for build time and runtime context), **tool requirements**, and
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


Profiles can be created with the ``detect`` option in :ref:`conan profile <reference_commands_profile>` command,
and edited later. If you don't specify a *name*, the command will create the ``default`` profile:


.. code-block:: bash
    :caption: *Creating the Conan default profile*

    $ conan profile detect
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
    Saving detected profile to [CONAN_HOME]/profiles/default

.. code-block:: bash
    :caption: *Creating another profile: myprofile*

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
    Saving detected profile to [CONAN_HOME]/profiles/myprofile


Profile files can be used with ``-pr``/``--profile`` option in many commands like :command:`conan install` or
:command:`conan create` commands. If you don't specify any profile at all, the ``default`` profile will be
always used:

.. code-block:: bash
    :caption: Using the *default* profile

    $ conan create .


.. code-block:: bash
    :caption: Using a *myprofile* profile

    $ conan create . -pr=myprofile


Profiles can be located in different folders:

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

You can also show the profile's content per context:

.. code-block:: bash

    $ conan profile show -pr myprofile
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
    - Check the command and its sub-comands of :ref:`conan profile <reference_commands_profile>`.


Profile sections
----------------

These are the available sections in profiles:

[settings]
++++++++++

List of settings available from :ref:`reference_config_files_settings_yml`:

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
    shared=True


[tool_requires]
+++++++++++++++

List of ``tool_requires`` required by your recipe or its dependencies:

.. code-block:: text
    :caption: *myprofile*

    [tool_requires]
    cmake/3.25.2

.. seealso::

    Read more about tool requires in this section: :ref:`consuming_packages_tool_requires`.


.. _reference_config_files_profiles_buildenv:

[buildenv]
++++++++++

List of environment variables that will be injected to the environment every time the ConanFile
``run(cmd, env="conanbuild")`` method is invoked (build time context is automatically run by :ref:`conan_tools_env_virtualbuildenv`).

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

    # Unset the variable "MyPath1"
    MyPath1=!


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
``run(cmd, env="conanrun")`` method is invoked (runtime context is automatically run by :ref:`conan_tools_env_virtualrunenv`).


All the operators/patterns explained for :ref:`reference_config_files_profiles_buildenv` applies to this one in the same way:

.. code-block:: text
    :caption: *myprofile*

    [runenv]
    MyVar1=My Value; other
    MyVar1+=MyValue12
    MyPath1=(path)/some/path11
    MyPath1=+(path)/other path/path12
    MyPath1=!

.. _reference_config_files_profiles_conf:

[conf]
++++++

.. note::

    It's recommended to have previously read the :ref:`reference_config_files_global_conf` section.

List of user/tools configurations:

.. code-block:: text
    :caption: *myprofile*

    [conf]
    tools.microsoft.msbuild:verbosity=Diagnostic
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10
    # User conf variable
    user.confvar:something=False


They can also be used in :ref:`reference_config_files_global_conf`,
but **profiles values will have priority over globally defined ones in global.conf**, so let's see an example that is a bit more complex,
trying different configurations coming from the *global.conf* and another profile *myprofile*:


.. code-block:: text
    :caption: *global.conf*

    # Defining several lists
    user.myconf.build:ldflags=["--flag1 value1"]
    user.myconf.build:cflags=["--flag1 value1"]


.. code-block:: text
    :caption: *myprofile*

    [settings]
    ...

    [conf]
    # Appending values into the existing list
    user.myconf.build:ldflags+=["--flag2 value2"]

    # Unsetting the existing value (it'd be like we define it as an empty value)
    user.myconf.build:cflags=!

    # Prepending values into the existing list
    user.myconf.build:ldflags=+["--prefix prefix-value"]


Running, for instance, :command:`conan install . -pr myprofile`, the configuration output will be something like:

.. code-block:: bash

    ...
    Configuration:
    [settings]
    [options]
    [tool_requires]
    [conf]
    user.myconf.build:cflags=!
    user.myconf.build:ldflags=['--prefix prefix-value', '--flag1 value1', '--flag2 value2']
    ...


Profile rendering
-----------------

The profiles are rendered as **jinja2** templates by default. When Conan loads a profile, it immediately parses and
renders the template, which must result in a standard text profile.

Some of the capabilities of the profile templates are:

- Using the platform information, like obtaining the current OS, is possible because the
  Python ``platform`` module is added to the render context:

  .. code-block:: jinja
     :caption: *profile_vars*

     [settings]
     os = {{ {"Darwin": "Macos"}.get(platform.system(), platform.system()) }}

- Reading environment variables can be done because the Python ``os`` module is added
  to the render context:

  .. code-block:: jinja
     :caption: *profile_vars*

     [settings]
     build_type = {{ os.getenv("MY_BUILD_TYPE") }}

- Defining your own variables and using them in the profile:

  .. code-block:: jinja
     :caption: *profile_vars*

     {% set os = "FreeBSD" %}
     {% set clang = "my/path/to/clang" %}

     [settings]
     os = {{ os }}

     [conf]
     tools.build:compiler_executables={'c': '{{ clang }}', 'cpp': '{{ clang + '++' }}' }


- Joining and defining paths, including referencing the current profile directory. For
  example, defining a toolchain whose file is located besides the profile can be done.
  Besides the ``os`` Python module, the variable ``profile_dir`` pointing to the current profile
  folder is added to the context.

  .. code-block:: jinja
     :caption: *profile_vars*

     [conf]
     tools.cmake.cmaketoolchain:toolchain_file = {{ os.path.join(profile_dir, "toolchain.cmake") }}

- Including or importing other files from ``profiles`` folder:

  .. code-block:: jinja
     :caption: *profile_vars*

     {% set a = "Debug" %}

  .. code-block:: jinja
     :caption: *myprofile*

     {% import "profile_vars" as vars %}
     [settings]
     build_type = {{ vars.a }}

- Any other feature supported by *jinja2* is possible: for loops, if-else, etc. This
  would be useful to define custom per-package settings or options for multiple packages
  in a large dependency graph.


Profile patterns
----------------

Profiles also support patterns definition, so you can override some settings, configuration variables, etc.
for some specific packages:

.. code-block:: text
    :caption: *zlib_clang_profile*

    [settings]
    # Only for zlib
    zlib*:compiler=clang
    zlib*:compiler.version=3.5
    zlib*:compiler.libcxx=libstdc++11

    # For the all the dependency tree
    compiler=gcc
    compiler.version=4.9
    compiler.libcxx=libstdc++11

    [options]
    # shared=True option only for zlib package
    zlib*:shared=True

    [buildenv]
    # For the all the dependency tree
    *:MYVAR=my_var

    [conf]
    # Only for zlib
    zlib*:tools.build:compiler_executables={'c': '/usr/bin/clang', 'cpp': '/usr/bin/clang++'}


Your build tool will locate **clang** compiler only for the **zlib** package and **gcc** (default one)
for the rest of your dependency tree.

.. important::

    Putting only ``zlib:`` is not going to work, you have to always put a pattern-like expression, e.g., ``zlib*:``, ``zlib/1.*:``, etc.


They accept patterns too, like ``-s *@myuser/*``, which means that packages that have the username "myuser" will use
clang 3.5 as compiler, and gcc otherwise:

.. code-block:: text
    :caption: *myprofile*

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
    :caption: *myprofile*

    [settings]
    &:compiler=gcc
    &:compiler.version=4.9
    &:compiler.libcxx=libstdc++11


Profile includes
----------------

You can include other profile files using the ``include()`` statement. The path can be relative
to the current profile, absolute, or a profile name from the default profile location in the local cache.

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
    zlib*:compiler=clang
    zlib*:compiler.version=3.5
    zlib*:compiler.libcxx=libstdc++11


The final result of using *myprofile* is:

.. code-block:: text
    :caption: *myprofile (virtual result)*

    [settings]
    compiler=gcc
    compiler.libcxx=libstdc++11
    compiler.version=4.9
    zlib*:compiler=clang
    zlib*:compiler.libcxx=libstdc++11
    zlib*:compiler.version=3.5


.. seealso::

    - :ref:`How to compose two or more profiles <reference_commands_install_composition>`