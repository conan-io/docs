.. _conan_tools_gnu_gnutoolchain:

GnuToolchain
============

.. include:: ../../../common/experimental_warning.inc

The ``GnuToolchain`` is the toolchain generator for Autotools and other GNU-like build systems. It is a more modern and
usable alternative to the :ref:`AutotoolsToolchain<conan_tools_gnu_autotoolstoolchain>`, based on it, but with an improved
user experience, like the dict-like ``configure_args``, ``make_args`` and ``autoreconf_args`` attributes or the ``extra_env``
attribute to customize the generated environment. It will generate shell scripts containing environment variable definitions
that the autotools build system can understand.

.. warning::

    ``GnuToolchain`` and :ref:`AutotoolsToolchain<conan_tools_gnu_autotoolstoolchain>` are mutually exclusive
    alternatives. Do not use both in the same recipe: choose one or the other.

This generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "GnuToolchain"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    GnuToolchain

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import GnuToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = GnuToolchain(self)
            tc.generate()


Generated files
---------------

It will generate either the ``conangnutoolchain.sh`` or ``conangnutoolchain.bat`` files:

.. code-block:: bash

    $ conan install # there is a conanfile here, default is Release
    $ source conangnutoolchain.sh
    # or in Windows
    $ conangnutoolchain.bat

These launchers will append information to the ``CPPFLAGS``, ``LDFLAGS``, ``CXXFLAGS``,
``CFLAGS`` environment variables that translate the settings and options to the
corresponding build flags like ``-stdlib=libstdc++``, ``-std=gnu14``, architecture flags,
etc. It will also append the folder where the Conan generators are located to the
``PKG_CONFIG_PATH`` environment variable. On Apple platforms, ``ASFLAGS`` is also set with
architecture and sysroot flags to ensure the assembler uses the same cross-compilation
settings as the C/C++ compilers.

In a cross-building context, the environment variables ``CC_FOR_BUILD`` and ``CXX_FOR_BUILD`` are also set if the
build profile defines the ``c`` and ``cpp`` values in the configuration variable ``tools.build:compiler_executables``.
See more info in the :ref:`conf section<conan_tools_gnu_gnutoolchain_conf>`.

This generator will also generate a file called ``conanbuild.conf`` containing three keys:

- **configure_args**: Arguments to call the ``configure`` script.
- **make_args**: Arguments to call the ``make`` script.
- **autoreconf_args**: Arguments to call the ``autoreconf`` script.

The :ref:`Autotools build helper<conan_tools_gnu_build_helper>` will use that ``conanbuild.conf`` file to seamlessly call
the configure and make script using these precalculated arguments.


Customization
-------------

You can change some attributes before calling the ``generate()`` method if you want to change some of the precalculated
values:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import GnuToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = GnuToolchain(self)
            tc.configure_args["--my_argument"] = None
            tc.generate()


The constructor of ``GnuToolchain`` accepts the following arguments:

* **namespace** (Defaulted to ``None``): Avoids collisions when there are multiple toolchain calls in the same recipe. When
  set, the generated file will be named *<namespace>_conanbuild.conf* instead of *conanbuild.conf*. The same value
  must be passed to the constructor of the :ref:`Autotools build helper<conan_tools_gnu_build_helper>`.
* **prefix** (Defaulted to ``"/"``): Folder to use for the ``--prefix`` argument.

These are the attributes that can be customized:

* **configure_args**: Dict-like object with the arguments to be passed to the configure script. The keys are the
  argument names and the values their values, or ``None`` for arguments without value.

  - By default the following arguments are passed:

    * ``--prefix``: Takes the ``prefix`` constructor argument, ``/`` as default value.
    * ``--bindir=${prefix}/bin``
    * ``--sbindir=${prefix}/bin``
    * ``--libdir=${prefix}/lib``
    * ``--includedir=${prefix}/include``
    * ``--oldincludedir=${prefix}/include``
    * ``--datarootdir=${prefix}/res``

  - Also, depending on the ``package_type`` of the recipe, it will add by default:

    * ``--enable-shared``, ``--disable-static`` if ``package_type`` is ``shared-library``
    * ``--disable-shared``, ``--enable-static`` if ``package_type`` is ``static-library``

  - When cross-building, ``--host`` and ``--build`` are added with the calculated GNU triplets.

