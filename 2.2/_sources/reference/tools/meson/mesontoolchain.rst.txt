.. _conan_tools_meson_mesontoolchain:

MesonToolchain
==============

.. _MesonToolchain:

.. important::

    This class will generate files that are only compatible with Meson versions >= 0.55.0


The ``MesonToolchain`` is the toolchain generator for Meson and it can be used in the ``generate()`` method
as follows:


.. code:: python

    from conan import ConanFile
    from conan.tools.meson import MesonToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False]}
        default_options = {"shared": False}

        def generate(self):
            tc = MesonToolchain(self)
            tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
            tc.generate()


.. important::

    When your recipe has dependencies ``MesonToolchain`` only works with the ``PkgConfigDeps`` generator.
    Please, do not use other generators, as they can have overlapping definitions that can conflict.


Generated files
-----------------

The ``MesonToolchain`` generates the following files after a :command:`conan install` (or when building the package
in the cache) with the information provided in the ``generate()`` method as well as information
translated from the current ``settings``, ``conf``, etc.:

-  *conan_meson_native.ini*: if doing a native build.
-  *conan_meson_cross.ini*: if doing a cross-build (:ref:`conan_tools_build`).

conan_meson_native.ini
+++++++++++++++++++++++++

This file contains the definitions of all the Meson properties related to the Conan options
and settings for the current package, platform, etc. This includes but is not limited to the following:

* Detection of ``default_library`` from Conan settings.

    * Based on existence/value of an option named ``shared``.

* Detection of ``buildtype`` from Conan settings.

* Definition of the C++ standard as necessary.

* The Visual Studio runtime (``b_vscrt``), obtained from Conan input settings.


conan_meson_cross.ini
++++++++++++++++++++++++

This file contains the same information as the previous *conan_meson_native.ini*,
but with additional information to describe host, target, and build machines (such as the processor architecture).


Check out the meson documentation for more details on native and cross files:

* `Machine files <https://mesonbuild.com/Machine-files.html>`_
* `Native environments <https://mesonbuild.com/Native-environments.html>`_
* `Cross compilation <https://mesonbuild.com/Cross-compilation.html>`_


Default directories
+++++++++++++++++++++

``MesonToolchain`` manages some of the directories used by Meson. These are variables declared under
the ``[project options]`` section of the files `conan_meson_native.ini` and `conan_meson_cross.ini`
(see more information about `Meson directories <https://mesonbuild.com/Builtin-options.html#directories>`__):


``bindir``: value coming from ``self.cpp.package.bindirs``. Defaulted to None.
``sbindir``: value coming from ``self.cpp.package.bindirs``. Defaulted to None.
``libexecdir``: value coming from ``self.cpp.package.bindirs``. Defaulted to None.
``datadir``: value coming from ``self.cpp.package.resdirs``. Defaulted to None.
``localedir``: value coming from ``self.cpp.package.resdirs``. Defaulted to None.
``mandir``: value coming from ``self.cpp.package.resdirs``. Defaulted to None.
``infodir``: value coming from ``self.cpp.package.resdirs``. Defaulted to None.
``includedir``: value coming from ``self.cpp.package.includedirs``. Defaulted to None.
``libdir``: value coming from ``self.cpp.package.libdirs``. Defaulted to None.

Notice that it needs a ``layout`` to be able to initialize those ``self.cpp.package.xxxxx`` variables. For instance:

.. code:: python

    from conan import ConanFile
    from conan.tools.meson import MesonToolchain
    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        def layout(self):
            self.folders.build = "build"
            self.cpp.package.resdirs = ["res"]
        def generate(self):
            tc = MesonToolchain(self)
            self.output.info(tc.project_options["datadir"])  # Will print '["res"]'
            tc.generate()

.. note::

    All of them are saved only if they have any value. If the values are``None``, they won't be mentioned
    in ``[project options]`` section.


Customization
---------------

Attributes
+++++++++++++

project_options
^^^^^^^^^^^^^^^

This attribute allows defining Meson project options:

.. code:: python

    def generate(self):
        tc = MesonToolchain(self)
        tc.project_options["MYVAR"] = "MyValue"
        tc.generate()

This is translated to:

- One project options definition for ``MYVAR`` in ``conan_meson_native.ini`` or ``conan_meson_cross.ini`` file.

The ``wrap_mode: nofallback`` is defined by default as a project option, to make sure that dependencies are found in Conan packages. It is possible to change or remove it with:

.. code:: python

    def generate(self):
        tc = MesonToolchain(self)
        tc.project_options.pop("wrap_mode")
        tc.generate()

Note that in this case, Meson might be able to find dependencies in "wraps", it is the responsibility of the user to check the behavior and make sure about the dependencies origin.

preprocessor_definitions
^^^^^^^^^^^^^^^^^^^^^^^^

This attribute allows defining compiler preprocessor definitions, for multiple configurations (Debug, Release, etc).

.. code:: python

    def generate(self):
        tc = MesonToolchain(self)
        tc.preprocessor_definitions["MYDEF"] = "MyValue"
        tc.generate()

This is translated to:

- One preprocessor definition for ``MYDEF`` in ``conan_meson_native.ini`` or ``conan_meson_cross.ini`` file.

conf
++++++

``MesonToolchain`` is affected by these ``[conf]`` variables:

- ``tools.meson.mesontoolchain:backend``. the meson `backend
  <https://mesonbuild.com/Configuring-a-build-directory.html>`_ to use. Possible values:
  ``ninja``, ``vs``, ``vs2010``, ``vs2015``, ``vs2017``, ``vs2019``, ``xcode``.
