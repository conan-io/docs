.. _conan_tools_gnu_autotoolstoolchain:

AutotoolsToolchain
==================

The ``AutotoolsToolchain`` is the toolchain generator for Autotools. It will generate shell scripts containing
environment variable definitions that the autotools build system can understand.

This generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "AutotoolsToolchain"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    AutotoolsToolchain

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsToolchain(self)
            tc.generate()


Generated files
---------------

It will generate the file ``conanautotoolstoolchain.sh`` or ``conanautotoolstoolchain.bat`` files:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ source conanautotoolstoolchain.sh
    # or in Windows
    $ conanautotoolstoolchain.bat

This launchers will append information to the ``CPPFLAGS``, ``LDFLAGS``, ``CXXFLAGS``,
``CFLAGS`` environment variables that translate the settings and options to the
corresponding build flags like ``-stdlib=libstdc++``, ``-std=gnu14``, architecture flags,
etc. It will also append the folder where the Conan generators are located to the
``PKG_CONFIG_PATH`` environment variable.

Since `Conan 2.4.0 <https://github.com/conan-io/conan/releases/tag/2.4.0>`__,
in  a cross-building context, the environment variables ``CC_FOR_BUILD`` and ``CXX_FOR_BUILD`` are also set if the
build profile defines the ``c`` and ``cpp`` values in the configuration variable ``tools.build:compiler_executables``.
See more info in the :ref:`conf section<conan_tools_gnu_autotoolstoolchain_conf>`.

This generator will also generate a file called ``conanbuild.conf`` containing two keys:

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
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsToolchain(self)
            tc.configure_args.append("--my_argument")
            tc.generate()


* **configure_args**: Additional arguments to be passed to the configure script.
    - By default the following arguments are passed:
        * ``--prefix``: Takes ``/`` as default value.
        * ``--bindir=${prefix}/bin``
        * ``--sbindir=${prefix}/bin``
        * ``--libdir=${prefix}/lib``
        * ``--includedir=${prefix}/include``
        * ``--oldincludedir=${prefix}/include``
        * ``--datarootdir=${prefix}/res``
    - Also if the shared option exists it will add by default:
        * ``--enable-shared``, ``--disable-static`` if ``shared==True``
        * ``--disable-shared``, ``--enable-static`` if ``shared==False``

* **make_args** (Defaulted to ``[]``): Additional arguments to be passed to he make script.
* **autoreconf_args** (Defaulted to ``["--force", "--install"]``): Additional arguments to be passed to he make script.
* **extra_defines** (Defaulted to ``[]``): Additional defines.
* **extra_cxxflags** (Defaulted to ``[]``): Additional cxxflags.
* **extra_cflags** (Defaulted to ``[]``): Additional cflags.
* **extra_ldflags** (Defaulted to ``[]``): Additional ldflags.
* **ndebug**: "NDEBUG" if the ``settings.build_type`` != `Debug`.
* **gcc_cxx11_abi**: "_GLIBCXX_USE_CXX11_ABI" if ``gcc/libstdc++``.
* **libcxx**: Flag calculated from ``settings.compiler.libcxx``.
* **fpic**: True/False from ``options.fpic`` if defined.
* **cppstd**: Flag from ``settings.compiler.cppstd``
* **arch_flag**: Flag from ``settings.arch``
* **build_type_flags**: Flags from ``settings.build_type``
* **sysroot_flag**: To pass the ``--sysroot`` flag to the compiler.
* **apple_arch_flag**: Only when cross-building with Apple systems. Flags from ``settings.arch``.
* **apple_isysroot_flag**: Only when cross-building with Apple systems. Path to the root sdk.
* **msvc_runtime_flag**: Flag from ``settings.compiler.runtime_type`` when compiler is ``msvc`` or
  ``settings.compiler.runtime`` when using the deprecated ``Visual Studio``.

The following attributes are ready-only and will contain the calculated values for the current configuration and customized
attributes. Some recipes might need to read them to generate custom build files (not strictly Autotools) with the configuration:

* **defines**
* **cxxflags**
* **cflags**
* **ldflags**


.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        def generate(self):
            tc = AutotoolsToolchain(self)
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


Customizing the environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your ``Makefile`` or ``configure`` scripts need some other environment variable rather than ``CPPFLAGS``, ``LDFLAGS``,
``CXXFLAGS`` or ``CFLAGS``, you can customize it before calling the ``generate()`` method.
Call the ``environment()`` method to calculate the mentioned variables and then add the variables that you need.
The ``environment()`` method returns an :ref:`Environment<conan_tools_env_environment_model>` object:


.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            at = AutotoolsToolchain(self)
            env = at.environment()
            env.define("FOO", "BAR")
            at.generate(env)


The ``AutotoolsToolchain`` also sets ``CXXFLAGS``, ``CFLAGS``, ``LDFLAGS`` and ``CPPFLAGS`` reading
variables from the ``[conf]`` section in the profiles. :ref:`See the conf reference below<conan_tools_gnu_autotoolstoolchain_conf>`.


Managing the configure_args, make_args and autoreconf_args attributes
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

``AutotoolsToolchain`` provides some help methods so users can add/update/remove values defined in ``configure_args``,
``make_args`` and ``autoreconf_args`` (all of them lists of strings). Those methods are:

* ``update_configure_args(updated_flags)``: will change ``AutotoolsToolchain.configure_args``.
* ``update_make_args(updated_flags)``: will change ``AutotoolsToolchain.make_args``.
* ``update_autoreconf_args(updated_flags)``: will change ``AutotoolsToolchain.autoreconf_args``.

Where ``updated_flags`` is a dict-like Python object defining all the flags to change. It follows the next rules:

* Key-value are the flags names and their values, e.g., ``{"--enable-tools": no}`` will be translated as ``--enable-tools=no``.
* If that key has no value, then it will be an empty string, e.g., ``{"--disable-verbose": ""}`` will be translated as ``--disable-verbose``.
* If the key value is ``None``, it means that you want to remove that flag from the ``xxxxxx_args`` (notice that it could
  be ``configure_args``, ``make_args`` or ``autoreconf_args``), e.g., ``{"--force": None}`` will remove that flag from the final result.

In a nutshell, you will:

* **Add arguments**: if the given flag in ``updated_flags`` does not already exist in ``xxxxxx_args``.
* **Update arguments**: if the given flag in ``updated_flags`` already exists in attribute ``xxxxxx_args``.
* **Remove arguments**: if the given flag in ``updated_flags`` already exists in ``xxxxxx_args`` and it's passed with ``None`` as value.

For instance:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            at = AutotoolsToolchain(self)
            at.update_configure_args({
                "--new-super-flag": "",  # add new flag '--new-super-flag'
                "--host": "my-gnu-triplet",  # update flag '--host=my-gnu-triplet'
                "--force": None  # remove existing '--force' flag
            })
            at.generate()


Reference
---------

.. currentmodule:: conan.tools.gnu.autotoolstoolchain

.. autoclass:: AutotoolsToolchain
    :members:


.. _conan_tools_gnu_autotoolstoolchain_conf:

conf
^^^^

- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``CXXFLAGS``.
- ``tools.build:cflags`` list of extra of pure C flags that will be used by ``CFLAGS``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``LDFLAGS``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by ``LDFLAGS``.
- ``tools.build:defines`` list of preprocessor definitions that will be used by ``CPPFLAGS``.
- ``tools.build:linker_scripts`` list of linker scripts, each of which will be prefixed with ``-T`` and added to ``LDFLAGS``.
  Only use this flag with linkers that supports specifying linker scripts with the ``-T`` flag, such as ``ld``, ``gold``, and ``lld``.
- ``tools.build:sysroot`` defines the ``--sysroot`` flag to the compiler.
- ``tools.android:ndk_path`` (*new since Conan 2.5.0*) argument for NDK path in case of Android cross-compilation. It is used to set
  some environment variables like ``CC``, ``CXX``, ``LD``, ``STRIP``, ``RANLIB``, ``AS``, and ``AR`` in the *conanautotoolstoolchain.sh|bat* script.
- ``tools.build:compiler_executables`` dict-like Python object which specifies the
  compiler as key and the compiler executable path as value. Those keys will be mapped as
  follows:

  * ``c``: will set ``CC`` (and ``CC_FOR_BUILD`` if cross-building) in *conanautotoolstoolchain.sh|bat* script.
  * ``cpp``: will set ``CXX`` (and ``CXX_FOR_BUILD`` if cross-building) in *conanautotoolstoolchain.sh|bat* script.
  * ``rc``: will set ``RC`` in *conanautotoolstoolchain.sh|bat* script.
  * ``cuda``: will set ``NVCC`` in *conanautotoolstoolchain.sh|bat* script.
  * ``fortran``: will set ``FC`` in *conanautotoolstoolchain.sh|bat* script.


.. note::

    **flags order of preference**: Flags specified in the `tools.build` configuration,
    such as `cxxflags`, `cflags`, `sharedlinkflags`, `exelinkflags`, and `defines`, will
    always take precedence over those set by the AutotoolsToolchain attributes.
