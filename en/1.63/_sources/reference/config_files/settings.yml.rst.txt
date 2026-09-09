.. _settings_yml:

settings.yml
============

.. caution::

    We are actively working to finalize the *Conan 2.0 Release*. Some of the information on this page references
    **deprecated** features which will not be carried forward with the new release. It's important to check the 
    :ref:`Migration Guidelines<conan2_migration_guide>` to ensure you are using the most up to date features.

The input ``settings`` for packages in Conan are predefined in ``~/.conan/settings.yml`` file, so only a few like ``os`` or ``compiler``
are possible. These are the **default** values, but it is possible to customize them, see :ref:`custom_settings`.

.. code-block:: yaml

    # Only for cross building, 'os_build/arch_build' is the system that runs Conan
    os_build: [Windows, WindowsStore, Linux, Macos, FreeBSD, SunOS, AIX, VxWorks]
    arch_build: [x86, x86_64, ppc32be, ppc32, ppc64le, ppc64, armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3, sparc, sparcv9, mips, mips64, avr, s390, s390x, sh4le, e2k-v2, e2k-v3, e2k-v4, e2k-v5, e2k-v6, e2k-v7]

    # Only for building cross compilation tools, 'os_target/arch_target' is the system for
    # which the tools generate code
    os_target: [Windows, Linux, Macos, Android, iOS, watchOS, tvOS, FreeBSD, SunOS, AIX, Arduino, Neutrino]
    arch_target: [x86, x86_64, ppc32be, ppc32, ppc64le, ppc64, armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3, sparc, sparcv9, mips, mips64, avr, s390, s390x, asm.js, wasm, sh4le, e2k-v2, e2k-v3, e2k-v4, e2k-v5, e2k-v6, e2k-v7, xtensalx6, xtensalx106, xtensalx7]

    # Rest of the settings are "host" settings:
    # - For native building/cross building: Where the library/program will run.
    # - For building cross compilation tools: Where the cross compiler will run.
    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]
        WindowsStore:
            version: ["8.1", "10.0"]
        WindowsCE:
            platform: ANY
            version: ["5.0", "6.0", "7.0", "8.0"]
        Linux:
        iOS:
            version: &ios_version
                     ["7.0", "7.1", "8.0", "8.1", "8.2", "8.3", "9.0", "9.1", "9.2", "9.3", "10.0", "10.1", "10.2", "10.3",
                      "11.0", "11.1", "11.2", "11.3", "11.4", "12.0", "12.1", "12.2", "12.3", "12.4",
                      "13.0", "13.1", "13.2", "13.3", "13.4", "13.5", "13.6", "13.7",
                      "14.0", "14.1", "14.2", "14.3", "14.4", "14.5", "14.6", "14.7", "14.8",
                      "15.0", "15.1", "15.2", "15.3", "15.4", "15.5", "15.6", "16.0", "16.1"]
            sdk: [None, "iphoneos", "iphonesimulator"]
            sdk_version: [None, "11.3", "11.4", "12.0", "12.1", "12.2", "12.4",
                          "13.0", "13.1", "13.2", "13.4", "13.5", "13.6", "13.7",
                          "14.0", "14.1", "14.2", "14.3", "14.4", "14.5", "15.0", "15.2", "15.4", "15.5", "16.0", "16.1"]
        watchOS:
            version: ["4.0", "4.1", "4.2", "4.3", "5.0", "5.1", "5.2", "5.3", "6.0", "6.1", "6.2",
                      "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "8.0", "8.1", "8.3", "8.4", "8.5", "8.6", "8.7", "9.0", "9.1"]
            sdk: [None, "watchos", "watchsimulator"]
            sdk_version: [None, "4.3", "5.0", "5.1", "5.2", "5.3", "6.0", "6.1", "6.2",
                          "7.0", "7.1", "7.2", "7.4", "8.0", "8.0.1", "8.3", "8.5", "9.0", "9.1"]
        tvOS:
            version: ["11.0", "11.1", "11.2", "11.3", "11.4", "12.0", "12.1", "12.2", "12.3", "12.4",
                      "13.0", "13.2", "13.3", "13.4", "14.0", "14.2", "14.3", "14.4", "14.5", "14.6", "14.7",
                      "15.0", "15.1", "15.2", "15.3", "15.4", "15.5", "15.6", "16.0", "16.1"]
            sdk: [None, "appletvos", "appletvsimulator"]
            sdk_version: [None, "11.3", "11.4", "12.0", "12.1", "12.2", "12.4",
                          "13.0", "13.1", "13.2", "13.4", "14.0", "14.2", "14.3", "14.5", "15.0", "15.2", "15.4", "16.0", "16.1"]
        Macos:
            version: [None, "10.6", "10.7", "10.8", "10.9", "10.10", "10.11", "10.12", "10.13", "10.14", "10.15", "11.0", "12.0", "13.0"]
            sdk: [None, "macosx"]
            sdk_version: [None, "10.13", "10.14", "10.15", "11.0", "11.1", "11.3", "12.0", "12.1", "12.3", "13.0", "13.1"]
            subsystem:
                None:
                catalyst:
                    ios_version: *ios_version
        Android:
            api_level: ANY
        FreeBSD:
        SunOS:
        AIX:
        Arduino:
            board: ANY
        Emscripten:
        Neutrino:
            version: ["6.4", "6.5", "6.6", "7.0", "7.1"]
        baremetal:
        VxWorks:
            version: ["7"]
    arch: [x86, x86_64, ppc32be, ppc32, ppc64le, ppc64, armv4, armv4i, armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3, sparc, sparcv9, mips, mips64, avr, s390, s390x, asm.js, wasm, sh4le, e2k-v2, e2k-v3, e2k-v4, e2k-v5, e2k-v6, e2k-v7, xtensalx6, xtensalx106, xtensalx7]
    compiler:
        sun-cc:
            version: ["5.10", "5.11", "5.12", "5.13", "5.14", "5.15"]
            threads: [None, posix]
            libcxx: [libCstd, libstdcxx, libstlport, libstdc++]
        gcc: &gcc
            version: ["4.1", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9",
                      "5", "5.1", "5.2", "5.3", "5.4", "5.5",
                      "6", "6.1", "6.2", "6.3", "6.4", "6.5",
                      "7", "7.1", "7.2", "7.3", "7.4", "7.5",
                      "8", "8.1", "8.2", "8.3", "8.4", "8.5",
                      "9", "9.1", "9.2", "9.3", "9.4", "9.5",
                      "10", "10.1", "10.2", "10.3", "10.4", "10.5",
                      "11", "11.1", "11.2", "11.3", "11.4",
                      "12", "12.1", "12.2", "12.3",
                      "13", "13.1", "13.2"]
            libcxx: [libstdc++, libstdc++11]
            threads: [None, posix, win32]  # Windows MinGW
            exception: [None, dwarf2, sjlj, seh]  # Windows MinGW
            cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20, 23, gnu23]
        Visual Studio: &visual_studio
            runtime: [MD, MT, MTd, MDd]
            version: ["8", "9", "10", "11", "12", "14", "15", "16", "17"]
            toolset: [None, v90, v100, v110, v110_xp, v120, v120_xp,
                      v140, v140_xp, v140_clang_c2, LLVM-vs2012, LLVM-vs2012_xp,
                      LLVM-vs2013, LLVM-vs2013_xp, LLVM-vs2014, LLVM-vs2014_xp,
                      LLVM-vs2017, LLVM-vs2017_xp, v141, v141_xp, v141_clang_c2, v142,
                      llvm, ClangCL, v143]
            cppstd: [None, 14, 17, 20, 23]
        msvc:
            version: [170, 180, 190, 191, 192, 193]
            update: [None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            runtime: [static, dynamic]
            runtime_type: [Debug, Release]
            cppstd: [98, 14, 17, 20, 23]
            toolset: [None, v110_xp, v120_xp, v140_xp, v141_xp]
        clang:
            version: ["3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "4.0",
                      "5.0", "6.0", "7.0", "7.1",
                      "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
            libcxx: [None, libstdc++, libstdc++11, libc++, c++_shared, c++_static]
            cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20, 23, gnu23]
            runtime: [None, MD, MT, MTd, MDd, static, dynamic]
            runtime_type: [None, Debug, Release]
            runtime_version: [None, v140, v141, v142, v143]
        apple-clang: &apple_clang
            version: ["5.0", "5.1", "6.0", "6.1", "7.0", "7.3", "8.0", "8.1", "9.0", "9.1",
                      "10.0", "11.0", "12.0", "13", "13.0", "13.1", "14", "14.0", "15", "15.0"]
            libcxx: [libstdc++, libc++]
            cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20, 23, gnu23]
        intel:
            version: ["11", "12", "13", "14", "15", "16", "17", "18", "19", "19.1"]
            update: [None, ANY]
            base:
                gcc:
                    <<: *gcc
                    threads: [None]
                    exception: [None]
                Visual Studio:
                    <<: *visual_studio
                apple-clang:
                    <<: *apple_clang
        intel-cc:
            version: ["2021.1", "2021.2", "2021.3"]
            update: [None, ANY]
            mode: ["icx", "classic", "dpcpp"]
            libcxx: [None, libstdc++, libstdc++11, libc++]
            cppstd: [None, 98, gnu98, 03, gnu03, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20, 23, gnu23]
            runtime: [None, static, dynamic]
            runtime_type: [None, Debug, Release]
        qcc:
            version: ["4.4", "5.4", "8.3"]
            libcxx: [cxx, gpp, cpp, cpp-ne, accp, acpp-ne, ecpp, ecpp-ne]
            cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17]
        mcst-lcc:
            version: ["1.19", "1.20", "1.21", "1.22", "1.23", "1.24", "1.25"]
            base:
                gcc:
                    <<: *gcc
                    threads: [None]
                    exceptions: [None]

    build_type: [None, Debug, Release, RelWithDebInfo, MinSizeRel]


    cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20, 23, gnu23]  # Deprecated, use compiler.cppstd


As you can see, the possible values ``settings`` can take are restricted in the same file. This is done to ensure matching naming and
spelling as well as defining a common settings model among users and the OSS community.
If a setting is allowed to be set to any value, you can use ``ANY``.
If a setting is allowed to be set to any value or it can also be unset, you can use ``[None, ANY]``.

However, this configuration file can be modified to any needs, including new settings or subsettings and their values. If you want
to distribute a unified *settings.yml* file you can use the :ref:`conan config install command<conan_config_install>`.

.. note::

    The *settings.yml* file is not perfect nor definitive and surely incomplete. Please share any suggestion in the Conan issue tracker
    with any missing settings and values that could make sense for other users.

    To force the creation of the *settings.yml* the command ``conan config init`` is available.

Operating systems
-----------------

``baremetal`` operating system (introduced in Conan 1.43) is a convention meaning that the binaries run directly on the hardware, without a operating system or equivalent
layer. This is to differentiate to the ``None`` value, which is associated to the "this value is not defined" semantics.
The ``baremetal`` is a common name convention for embedded microprocessors and microcontrollers code. It is expected that users might customize the
space inside the ``baremetal`` setting with further subsettings to specify their specific hardware platforms, boards, families, etc.
At the moment (Conan 1.43) the ``os=baremetal`` value is still not used by Conan builtin toolchains and helpers, but it is expected that they can
evolve and start using it.


