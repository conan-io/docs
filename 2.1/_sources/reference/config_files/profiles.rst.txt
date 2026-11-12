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

    [tool_requires]
    tool1/0.1@user/channel
    *: tool4/0.1@user/channel

    [buildenv]
    VAR1=value

    [runenv]
    EnvironmentVar1=My Value

    [conf]
    tools.build:jobs=2

    [replace_requires]
    zlib/1.2.123: zlib/*

    [replace_tool_requires]
    7zip/*: 7zip/system

    [platform_requires]
    dlib/1.3.22

    [platform_tool_requires]
    cmake/3.24.2

Profiles can be created with the ``detect`` option in :ref:`conan profile <reference_commands_profile>` command,
and edited later. If you don't specify a *name*, the command will create the ``default`` profile:


.. code-block:: bash
    :caption: *Creating the Conan default profile*

    $ conan profile detect
    apple-clang>=13, using the major as version
    Detected profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos

    WARN: This profile is a guess of your environment, please check it.
    WARN: Defaulted to cppstd='gnu17' for apple-clang.
    WARN: The output of this command is not guaranteed to be stable and can change in future Conan versions.
    WARN: Use your own profile files for stability.
    Saving detected profile to [CONAN_HOME]/profiles/default


.. note:: **A note about the detected C++ standard by Conan**

    Conan will always set the default C++ standard as the one that the detected compiler
    version uses by default, except for the case of macOS using apple-clang. In this case,
    for apple-clang>=11, it sets ``compiler.cppstd=gnu17``. If you want to use a different
    C++ standard, you can edit the default profile file directly.


.. code-block:: bash
    :caption: *Creating another profile: myprofile*

    $ conan profile detect --name myprofile
    Found apple-clang 14.0
    apple-clang>=13, using the major as version
    Detected profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos

    WARN: This profile is a guess of your environment, please check it.
    WARN: Defaulted to cppstd='gnu17' for apple-clang.
    WARN: The output of this command is not guaranteed to be stable and can change in future Conan versions.
    WARN: Use your own profile files for stability.
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
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos

    Build profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos


.. seealso::

    - Manage your profiles and share them using :ref:`reference_commands_conan_config_install`.
    - Check the command and its sub-commands of :ref:`conan profile <reference_commands_profile>`.


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
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos


[options]
+++++++++

List of options available from your recipe and its dependencies:

.. code-block:: text
    :caption: *myprofile*

    [options]
    my_pkg_option=True
    shared=True


.. _reference_config_files_profiles_tool_requires:

[tool_requires]
+++++++++++++++

List of ``tool_requires`` required by your recipe or its dependencies:

.. code-block:: text
    :caption: *myprofile*

    [tool_requires]
    cmake/3.25.2

.. seealso::

    Read more about tool requires in this section: :ref:`consuming_packages_tool_requires`.


.. _reference_config_files_profiles_system_tools:

[system_tools] (DEPRECATED)
+++++++++++++++++++++++++++

.. note::

    This section is **deprecated** and  has been replaced by :ref:`reference_config_files_profiles_platform_requires` and :ref:`reference_config_files_profiles_platform_tool_requires` sections.


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
++++++++

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
    tools.build:verbosity=verbose
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10
    # User conf variable
    user.confvar:something=False

Recall some hints about configuration scope and naming:

- ``core.xxx`` configuration can only be defined in ``global.conf`` file, but not in profiles
- ``tools.yyy`` and ``user.zzz`` can be defined in ``global.conf`` and they will affect both the "build" and the "host" context. But configurations defined in a profile ``[conf]`` will only affect the respective "build" or "host" context of the profile, not both.

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


.. _reference_config_files_profiles_replace_requires:

[replace_requires]
++++++++++++++++++

.. include:: ../../common/experimental_warning.inc

This section allows the user to redefine requires of recipes. This can be useful when a package can be changed by a similar one like `zlib` and `zlibng`.
It is also useful to solve conflicts, or to replace some dependencies by system alternatives wrapped in another Conan package recipe.

References listed under this section work as a **literal replacement of requires in recipes**, and is done as the very first step before any other processing
of recipe requirements, without processing them or checking for conflicts.

As an example, we could define `zlibng` as a replacement for the typical `zlib`:abbr:

.. code-block:: text
    :caption: *myprofile*

    [replace_requires]
    zlib/*: zlibng/*

Using the ``*`` pattern for the ``zlibng`` reference means that ``zlib`` will be replaced by the exact same version of ``zlibng``.

Other examples are:

.. code-block:: text
    :caption: *myprofile*

    [replace_requires]
    dep/*: dep/1.1               # To override dep/[>=1.0 <2] in recipes to a specific version dep/1.1)
    dep/*: dep/*@system          # To override a dep/1.3 in recipes to dep/1.3@system
    dep/*: dep/[>=1 <2]          # To override every dep requirement in recipes to a specific version range
    dep/*@*/*: dep/*@system/*    # To override "dep/1.3@comp/stable" in recipes to the same version with other user but same channel
    dep/1.1: dep/1.1@system      # To replace exact reference in recipes by the same one in the system
    dep/1.1@*: dep/1.1@*/stable  # To replace dep/[>=1.0 <2]@comp version range in recipes by 1.1 version in stable chanel

.. note:: **Best practices**

   - Please make rational use of this feature. It is not a versioning mechanism and is not intended to replace actual requires in recipes.
   - The usage of this feature is intended for **temporarily** solving conflicts or replacing a specific dependency by a system one in some cross-build scenarios.


.. _reference_config_files_profiles_replace_tool_requires:

[replace_tool_requires]
+++++++++++++++++++++++

.. include:: ../../common/experimental_warning.inc

Same usage as the `replace_requires` section but in this case for `tool_requires`.

.. code-block:: text
    :caption: *myprofile*

    [replace_tool_requires]
    cmake/*: cmake/3.25.2

In this case, whatever version of ``cmake`` declared in recipes, will be replaced by the reference `cmake/3.25.2`.


.. _reference_config_files_profiles_platform_requires:

[platform_requires]
+++++++++++++++++++

.. include:: ../../common/experimental_warning.inc

This section allows the user to redefine requires of recipes replacing them with platform-provided dependencies, this means that Conan will not try to download the
reference or look for it in the cache and will assume that it is installed in your system and ready to be used.

For example, if the zlib 1.2.11 library is already installed in your system or it is part of your build toolchain and you would like Conan to use it,
you could specify so as:

.. code-block:: text
    :caption: *myprofile*

    [platform_requires]
    zlib/1.2.11


.. _reference_config_files_profiles_platform_tool_requires:

[platform_tool_requires]
++++++++++++++++++++++++

.. include:: ../../common/experimental_warning.inc

Same usage as the `platform_requires` section but in this case for `tool_requires` such as `cmake`, `meson`...

As an example, let's say you have already installed ``cmake==3.24.2`` in your system:

.. code-block:: bash

    $ cmake --version
    cmake version 3.24.2

    CMake suite maintained and supported by Kitware (kitware.com/cmake).

And you have in your recipe (or the transitive dependencies) declared a **tool_requires**, i.e., something like this:

.. code-block:: python
    :caption: **conanfile.py**

    from conan import ConanFile

    class PkgConan(ConanFile):
        name = "pkg"
        version = "2.0"
        # ....

        # Exact version
        def build_requirements(self):
            self.tool_requires("cmake/3.24.2")

        # Or even version ranges
        def build_requirements(self):
            self.tool_requires("cmake/[>=3.20.0]")

Given this situation, it could make sense to want to use your already installed CMake version, so it's enough to declare
it as a ``platform_tool_requires`` in your profile:

.. code-block:: text
    :caption: *myprofile*

    ...

    [platform_tool_requires]
    cmake/3.24.2

Whenever you want to create the package, you'll see that build requirement is already satisfied because of the platform tool
declaration:

.. code-block:: bash
    :emphasize-lines: 9,18

    $ conan create . -pr myprofile --build=missing
    ...
    -------- Computing dependency graph --------
    Graph root
        virtual
    Requirements
        pkg/2.0#3488ec5c2829b44387152a6c4b013767 - Cache
    Build requirements
        cmake/3.24.2 - Platform

    -------- Computing necessary packages --------

    -------- Computing necessary packages --------
    pkg/2.0: Forced build from source
    Requirements
        pkg/2.0#3488ec5c2829b44387152a6c4b013767:20496b332552131b67fb99bf425f95f64d0d0818 - Build
    Build requirements
        cmake/3.24.2 - Platform

Note that if the ``platform_tool_requires`` declared **does not make a strict match** with the ``tool_requires`` one (version or
version range), then Conan will try to bring them remotely or locally as usual.


.. _reference_config_files_profiles_rendering:

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

- Getting settings from a filename, including referencing the current profile name. For
  example, defining a generic profile which is configured according to its file name.
  The variable ``profile_name`` pointing to the current profile file name is added to the context.

  .. code-block:: jinja
     :caption: *Linux-x86_64-gcc-12*

     {% set os, arch, compiler, compiler_version = profile_name.split('-') %}
     [settings]
     os={{ os }}
     arch={{ arch }}
     compiler={{ compiler }}
     compiler.version={{ compiler_version }}

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

.. _reference_config_files_profiles_detect_api:

**Profile Rendering with ``detect_api``**

.. warning::

    **Stability Guarantees**: The detect_api, similar to ``conan profile detect``, does not
    offer strong stability guarantees.
    
    **Usage Recommendations**: The detect_api is not a regular API meant for creating new
    commands or similar functionalities. While auto-detection can be convenient, it's not
    the recommended approach for all scenarios. This API is internal to Conan and is only
    exposed for profile and *global.conf* rendering. It's advised to use it judiciously.

Conan also injects ``detect_api`` to the jinja rendering context. With it, it's
possible to use Conan's auto-detection capabilities directly within Jinja profile
templates. This provides a way to dynamically determine certain settings based on the
environment.

``detect_api`` can be invoked within the Jinja template of a profile. For instance, to
detect the operating system and architecture, you can use:

.. code-block:: jinja

    [settings]
    os={{detect_api.detect_os()}}
    arch={{detect_api.detect_arch()}}
  
Similarly, for more advanced detections like determining the compiler, its version, and
the associated runtime, you can use:

.. code-block:: jinja

    {% set compiler, version, compiler_exe = detect_api.detect_default_compiler() %}
    {% set runtime, _ = detect_api.default_msvc_runtime(compiler) %}
    [settings]
    compiler={{compiler}}
    compiler.version={{detect_api.default_compiler_version(compiler, version)}}
    compiler.runtime={{runtime}}
    compiler.cppstd={{detect_api.default_cppstd(compiler, version)}}
    compiler.libcxx={{detect_api.detect_libcxx(compiler, version, compiler_exe)}}

**detect_api reference**:

    - **`detect_os()`**: returns operating system as a string (e.g., "Windows", "Macos").
    - **`detect_arch()`**: returns system architecture as a string (e.g., "x86_64", "armv8").
    - **`detect_libcxx(compiler, version, compiler_exe=None)`**: returns C++ standard library as a string (e.g., "libstdc++", "libc++").
    - **`default_msvc_runtime(compiler)`**: returns tuple with runtime (e.g., "dynamic") and its version (e.g., "v143").
    - **`default_cppstd(compiler, compiler_version)`**: returns default C++ standard as a string (e.g., "gnu14").
    - **`detect_default_compiler()`**: returns tuple with compiler name (e.g., "gcc"), its version and the executable path.
    - **`detect_msvc_update(version)`**: returns MSVC update version as a string (e.g., "7").
    - **`default_msvc_ide_version(version)`**: returns MSVC IDE version as a string (e.g., "17").
    - **`default_compiler_version(compiler, version)`**: returns the default version that
        Conan uses in profiles, typically dropping some of the minor or patch digits, that
        do not affect binary compatibility.

.. _reference_config_files_profile_patterns:

Profile patterns
----------------

Profiles (and everywhere where a setting or option is defined) also support patterns definition, so you can override some settings, configuration variables, etc.
for some specific packages:

.. code-block:: text
    :caption: *zlib_clang_profile*

    [settings]
    # Only for zlib
    zlib/*:compiler=clang
    zlib/*:compiler.version=3.5
    zlib/*:compiler.libcxx=libstdc++11

    # For the all the dependency tree
    compiler=gcc
    compiler.version=4.9
    compiler.libcxx=libstdc++11

    [options]
    # shared=True option only for zlib package
    zlib/*:shared=True

    [buildenv]
    # For the all the dependency tree
    *:MYVAR=my_var

    [conf]
    # Only for zlib
    zlib/*:tools.build:compiler_executables={'c': '/usr/bin/clang', 'cpp': '/usr/bin/clang++'}


Your build tool will locate **clang** compiler only for the **zlib** package and **gcc** (default one)
for the rest of your dependency tree.

.. important::

    Putting only ``zlib:`` is deprecated behaviour and won't work, you have to always put a pattern-like expression, e.g., ``zlib*:``,
    ``zlib/*:``, ``zlib/1.*:``, etc.


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

Partial matches are also supported, so you can define a pattern like ``zlib*`` to match all the zlib like libraries,
so it will match everything starting with zlib, like ``zlib``, ``zlibng``, ``zlib/1.2.8@user/channel``, etc.

.. code-block:: text
    :caption: *myprofile*

    [settings]
    zlib*:compiler=clang
    zlib*:compiler.version=3.5
    zlib*:compiler.libcxx=libstdc++11


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
    zlib/*:compiler=clang
    zlib/*:compiler.version=3.5
    zlib/*:compiler.libcxx=libstdc++11


The final result of using *myprofile* is:

.. code-block:: text
    :caption: *myprofile (virtual result)*

    [settings]
    compiler=gcc
    compiler.libcxx=libstdc++11
    compiler.version=4.9
    zlib/*:compiler=clang
    zlib/*:compiler.libcxx=libstdc++11
    zlib/*:compiler.version=3.5


.. seealso::

    - :ref:`How to compose two or more profiles <reference_commands_install_composition>`
