.. _settings_yml:

settings.yml
============

The input ``settings`` for packages in Conan are predefined in ``~/.conan/settings.yml`` file, so only a few like ``os`` or ``compiler``
are possible.

.. code-block:: yaml

    # Only for cross building, 'os_build/arch_build' is the system that runs Conan
    os_build: [Windows, WindowsStore, Linux, Macos, FreeBSD, SunOS]
    arch_build: [x86, x86_64, ppc32, ppc64le, ppc64, armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3, sparc, sparcv9, mips, mips64, avr]

    # Only for building cross compilation tools, 'os_target/arch_target' is the system for
    # which the tools generate code
    os_target: [Windows, Linux, Macos, Android, iOS, watchOS, tvOS, FreeBSD, SunOS, Arduino]
    arch_target: [x86, x86_64, ppc32, ppc64le, ppc64, armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3, sparc, sparcv9, mips, mips64, avr]

    # Rest of the settings are "host" settings:
    # - For native building/cross building: Where the library/program will run.
    # - For building cross compilation tools: Where the cross compiler will run.
    os:
        Windows:
            subsystem: [None, cygwin, msys, msys2, wsl]
        WindowsStore:
            version: ["8.1", "10.0"]
        Linux:
        Macos:
            version: [None, "10.6", "10.7", "10.8", "10.9", "10.10", "10.11", "10.12", "10.13", "10.14"]
        Android:
            api_level: ANY
        iOS:
            version: ["7.0", "7.1", "8.0", "8.1", "8.2", "8.3", "9.0", "9.1", "9.2", "9.3", "10.0", "10.1", "10.2", "10.3", "11.0"]
        watchOS:
            version: ["4.0"]
        tvOS:
            version: ["11.0"]
        FreeBSD:
        SunOS:
        Arduino:
            board: ANY
    arch: [x86, x86_64, ppc32, ppc64le, ppc64, armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3, sparc, sparcv9, mips, mips64, avr]
    compiler:
        sun-cc:
            version: ["5.10", "5.11", "5.12", "5.13", "5.14"]
            threads: [None, posix]
            libcxx: [libCstd, libstdcxx, libstlport, libstdc++]
        gcc:
            version: ["4.1", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9",
                    "5", "5.1", "5.2", "5.3", "5.4", "5.5",
                    "6", "6.1", "6.2", "6.3", "6.4",
                    "7", "7.1", "7.2", "7.3",
                    "8", "8.1", "8.2"]
            libcxx: [libstdc++, libstdc++11]
            threads: [None, posix, win32] #  Windows MinGW
            exception: [None, dwarf2, sjlj, seh] # Windows MinGW
        Visual Studio:
            runtime: [MD, MT, MTd, MDd]
            version: ["8", "9", "10", "11", "12", "14", "15"]
            toolset: [None, v90, v100, v110, v110_xp, v120, v120_xp,
                    v140, v140_xp, v140_clang_c2, LLVM-vs2012, LLVM-vs2012_xp,
                    LLVM-vs2013, LLVM-vs2013_xp, LLVM-vs2014, LLVM-vs2014_xp,
                    LLVM-vs2017, LLVM-vs2017_xp, v141, v141_xp, v141_clang_c2]
        clang:
            version: ["3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "4.0",
                    "5.0", "6.0", "7.0",
                    "8"]
            libcxx: [libstdc++, libstdc++11, libc++]
        apple-clang:
            version: ["5.0", "5.1", "6.0", "6.1", "7.0", "7.3", "8.0", "8.1", "9.0", "9.1", "10.0"]
            libcxx: [libstdc++, libc++]

    build_type: [None, Debug, Release, RelWithDebInfo, MinSizeRel]
    cppstd: [None, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20]

As you can see, the possible values ``settings`` can take are restricted in the same file. This is done to ensure matching naming and
spelling as well as defining a common settings model among users and the OSS community.

However, this configuration file can be you can modified to any needs, including new settings or subsettings and their values. If you want
to distribute a unified *settings.yml* file you can use the :ref:`conan config install command<conan_config_install>`.

.. note::

    The *settings.yml* file is not perfect nor definitive and surely incomplete. Please share any suggestion in the Conan issue tracker
    with any missing settings and values that could make sense for other users.


Architectures
-------------

Here you can find a brief explanation of each of the architectures defined as ``arch``, ``arch_build`` and ``arch_target`` settings.

- **x86**: The popular 32 bit x86 architecture.

- **x86_64**: The popular 64 bit x64 architecture.

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