- ``tools.apple:sdk_path`` argument for SDK path in case of Apple cross-compilation. It is used as value
  of the flag ``-isysroot``.
- ``tools.android:ndk_path`` argument for NDK path in case of Android cross-compilation. It is used to get
  some binaries like ``c``, ``cpp`` and ``ar`` used in ``[binaries]`` section from *conan_meson_cross.ini*.
- ``tools.build:cxxflags`` list of extra C++ flags that is used by ``cpp_args``.
- ``tools.build:cflags`` list of extra of pure C flags that is used by ``c_args``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that is used by ``c_link_args`` and ``cpp_link_args``.
- ``tools.build:exelinkflags`` list of extra linker flags that is used by ``c_link_args`` and ``cpp_link_args``.
- ``tools.build:linker_scripts`` list of linker scripts, each of which will be prefixed with ``-T`` and passed to ``c_link_args`` and
  ``cpp_link_args``. Only use this flag with linkers that supports specifying linker scripts with the ``-T`` flag, such as ``ld``, ``gold``,
  and ``lld``.
- ``tools.build:compiler_executables`` dict-like Python object which specifies the compiler as key
  and the compiler executable path as value. Those keys will be mapped as follows:

  * ``c``: will set ``c`` in ``[binaries]`` section from *conan_meson_xxxx.ini*.
  * ``cpp``: will set ``cpp`` in ``[binaries]`` section from *conan_meson_xxxx.ini*.
  * ``objc``: will set ``objc`` in ``[binaries]`` section from *conan_meson_xxxx.ini*.
  * ``objcpp``: will set ``objcpp`` in ``[binaries]`` section from *conan_meson_xxxx.ini*.


Using Proper Data Types for Conan Options in Meson
--------------------------------------------------

Always transform Conan options into valid Python data types before assigning them as Meson
values:

.. code:: python

    options = {{"shared": [True, False], "fPIC": [True, False], "with_msg": ["ANY"]}}
    default_options = {{"shared": False, "fPIC": True, "with_msg": "Hi everyone!"}}

    def generate(self):
        tc = MesonToolchain(self) 
        tc.project_options["DYNAMIC"] = bool(self.options.shared)  # shared is bool
        tc.project_options["GREETINGS"] = str(self.options.with_msg)  # with_msg is str 
        tc.generate()

In contrast, directly assigning a Conan option as a Meson value is strongly discouraged:

.. code:: python

    options = {{"shared": [True, False], "fPIC": [True, False], "with_msg": ["ANY"]}}
    default_options = {{"shared": False, "fPIC": True, "with_msg": "Hi everyone!"}}
    # ...
    def generate(self):
        tc = MesonToolchain(self)
        tc.project_options["DYNAMIC"] = self.options.shared  # == <PackageOption object>
        tc.project_options["GREETINGS"] = self.options.with_msg  # == <PackageOption object>
        tc.generate()

These are not boolean or string values but an internal Conan class representing such
option values. If you assign these values directly, upon executing the `generate()`
function, you should receive a warning in your console stating, ``WARN: deprecated:
Please, do not use a Conan option value directly.`` This method is considered bad practice
as it can result in unexpected errors during your project's build process.


Cross-building for Apple and Android
-------------------------------------

The ``MesonToolchain`` adds all the flags required to cross-compile for Apple (MacOS M1, iOS, etc.) and Android.

**Apple**

It adds link flags ``-arch XXX``, ``-isysroot [SDK_PATH]`` and the minimum deployment target flag, e.g., ``-mios-version-min=8.0``
to the ``MesonToolchain`` ``c_args``, ``c_link_args``, ``cpp_args``, and ``cpp_link_args`` attributes, given the
Conan settings for any Apple OS (iOS, watchOS, etc.) and the ``tools.apple:sdk_path`` configuration value like it's shown
in this example of host profile:

.. code-block:: text
    :caption: **ios_host_profile**

    [settings]
    os = iOS
    os.version = 10.0
    os.sdk = iphoneos
    arch = armv8
    compiler = apple-clang
    compiler.version = 12.0
    compiler.libcxx = libc++

    [conf]
    tools.apple:sdk_path=/my/path/to/iPhoneOS.sdk

Objective-C arguments
++++++++++++++++++++++

In Apple OS's there are also specific Objective-C/Objective-C++ arguments: ``objc``,
``objcpp``, ``objc_args``, ``objc_link_args``, ``objcpp_args``, and ``objcpp_link_args``,
as public attributes of the ``MesonToolchain`` class, where the variables ``objc`` and
``objcpp`` are initialized as ``clang`` and ``clang++`` respectively by default.


**Android**

It initializes the ``MesonToolchain`` ``c``, ``cpp``, and ``ar`` attributes, which are needed to cross-compile for Android, given the
Conan settings for Android and the ``tools.android:ndk_path`` configuration value like it's shown
in this example of host profile:


.. code-block:: text
    :caption: **android_host_profile**

    [settings]
    os = Android
    os.api_level = 21
    arch = armv8

    [conf]
    tools.android:ndk_path=/my/path/to/NDK


.. seealso::

    - :ref:`Getting started with Meson<examples_tools_meson_toolchain_build_simple_meson_project>`


.. _MesonToolchain Reference:

Reference
---------

.. currentmodule:: conan.tools.meson

.. autoclass:: MesonToolchain
    :members:
