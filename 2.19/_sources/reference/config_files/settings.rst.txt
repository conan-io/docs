.. _reference_config_files_settings_yml:

settings.yml
============

This configuration file is located in the Conan user home, i.e., ``[CONAN_HOME]/settings.yml``.
It looks like this:

.. conan-home-file::
   :file-path: settings.yml
   :language: yaml

As you can see, the possible values of ``settings`` are defined in the same file. This is done to ensure matching naming and
spelling as well as defining a common settings model among users and the OSS community. Some general information about settings:

* If a setting is allowed to be set to any value, you can use ``ANY``.
* If a setting is allowed to be set to any value or it can also be unset, you can use ``[null, ANY]``.

However, this configuration file can be modified to any needs, including new settings or sub-settings and their values. If you want
to distribute an unified *settings.yml* file you can use the :ref:`conan config install command<reference_commands_conan_config_install>`.

.. seealso::

    - :ref:`creating_packages_configure_options_settings`
    - :ref:`conan_conanfile_properties_settings`


Operating systems
-----------------

``baremetal`` operating system is a convention meaning that the binaries run directly
on the hardware, without an operating system or equivalent layer. This is to differentiate to the ``null`` value,
which is associated to the "this value is not defined" semantics. ``baremetal`` is a common name convention for
embedded microprocessors and microcontrollers' code. It is expected that users might customize the space inside the
``baremetal`` setting with further subsettings to specify their specific hardware platforms, boards, families, etc.
At the moment the ``os=baremetal`` value is still not used by Conan builtin toolchains and helpers,
but it is expected that they can evolve and start using it.


Compilers
---------

Some notes about different compilers:

msvc
++++

The ``msvc`` compiler setting uses the actual ``cl.exe`` compiler version, that is 190 (19.0), 191 (19.1), etc, instead of the Visual Studio IDE version(15, 16, etc).

When using the ``msvc`` compiler, the Visual Studio toolset version (the actual ``vcvars`` activation
and ``MSBuild`` location) will be defined by the default provided by that compiler version:

- ``msvc`` compiler version '190': Visual Studio 14 2015 (toolset v140)
- ``msvc`` compiler version '191': Visual Studio 15 2017 (toolset v141)
- ``msvc`` compiler version '192': Visual Studio 16 2019 (toolset v142)
- ``msvc`` compiler version '193': Visual Studio 17 2022 (toolset v143, compiler versions up to 19.39, toolset version 14.3X)
- ``msvc`` compiler version '194': Visual Studio 17 2022 (toolset v143, compiler versions from 19.40, toolset version 14.4X, Visual Studio update 17.10)

Note that both ``compiler.version=193`` and ``compiler.version=194`` map to the ``v143`` toolset, but to different toolset versions ``14.3X``
and ``14.4X``, due to the versioning scheme change done from Visual Studio update 17.10 that introduced compiler version 19.40 and toolset version 14.40
while keeping the toolset ``v143`` nomenclature.

If you want to explicitly force a specific Visual Studio IDE version, you can do it with the ``tools.microsoft.msbuild:vs_version`` configuration:

.. code-block:: text

    [settings]
    compiler=msvc
    compiler.version=190

    [conf]
    tools.microsoft.msbuild:vs_version = 16


In this case, the ``vcvars`` will activate the Visual Studio 16 installation, but the ``190`` compiler version will still be used
because the necessary ``toolset=v140`` will be set.

The settings define the last digit ``update: [null, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]``, which by default is ``null`` and means that Conan
assumes binary compatibility for the compiler patches, which works in general for the Microsoft compilers. For cases where finer
control is desired, you can just add the ``update`` part to your profiles:

.. code-block:: text

    [settings]
    compiler=msvc
    compiler.version=191
    compiler.update=3

This will be equivalent to the full version ``1913 (19.13)``. If even further details are desired, you could even add your own digits
to the ``update`` subsetting in ``settings.yml``.


intel-cc
++++++++

.. include:: ../../common/experimental_warning.inc

This compiler is aimed to handle the new Intel oneAPI DPC++/C++/Classic compilers. Instead of having *n* different compilers,
you have 3 different **modes** of working:

* ``icx`` for Intel oneAPI C++.
* ``dpcpp`` for Intel oneAPI DPC++.
* ``classic`` for Intel C++ Classic ones.

Besides that, Intel releases some versions with revisions numbers so the ``update`` field is supposed to be any
possible minor number for the Intel compiler version used, e.g, ``compiler.version=2021.1`` and
``compiler.update=311`` mean Intel version is ``2021.1.311``.


Architectures
-------------

Here you can find a brief explanation of each of the architectures defined as ``arch``, ``arch_build`` and ``arch_target`` settings.

- **x86**: The popular 32 bit x86 architecture.
- **x86_64**: The popular 64 bit x64 architecture.
- **ppc64le**: The PowerPC 64 bit Big Endian architecture.
- **ppc32**: The PowerPC 32 bit architecture.
- **ppc64le**: The PowerPC 64 bit Little Endian architecture.
- **ppc64**: The PowerPC 64 bit Big Endian architecture.
- **armv5el**: The ARM 32 bit version 5 architecture, soft-float.
- **armv5hf**: The ARM 32 bit version 5 architecture, hard-float.
- **armv6**: The ARM 32 bit version 6 architecture.
- **armv7**: The ARM 32 bit version 7 architecture.
- **armv7hf**: The ARM 32 bit version 7 hard-float architecture.
- **armv7s**: The ARM 32 bit version 7 *swift* architecture mostly used in Apple's A6 and A6X chips on iPhone 5, iPhone 5C and iPad 4.
- **armv7k**: The ARM 32 bit version 7 *k* architecture mostly used in Apple's WatchOS.
- **armv8**: The ARM 64 bit and 32 bit compatible version 8 architecture. It covers only the ``aarch64`` instruction set.
- **armv8_32**: The ARM 32 bit version 8 architecture. It covers only the ``aarch32`` instruction set (a.k.a. ``ILP32``).
- **armv8.3**: The ARM 64 bit and 32 bit compatible version 8.3 architecture. Also known as ``arm64e``, it is used on the A12 chipset added
  in the latest iPhone models (XS/XS Max/XR).
- **arm64ec**: Windows 11 ARM64EC (Emulation Compatible). This architecture support is **experimental** and incomplete. Supported in CMake for VS and MSBuild integrations.. Report new issues in Github if necessary.
- **sparc**: The SPARC (Scalable Processor Architecture) originally developed by Sun Microsystems.
- **sparcv9**: The SPARC version 9 architecture.
- **mips**: The 32 bit MIPS (Microprocessor without Interlocked Pipelined Stages) developed by MIPS Technologies (formerly MIPS Computer
  Systems).
- **mips64**: The 64 bit MIPS (Microprocessor without Interlocked Pipelined Stages) developed by MIPS Technologies (formerly MIPS Computer
  Systems).
- **avr**: The 8 bit AVR microcontroller architecture developed by Atmel (Microchip Technology).
- **s390**: The 32 bit address Enterprise Systems Architecture 390 from IBM.
- **s390x**: The 64 bit address Enterprise Systems Architecture 390 from IBM.
- **asm.js**: The subset of JavaScript that can be used as low-level target for compilers, not really a processor architecture, it's produced
  by Emscripten. Conan treats it as an architecture to align with build systems design (e.g. GNU auto tools and CMake).
- **wasm**: The Web Assembly, not really a processor architecture, but byte-code format for Web, it's produced by Emscripten. Conan treats it
  as an architecture to align with build systems design (e.g. GNU auto tools and CMake).
- **sh4le**: The Hitachi SH-4 SuperH architecture.
- **e2k-v2**: The Elbrus 2000 v2 512 bit VLIW (Very Long Instruction Word) architecture (Elbrus 2CM, Elbrus 2C+ CPUs) originally developed by MCST (Moscow Center of SPARC Technologies).
- **e2k-v3**: The Elbrus 2000 v3 512 bit VLIW (Very Long Instruction Word) architecture (Elbrus 2S, aka Elbrus 4C, CPU) originally developed by MCST (Moscow Center of SPARC Technologies).
- **e2k-v4**: The Elbrus 2000 v4 512 bit VLIW (Very Long Instruction Word) architecture (Elbrus 8C, Elbrus 8C1, Elbrus 1C+ and Elbrus 1CK CPUs) originally developed by MCST (Moscow Center of SPARC Technologies).
- **e2k-v5**: The Elbrus 2000 v5 512 bit VLIW (Very Long Instruction Word) architecture (Elbrus 8C2 ,aka Elbrus 8CB, CPU) originally developed by MCST (Moscow Center of SPARC Technologies).
- **e2k-v6**: The Elbrus 2000 v6 512 bit VLIW (Very Long Instruction Word) architecture (Elbrus 2C3, Elbrus 12C and Elbrus 16C CPUs) originally developed by MCST (Moscow Center of SPARC Technologies).
- **e2k-v7**: The Elbrus 2000 v7 512 bit VLIW (Very Long Instruction Word) architecture (Elbrus 32C CPU) originally developed by MCST (Moscow Center of SPARC Technologies).
- **xtensalx6**: Xtensa LX6 DPU for ESP32 microcontroller.
- **xtensalx106**: Xtensa LX6 DPU for ESP8266 microcontroller.
- **xtensalx7**: Xtensa LX7 DPU for ESP32-S2 and ESP32-S3 microcontrollers.


C++ standard libraries (aka compiler.libcxx)
--------------------------------------------

``compiler.libcxx`` sub-setting defines C++ standard libraries implementation to be used. The sub-setting applies only to certain compilers,
e.g. it applies to *clang*, *apple-clang* and *gcc*, but doesn't apply to *Visual Studio*.

- **libstdc++** (gcc, clang, apple-clang, sun-cc): `The GNU C++ Library <https://gcc.gnu.org/onlinedocs/libstdc++/>`__. NOTE that this implicitly
  defines **_GLIBCXX_USE_CXX11_ABI=0** to use old ABI. Might be a wise choice for old systems, such as CentOS 6. On Linux systems,
  you may need to install `libstdc++-dev <https://packages.debian.org/sid/libstdc++-dev>`_ (package name could be different in various distros)
  in order to use the standard library. NOTE that on Apple systems usage of **libstdc++** has been deprecated.

- **libstdc++11** (gcc, clang, apple-clang): `The GNU C++ Library <https://gcc.gnu.org/onlinedocs/libstdc++/>`__. NOTE that this implicitly
  defines **_GLIBCXX_USE_CXX11_ABI=1** to use new ABI. Might be a wise choice for newer systems, such as Ubuntu 20. On Linux systems,
  you may need to install `libstdc++-dev <https://packages.debian.org/sid/libstdc++-dev>`_ (package name could be different in various distros)
  in order to use the standard library. NOTE that on Apple systems usage of **libstdc++** has been deprecated.

- **libc++** (clang, apple-clang): `LLVM libc++ <https://libcxx.llvm.org/>`__. On Linux systems, you may need to install `libc++-dev <https://packages.debian.org/sid/libc++-dev>`_
  (package name could be different in various distros) in order to use the standard library.

- **c++_shared** (clang, Android only): use `LLVM libc++ <https://libcxx.llvm.org/>`__ as a shared library. Refer to the `C++ Library Support <https://developer.android.com/ndk/guides/cpp-support>`__ for the
  additional details.

- **c++_static** (clang, Android only): use `LLVM libc++ <https://libcxx.llvm.org/>`__ as a static library. Refer to the `C++ Library Support <https://developer.android.com/ndk/guides/cpp-support>`__ for the
  additional details.

- **libCstd** (sun-cc): Rogue Wave's stdlib. See `Comparing C++ Standard Libraries libCstd, libstlport, and libstdcxx <https://www.oracle.com/solaris/technologies/cmp-stlport-libcstd.html>`__.

- **libstlport** (sun-cc): `STLport <http://www.stlport.org/>`__. See `Comparing C++ Standard Libraries libCstd, libstlport, and libstdcxx <https://www.oracle.com/solaris/technologies/cmp-stlport-libcstd.html>`__.

- **libstdcxx** (sun-cc): `Apache C++ Standard Library <http://people.apache.org/~gmcdonald/stdcxx/index.html>`__. See `Comparing C++ Standard Libraries libCstd, libstlport, and libstdcxx <https://www.oracle.com/solaris/technologies/cmp-stlport-libcstd.html>`__.

- **gpp** (qcc): GNU C++ lib. See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.

- **cpp** (qcc): Dinkum C++ lib. See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.

- **cpp-ne** (qcc): Dinkum C++ lib (no exceptions). See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.

- **acpp** (qcc): Dinkum Abridged C++ lib. See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.

- **acpp-ne** (qcc): Dinkum Abridged C++ lib (no exceptions). See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.

- **ecpp** (qcc): Embedded Dinkum C++ lib. See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.

- **ecpp-ne** (qcc): Embedded Dinkum C++ lib (no exceptions). See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.

- **cxx** (qcc): LLVM C++. See `QCC documentation <https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_utilities/q/qcc.html>`__.


.. _reference_config_files_customizing_settings:

Customizing settings
--------------------

Settings are also customizable to add your own ones:


Adding new settings
+++++++++++++++++++

It is possible to add new settings at the root of the *settings.yml* file, something like:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [null, cygwin, msys, msys2, wsl]
    distro: [null, RHEL6, CentOS, Debian]


If we want to create different binaries from our recipes defining this new setting, we would need to add to
our recipes that:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch", "distro"


The value ``null`` allows for not defining it (which would be a default value, valid for all the other distros).
It is also possible to define values for it in the profiles:

.. code-block:: text

    [settings]
    os = "Linux"
    distro = "CentOS"
    compiler = "gcc"

And use their values to affect our build if desired:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch", "distro"

        def generate(self):
            tc = CMakeToolchain(self)
            if self.settings.distro == "CentOS":
                tc.cache_variables["SOME_CENTOS_FLAG"] = "Some CentOS Value"
                ...


Adding new sub-settings
+++++++++++++++++++++++

The above approach requires modification to all recipes to take it into account. It is also possible to define
kind of incompatible settings, like ``os=Windows`` and ``distro=CentOS``. While adding new settings is totally
suitable, it might make more sense to add it as a new sub-setting of the ``Linux`` OS:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [null, cygwin, msys, msys2, wsl]
        Linux:
            distro: [null, RHEL6, CentOS, Debian]

With this definition we could define our profiles as:

.. code-block:: text

    [settings]
    os = "Linux"
    os.distro = "CentOS"
    compiler = "gcc"


And any attempt to define ``os.distro`` for another ``os`` value rather than ``Linux`` will raise an error.

As this is a sub-setting, it will be automatically taken into account in all recipes that declare an ``os`` setting.
Note that having a value of ``distro=null`` possible is important if you want to keep previously created binaries,
otherwise you would be forcing to always define a specific distro value, and binaries created without this sub-setting,
won't be usable anymore.

The sub-setting can also be accessed from recipes:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"  # Note, no "distro" defined here

        def generate(self):
            tc = CMakeToolchain(self)
            if self.settings.os == "Linux" and self.settings.os.distro == "CentOS":
                tc.cache_variables["SOME_CENTOS_FLAG"] = "Some CentOS Value"


It is possible to have ``ANY`` to define nested subsettings, being the ``ANY`` the fallback for any value not matching the defined ones:

.. code-block:: yaml

    os:
        ANY:
            version: [null, ANY]
        Ubuntu:
            version: ["18.04", "20.04"]

This will allow settings like ``-s os=MyOS -s os.version=1.2.3``, because the version can be ``ANY`` for ``os!=Ubuntu``,
but if we try ``-s os=Ubuntu -s os.version=1.2.3`` it will error because ``Ubuntu`` only accept those defined versions.
 

Add new values
++++++++++++++

In the same way we have added a new ``distro`` sub-setting, it is possible to add new values to existing settings
and sub-settings. For example, if some compiler version is not present in the range of accepted values, you can add those new values.

You can also add a completely new compiler:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [null, cygwin, msys, msys2, wsl]
       ...
    compiler:
        gcc:
            ...
        mycompiler:
            version: [1.1, 1.2]
        msvc:


This works as the above regarding profiles, and the way they can be accessed from recipes. The main issue with custom compilers is that
the builtin build helpers, like ``CMake``, ``MSBuild``, etc, internally contains code that will check for those values. For example,
the ``MSBuild`` build helper will only know how to manage the ``msvc`` setting and sub-settings, but not the new compiler.
For those cases, custom logic can be implemented in the recipes:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        def build(self):
            if self.settings.compiler == "mycompiler":
                my_custom_compile = ["some", "--flags", "for", "--my=compiler"]
                self.run(["mycompiler", "."] + my_custom_compile)


.. note::

    You can remove items from *settings.yml* file: compilers, OS, architectures, etc.
    Do that only in the case you really want to protect against creation of binaries for other platforms other
    than your main supported ones. In the general case, you can leave them, the binary configurations are managed
    in **profiles**, and you want to define your supported configurations in profiles, not by restricting the *settings.yml*


.. note::

    If you customize your *settings.yml*, you can share, distribute and sync this configuration with your team
    and CI machines with the :ref:`reference_commands_conan_config_install` command.


.. _reference_config_files_settings_user_yml:

settings_user.yml
-----------------

The previous section explains how to customize the Conan *settings.yml*, but you could also create your *settings_user.yml*.
This file will contain only the new fields-values that you want to use in your recipes, so the final result will be a
composition of both files, the *settings.yml* and the *settings_user.yml*.


.. seealso::

    - :ref:`examples_config_files_settings_user`
