.. _custom_settings:

Customizing settings
====================

There is a file in *<userhome>/.conan/settings.yml* that contains a default definition
of the allowed ``settings`` values for Conan package recipes. It looks like:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]
        Linux:
        Macos:
            version: [None, "10.6", "10.7", "10.8", "10.9", "10.10", "10.11", "10.12", "10.13", "10.14"]
        Android:
            api_level: ANY
        iOS:
            version: ["7.0", "7.1", "8.0", "8.1", "8.2", "8.3", "9.0", "9.1", "9.2", "9.3", "10.0", "10.1", "10.2", "10.3", "11.0", "11.1", "11.2", "11.3", "11.4", "12.0", "12.1"]
        watchOS:
            version: ["4.0", "4.1", "4.2", "4.3", "5.0", "5.1"]
        FreeBSD:
        SunOS:
        Emscripten:
    arch: [x86, x86_64, ppc32, ppc64le, ppc64, armv4, armv4i, armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3, sparc, sparcv9, mips, mips64, avr, s390, s390x, asm.js, wasm]
    compiler:
        gcc:
            version: ["4.1", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9",
                    "5", "5.1", "5.2", "5.3", "5.4", "5.5",
                    "6", "6.1", "6.2", "6.3", "6.4",
                    "7", "7.1", "7.2", "7.3",
                    "8", "8.1", "8.2",
                    "9"]
            libcxx: [libstdc++, libstdc++11]
            threads: [None, posix, win32] #  Windows MinGW
            exception: [None, dwarf2, sjlj, seh] # Windows MinGW
            cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20]
        Visual Studio:
            runtime: [MD, MT, MTd, MDd]
            version: ["8", "9", "10", "11", "12", "14", "15", "16"]
            toolset: [None, v90, v100, v110, v110_xp, v120, v120_xp,
                    v140, v140_xp, v140_clang_c2, LLVM-vs2012, LLVM-vs2012_xp,
                    LLVM-vs2013, LLVM-vs2013_xp, LLVM-vs2014, LLVM-vs2014_xp,
                    LLVM-vs2017, LLVM-vs2017_xp, v141, v141_xp, v141_clang_c2, v142]
            cppstd: [None, 14, 17, 20]

This are the **default** settings and values. They are a common syntax and notation for having package binary 
IDs that are common to all developers. They are also used for validation, for example if you write in a profile
``[settings]`` something like ``os=Windos`` (note the typo), then it will raise an error, telling you it is not
a recognized ``os`` and offering a list of available ``os``. Also, note how the sub-settings are different for
different platforms, for example the standard C++ library (``compiler.libcxx``) exists for the ``gcc`` compiler,
but not for ``Visual Studio`` compiler. And in the same way, ``Visual Studio`` has a ``runtime`` sub-setting that
is missing in ``gcc``. Trying to incorrectly use or define these sub-settings in the wrong compiler will also
raise an error.

These settings are good for defining a base for Open Source packages, and for a large number of mainstream
configurations. But it is likely that you might need finer detail of definition of the binaries that are being
created. 

For example, it is possible that you are managing binaries for older Linux distros, like RHEL 6, or old Centos,
besides other modern distributions. The problem is that the binaries compiled for modern distributions will
not work (will not be binary compatible, or ABI incompatible) in those older distributions, mainly because of
different versions of glibc. We would need a way to model the differences of the binaries for those platforms. 
Check out the section :ref:`deployment_challenges` which explains mentioned situation in detail.

.. _add_new_settings:

Adding new settings
-------------------

It is possible to add new settings at the root of the *settings.yml* file, something like:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]
    distro: [None, RHEL6, CentOS, Debian]

If we want to create different binaries from our recipes defining this new setting, we would need to add to
our recipes that:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch", "distro"

The value ``None`` allows for not defining it (which would be a default value, valid for all other distros).
It is possible to define values for it in the profiles:

.. code-block:: text

    [settings]
    os = "Linux"
    distro = "CentOS"
    compiler = "gcc"

And use their values to affect our build if desired:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch", "distro"

        def build(self):
            cmake = CMake(self)
            if self.settings.distro == "CentOS":
                cmake.definitions["SOME_CENTOS_FLAG"] = "Some CentOS Value"
                ...

.. _add_new_sub_settings:

Adding new sub-settings
-----------------------
The above approach requires modification to all recipes to take it into account. It is also possible to define
kind of incompatible settings, like ``os=Windows`` and ``distro=CentOS``. While adding new settings is totally
possible, it might make more sense for other cases, but for this example it is more adequate to add it as above
subsetting of the ``Linux`` OS:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]
        Linux:
            distro: [None, RHEL6, CentOS, Debian]

With this definition we could define our profiles as:

.. code-block:: text

    [settings]
    os = "Linux"
    os.distro = "CentOS"
    compiler = "gcc"

And any attempt to define ``os.distro`` for another ``os`` value rather than ``Linux`` will raise an error.

As this is a subsetting, it will be automatically taken into account in all recipes that declare an ``os`` setting.
Note that having a value of ``distro=None`` possible is important if you want to keep previously created binaries,
otherwise you would be forcing to always define a specific distro value, and binaries created without this subsetting,
won't be usable anymore.

The sub-setting can also be accessed from recipes:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"  # Note, no "distro" defined here

        def build(self):
            cmake = CMake(self)
            if self.settings.os == "Linux" and self.settings.os.distro == "CentOS":
                cmake.definitions["SOME_CENTOS_FLAG"] = "Some CentOS Value"


Add new values
--------------

In the same way we have added a new ``distro`` subsetting, it is possible to add new values to existing settings
and subsettings. For example, if some compiler version is not present in the range of accepted values, you can add those new values.

You can also add a completely new compiler:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]
       ...
    compiler:
        gcc:
            ...
        mycompiler:
            version: [1.1, 1.2]
        Visual Studio:

This works as the above regarding profiles, and the way they can be accessed from recipes. The main issue with custom compilers is that
the builtin build helpers, like ``CMake``, ``MSBuild``, etc, internally contains code that will check for those values. For example,
the ``MSBuild`` build helper will only know how to manage the ``Visual Studio`` setting and sub-settings, but not the new compiler.
For those cases, custom logic can be implemented in the recipes:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        def build(self):
            if self.settings.compiler == "mycompiler":
                my_custom_compile = ["some", "--flags", "for", "--my=compiler"]
                self.run(["mycompiler", "."] + my_custom_compile)


.. note::

    You can also remove items from *settings.yml* file. You can remove compilers, OS, architectures, etc.
    Do that only in the case you really want to protect against creation of binaries for other platforms other 
    than your main supported ones. In the general case, you can leave them, the binary configurations are managed 
    in **profiles**, and you want to define your supported configurations in profiles, not by restricting the *settings.yml*



.. note::

    If you customize your *settings.yml*, you can share, distribute and sync this configuration with your team
    and CI machines with the :ref:`conan_config_install` command.
