* **make_args** (Defaulted to ``{}``): Dict-like object with the additional arguments to be passed to the make script.
* **autoreconf_args** (Defaulted to ``{"--force": None, "--install": None}``): Dict-like object with the additional arguments
  to be passed to the autoreconf script.
* **extra_defines** (Defaulted to ``[]``): Additional defines.
* **extra_cxxflags** (Defaulted to ``[]``): Additional cxxflags.
* **extra_cflags** (Defaulted to ``[]``): Additional cflags.
* **extra_ldflags** (Defaulted to ``[]``): Additional ldflags.
* **extra_env**: :ref:`Environment<conan_tools_env_environment_model>` object with the extra environment variables to
  define in the generated script. It is initialized with some default values (like the ``CC``, ``CXX``, ``LD``, ``AR``,
  ``NM``, ``OBJDUMP``, ``RANLIB`` and ``STRIP`` variables for MSVC, the Android NDK ones if ``tools.android:ndk_path`` is
  defined, or the ones defined with ``tools.build:compiler_executables``) and the values defined here have precedence over the ones
  calculated by the toolchain.
* **ndebug**: "NDEBUG" if the ``settings.build_type`` is ``Release``, ``RelWithDebInfo`` or ``MinSizeRel``.
* **gcc_cxx11_abi**: "_GLIBCXX_USE_CXX11_ABI" if ``gcc/libstdc++``.
* **libcxx**: Flag calculated from ``settings.compiler.libcxx``.
* **fpic**: True/False from ``options.fPIC`` if defined.
* **cppstd**: Flag from ``settings.compiler.cppstd``
* **arch_flag**: Flag from ``settings.arch``
* **arch_ld_flag**: Linker flag from ``settings.arch``
* **threads_flags**: List of flags to enable threads, if applicable for the compiler.
* **build_type_flags**: Flags from ``settings.build_type``
* **build_type_link_flags**: Linker flags from ``settings.build_type``
* **sysroot_flag**: To pass the ``--sysroot`` flag to the compiler.
* **apple_arch_flag**: Only when cross-building with Apple systems. Flags from ``settings.arch``. For universal binaries, contains multiple ``-arch`` flags.
* **apple_isysroot_flag**: Only when cross-building with Apple systems. Path to the root sdk.
* **apple_min_version_flag**: Only for Apple systems, defines the ``-m{ios,macosx,watchos,tvos,...}-version-min=xxx`` flag.
* **msvc_runtime_flag**: Flag from ``settings.compiler.runtime_type`` when compiler is ``msvc``.
* **msvc_extra_flags**: Extra flags for MSVC (like ``-FS``) that are automatically added to the ``CXXFLAGS`` and ``CFLAGS``.
* **msvc_runtime_link_flags**: Extra linker flags when using ``clang`` with the MSVC runtime.
* **asflags**: List of assembler flags set in the ``ASFLAGS`` environment variable. On Apple platforms,
  populated with ``arch_flag``, ``sysroot_flag``, ``apple_isysroot_flag``, ``apple_arch_flag``, and
  ``apple_min_version_flag``. Empty on non-Apple platforms.


The following attributes are read-only and will contain the calculated values for the current configuration and customized
attributes. Some recipes might need to read them to generate custom build files (not strictly Autotools) with the configuration:

* **defines**
* **cxxflags**
* **cflags**
* **ldflags**
* **rcflags**


.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import GnuToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = GnuToolchain(self)
            # Customize the flags
            tc.extra_cxxflags = ["MyFlag"]
            # Read the computed flags and use them (write custom files etc)
            tc.defines
            tc.cxxflags
            tc.cflags
            tc.ldflags


