.. _conan_tools_gnu_autotools_toolchain:

AutotoolsToolchain
==================

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.


The ``AutotoolsToolchain`` is the toolchain generator for Autotools. It will generate shell scripts containing
environment variable definitions that the autotools build system can understand.

.. important::

    This class will require very soon to define both the "host" and "build" profiles. It is very recommended to
    start defining both profiles immediately to avoid future breaking. Furthermore, some features, like trying to
    cross-compile might not work at all if the "build" profile is not provided.

The ``AutotoolsToolchain`` generator can be used by name in conanfiles:

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

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsToolchain(self)
            tc.generate()

The ``AutotoolsToolchain`` will generate after a ``conan install`` command the *conanautotoolstoolchain.sh* or *conanautotoolstoolchain.bat* files:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ source conanautotoolstoolchain.sh
    # or in Windows
    $ conanautotoolstoolchain.bat

This generator will append information to the ``CPPFLAGS``, ``LDFLAGS``, ``CXXFLAGS``,
``CFLAGS`` environment variables that translate the settings and options to the
corresponding build flags like ``-stdlib=libstdc++``, ``-std=gnu14``, architecture flags,
etc. It will also append the folder where the Conan generators are located to the
``PKG_CONFIG_PATH`` environment variable.

This generator will also generate a file called ``conanbuild.conf`` containing two keys:

- **configure_args**: Arguments to call the ``configure`` script.
- **make_args**: Arguments to call the ``make`` script.
- **autoreconf_args**: Arguments to call the ``autoreconf`` script.

The :ref:`Autotools build helper<conan_tools_gnu_build_helper>` will use that ``conanbuild.conf`` file to seamlessly call
the configure and make script using these precalculated arguments.

It supports the following methods and attributes:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, namespace=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: this argument avoids collisions when you have multiple toolchain calls in the same
  recipe. By setting this argument, the *conanbuild.conf* file used to pass information to the build
  helper will be named as: *<namespace>_conanbuild.conf*. The default value is ``None`` meaning that
  the name of the generated file is *conanbuild.conf*. This namespace must be also set with the same
  value in the constructor of the :ref:`Autotools build helper<conan_tools_gnu_build_helper>` so that
  it reads the information from the proper file.


Attributes
++++++++++

You can change some attributes before calling the ``generate()`` method if you want to change some of the precalculated
values:

.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsToolchain(self)
            tc.configure_args.append("--my_argument")
            tc.generate()


* **configure_args**: Additional arguments to be passed to the configure script.
    - By default the following arguments are passed:
        * ``--prefix``: With the self.package_folder value.
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
* **defines** (Defaulted to ``[]``): Additional defines.
* **cxxflags** (Defaulted to ``[]``): Additional cxxflags.
* **cflags** (Defaulted to ``[]``): Additional cflags.
* **ldflags** (Defaulted to ``[]``): Additional ldflags.
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


conf
+++++

``AutotoolsToolchain`` is affected by these :ref:`[conf]<global_conf>` variables:

- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``CXXFLAGS``.
- ``tools.build:cflags`` list of extra of pure C flags that will be used by ``CFLAGS``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``LDFLAGS``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by by ``LDFLAGS``.
- ``tools.build:defines`` list of preprocessor definitions that will be used by ``CPPFLAGS``.
- ``tools.build:sysroot`` defines the ``--sysroot`` flag to the compiler.


Customizing the environment
+++++++++++++++++++++++++++

If your ``Makefile`` or ``configure`` scripts need some other environment variable rather than ``CPPFLAGS``, ``LDFLAGS``,
``CXXFLAGS`` or ``CFLAGS``, you can customize it before calling the ``generate()`` method.
Call the ``environment()`` method to calculate the mentioned variables and then add the variables that you need.
The ``environment()`` method returns an :ref:`Environment<conan_tools_env_environment_model>` object:


.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            at = AutotoolsToolchain(self)
            env = at.environment()
            env.define("FOO", "BAR")
            at.generate(env)