Compilers
---------

Some notes about different compilers:

msvc
++++

.. important::

    This feature is still **under development**, , that is intended to deprecate the ``Visual Studio``, while it is recommended and usable and
    we will try not to break them in future releases, some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.

- It uses the compiler version, that is 190 (19.0), 191 (19.1), etc, instead of the Visual Studio IDE (15, 16, etc).
- It is only used by the new build integrations in :ref:`conan_tools_cmake` and :ref:`conan_tools_microsoft`, but not the previous ones.
- At the moment it implements a ``compatible_packages`` fallback to Visual Studio compiled packages, that is, previous existing binaries
  compiled with ``settings.compiler="Visual Studio"`` can be used for the ``msvc`` compiler if no binaries exist for it yet.
  This behavior can be opted-out with ``core.package_id:msvc_visual_incompatible`` :ref:`global_conf` configuration.

When using the ``msvc`` compiler, the Visual Studio toolset version (the actual ``vcvars`` activation and ``MSBuild`` location) will be
defined by the default provide of that compiler version:

- ``msvc`` compiler version '190': Visual Studio 14 2015
- ``msvc`` compiler version '191': Visual Studio 15 2017
- ``msvc`` compiler version '192': Visual Studio 16 2019

This can be configured in your profiles with the ``tools.microsoft.msbuild:vs_version`` configuration:

.. code-block:: text

    [settings]
    compiler=msvc
    compiler.version=190

    [conf]
    tools.microsoft.msbuild:vs_version = 16


In this case, the ``vcvars`` will activate the Visual Studio 16 installation, but the ``190`` compiler version will still be used
because the necessary ``toolset=v140`` will be set.

The settings define the last digit ``update: [None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]``, which by default is ``None``, means that Conan
assumes binary compatibility for the compiler patches, which works in general for the Microsoft compilers. For cases where finer
control is desired, you can just add the ``update`` part to your profiles:

.. code-block:: text

    [settings]
    compiler=msvc
    compiler.version=191
    compiler.version.update=3


This will be equivalent to the full version ``1913 (19.13)``. If even further details is desired, you could even add your own digits
to the ``update`` subsetting in ``settings.yml``.


intel-cc
++++++++

Available since: `1.41.0 <https://github.com/conan-io/conan/releases/tag/1.41.0>`_

This compiler is a new, **experimental** one, aimed to handle the new Intel oneAPI DPC++/C++/Classic compilers. Instead of having *n* different compilers, you have 3 different **modes** of working:

* ``icx`` for Intel oneAPI C++.
* ``dpcpp`` for Intel oneAPI DPC++.
* ``classic`` for Intel C++ Classic ones.

Besides that, Intel releases some versions with revisions numbers so the ``update`` field it's supposed to be any possible minor number for the Intel compiler version used, e.g,
``compiler.version=2021.1`` and ``compiler.update=311`` mean Intel version is ``2021.1.311``.


For more information, you can check the :ref:`IntelCC section <conan_tools_intel>`.

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


C++ standard libraries (aka compiler.libcxx)
--------------------------------------------

``compiler.libcxx`` sub-setting defines C++ standard libraries implementation to be used. The sub-setting applies only to certain compilers,
e.g. it applies to *clang*, *apple-clang* and *gcc*, but doesn't apply to *Visual Studio*.

- **libstdc++** (gcc, clang, apple-clang, sun-cc): `The GNU C++ Library <https://gcc.gnu.org/onlinedocs/libstdc++/>`__. NOTE that this implicitly
  defines **_GLIBCXX_USE_CXX11_ABI=0** to use old ABI. See :ref:`How to manage the GCC >= 5 ABI <manage_gcc_abi>` for the additional details. Might
  be a wise choice for old systems, such as CentOS 6. On Linux systems, you may need to install `libstdc++-dev <https://packages.debian.org/sid/libstdc++-dev>`_
  (package name could be different in various distros) in order to use the standard library. NOTE that on Apple systems usage of **libstdc++** has been deprecated.

- **libstdc++11** (gcc, clang, apple-clang): `The GNU C++ Library <https://gcc.gnu.org/onlinedocs/libstdc++/>`__. NOTE that this implicitly
  defines **_GLIBCXX_USE_CXX11_ABI=1** to use new ABI. See :ref:`How to manage the GCC >= 5 ABI <manage_gcc_abi>` for the additional details. Might
  be a wise choice for newer systems, such as Ubuntu 20. On Linux systems, you may need to install `libstdc++-dev <https://packages.debian.org/sid/libstdc++-dev>`_
  (package name could be different in various distros) in order to use the standard library. NOTE that on Apple systems usage of **libstdc++** has been deprecated.

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