If you want to change the default values for ``configure_args``, adjust the ``cpp.package`` object at the ``layout()`` method:

    .. code:: python

        def layout(self):
            ...
            # For bindir and sbindir takes the first value:
            self.cpp.package.bindirs = ["mybin"]
            # For libdir takes the first value:
            self.cpp.package.libdirs = ["mylib"]
            # For includedir and oldincludedir takes the first value:
            self.cpp.package.includedirs = ["myinclude"]
            # For datarootdir takes the first value:
            self.cpp.package.resdirs = ["myres"]

    .. note::
        It is **not valid** to change the self.cpp_info  at the ``package_info()`` method.


Managing the configure_args, make_args and autoreconf_args attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``GnuToolchain``, ``configure_args``, ``make_args`` and ``autoreconf_args`` are dict-like Python objects, so they can
be managed with the regular Python dictionary operations. This is the main difference with the ``AutotoolsToolchain``,
that uses lists of strings and some helper methods to modify them. The rules are:

* Key-value are the flags names and their values, e.g., ``{"--enable-tools": "no"}`` will be translated as ``--enable-tools=no``.
* If that flag has no value, then the value must be ``None``, e.g., ``{"--disable-verbose": None}`` will be translated as ``--disable-verbose``.
* Setting a key that already exists will update its value, and deleting a key will remove the flag from the final result.

For instance:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import GnuToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = GnuToolchain(self)
            # add new flag '--new-super-flag'
            tc.configure_args["--new-super-flag"] = None
            # update flag '--host=my-gnu-triplet'
            tc.configure_args["--host"] = "my-gnu-triplet"
            # remove existing '--force' flag
            del tc.autoreconf_args["--force"]
            tc.generate()

The ``GnuToolchain`` will listen to ``tools.gnu:extra_configure_args`` from the
:ref:`reference_config_files_global_conf` to extend the ``configure_args`` attribute.

The ``yes_no()`` helper method returns ``"yes"`` or ``"no"`` depending on the value of a recipe option, which is useful for
the ``--enable-xxx=yes|no`` arguments:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import GnuToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        options = {"with_tools": [True, False]}
        default_options = {"with_tools": True}

        def generate(self):
            tc = GnuToolchain(self)
            # --enable-tools=yes or --enable-tools=no
            tc.configure_args["--enable-tools"] = tc.yes_no("with_tools")
            # Negated, --disable-tools=no or --disable-tools=yes
            tc.configure_args["--disable-tools"] = tc.yes_no("with_tools", negated=True)
            tc.generate()


Customizing the environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your ``Makefile`` or ``configure`` scripts need some other environment variable rather than ``CPPFLAGS``, ``LDFLAGS``,
``CXXFLAGS`` or ``CFLAGS``, you can define them in the ``extra_env`` attribute before calling the ``generate()`` method.
It is an :ref:`Environment<conan_tools_env_environment_model>` object, and the values defined there have precedence over the
ones that the toolchain computes by default:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import GnuToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = GnuToolchain(self)
            tc.extra_env.define("FOO", "BAR")
            # Prepend a compiler wrapper
            tc.extra_env.prepend("CC", "compile")
            # Do not define RANLIB in the generated script
            tc.extra_env.unset("RANLIB")
            tc.generate()

The ``GnuToolchain`` also sets ``CXXFLAGS``, ``CFLAGS``, ``LDFLAGS`` and ``CPPFLAGS`` reading
variables from the ``[conf]`` section in the profiles. :ref:`See the conf reference below<conan_tools_gnu_gnutoolchain_conf>`.


Support for Universal Binaries in macOS
---------------------------------------

Starting in Conan 2.21.0, there's support for building universal binaries on
macOS using ``GnuToolchain``. To specify multiple architectures for a
universal binary in Conan, use the `|` separator when defining the architecture
in the settings. This approach enables passing a list of architectures. For
example, running:

.. code:: bash

    conan create . --name=mylibrary --version=1.0 -s="arch=armv8|x86_64"

will create a universal binary for *mylibrary* containing both ``armv8`` and ``x86_64``
architectures, by setting multiple ``-arch`` flags in the generated toolchain script.

.. warning::

    Attempting to use universal architecture settings on non-Apple platforms
    will result in an error.

    Be aware that this feature is primarily beneficial for building final
    universal binaries for release purposes. The default Conan behavior of
    managing one binary per architecture generally provides a more reliable and
    trouble-free experience. Users should be cautious and not overly rely on
    this feature for broader use cases.


Reference
---------

.. currentmodule:: conan.tools.gnu.gnutoolchain

.. autoclass:: GnuToolchain
    :members:


.. _conan_tools_gnu_gnutoolchain_conf:

conf
^^^^

- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``CXXFLAGS``.
- ``tools.build:cflags`` list of extra of pure C flags that will be used by ``CFLAGS``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``LDFLAGS``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by ``LDFLAGS``.
- ``tools.build:rcflags`` list of extra RC flags to define ``RCFLAGS``
- ``tools.build:defines`` list of preprocessor definitions that will be used by ``CPPFLAGS``.
- ``tools.build:linker_scripts`` list of linker scripts, each of which will be prefixed with ``-T`` and added to ``LDFLAGS``.
  Only use this flag with linkers that supports specifying linker scripts with the ``-T`` flag, such as ``ld``, ``gold``, and ``lld``.
- ``tools.build:sysroot`` defines the ``--sysroot`` flag to the compiler.
- ``tools.gnu:host_triplet`` and ``tools.gnu:build_triplet`` define the GNU triplets used for the ``--host`` and ``--build``
  arguments when cross-building, instead of the automatically calculated ones.
- ``tools.android:ndk_path`` argument for NDK path in case of Android cross-compilation. It is used to set
  some environment variables like ``CC``, ``CXX``, ``LD``, ``STRIP``, ``RANLIB``, ``AS``, ``AR``, ``ADDR2LINE``, ``NM``,
  ``OBJCOPY``, ``OBJDUMP``, ``READELF``, and ``ELFEDIT`` in the *conangnutoolchain.sh|bat* script,
  as long as they are not already defined in the ``buildenv`` environment. If they are defined in the ``buildenv`` environment,
  the ``conangnutoolchain`` file will not define them, leaving their definition to the ``VirtualBuildEnv`` generator.
- ``tools.build:compiler_executables`` dict-like Python object which specifies the
  compiler as key and the compiler executable path as value. Those keys will be mapped as
  follows:

  * ``c``: will set ``CC`` (and ``CC_FOR_BUILD`` if cross-building) in *conangnutoolchain.sh|bat* script.
  * ``cpp``: will set ``CXX`` (and ``CXX_FOR_BUILD`` if cross-building) in *conangnutoolchain.sh|bat* script.
  * ``rc``: will set ``RC`` in *conangnutoolchain.sh|bat* script.
  * ``cuda``: will set ``NVCC`` in *conangnutoolchain.sh|bat* script.
  * ``fortran``: will set ``FC`` in *conangnutoolchain.sh|bat* script.
  * ``objc``: will set ``OBJC`` in *conangnutoolchain.sh|bat* script.
  * ``objcpp``: will set ``OBJCXX`` in *conangnutoolchain.sh|bat* script.
  * ``asm``: will set ``AS`` in *conangnutoolchain.sh|bat* script.
  * ``nm``: will set ``NM`` in *conangnutoolchain.sh|bat* script.
  * ``ranlib``: will set ``RANLIB`` in *conangnutoolchain.sh|bat* script.
  * ``objdump``: will set ``OBJDUMP`` in *conangnutoolchain.sh|bat* script.
  * ``strip``: will set ``STRIP`` in *conangnutoolchain.sh|bat* script.

  Keys not listed above are reported with a ``risk`` warning.
- ``tools.gnu:extra_configure_args`` list of arguments to extend the ``configure_args`` attribute of ``GnuToolchain``.
- ``tools.apple:enable_arc`` boolean to add ``-fobjc-arc`` (or ``-fno-objc-arc`` if ``False``) to ``OBJCFLAGS`` and ``OBJCXXFLAGS``.


.. note::

    **flags order of preference**: Flags specified in the `tools.build` configuration,
    such as `cxxflags`, `cflags`, `sharedlinkflags`, `exelinkflags`, and `defines`, will
    always take precedence over those set by the GnuToolchain attributes.
