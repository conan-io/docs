.. _conan-cmake-build-helper:

CMake
-----

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.


The ``CMake`` build helper is a wrapper around the command line invocation of cmake. It will abstract the
calls like ``cmake --build . --config Release`` into Python method calls. It will also add the argument
``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake`` to the ``configure()`` call.

The helper is intended to be used in the ``build()`` method, to call CMake commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conans import ConanFile
    from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()
            deps = CMakeDeps(self)
            deps.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

**Note:** This helper includes the additional flag `-DCMAKE_SH="CMAKE_SH-NOTFOUND"` when using the `MinGW Makefiles` CMake's
generator, to avoid the error of `sh` being in the PATH (CMake version < 3.17.0).

It supports the following methods:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, namespace=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: this argument avoids collisions when you have multiple toolchain calls in the same
  recipe. By setting this argument the *conanbuild.conf* file used to pass some information to the
  toolchain will be named as: *<namespace>_conanbuild.conf*. The default value is ``None`` meaning that
  the name of the generated file is *conanbuild.conf*. This namespace must be also set with the same
  value in the constructor of the :ref:`CMakeToolchain<conan-cmake-toolchain>` so that it reads the
  information from the proper file.

configure()
+++++++++++

.. code:: python

    def configure(self, variables=None, build_script_folder=None):

Calls ``cmake``, with the generator defined in the ``cmake_generator`` field of the
``conanbuild.conf`` file, and passing ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake``.

.. important::

    If ``conanbuild.conf`` file is not there, Conan will raise an exception because it's a mandatory one even though it's empty.


- ``build_script_folder``: Relative path to the folder containing the root *CMakeLists.txt*
- ``variables``: should be a dictionary of CMake variables and values, that will be mapped to command line ``-DVAR=VALUE`` arguments.
  Recall that in the general case information to CMake should be passed in ``CMakeToolchain`` to be provided in the ``conan_toolchain.cmake`` file.
  This ``variables`` argument is intended for exceptional cases that wouldn't work in the toolchain approach.


build()
+++++++

.. code:: python

    def build(self, build_type=None, target=None, cli_args=None, build_tool_args=None):


Calls the build system. Equivalent to :command:`cmake --build .` in the build folder.


- ``build_type``: Use it only to override the value defined in the ``settings.build_type`` for a multi-configuration generator (e.g. Visual Studio, XCode).
  This value will be ignored for single-configuration generators, they will use the one defined in the toolchain file during the install step.
- ``target``: name of the build target to run.
- ``cli_args``: A list of arguments ``[arg1, arg2, ...]`` that will be passed to the ``cmake --build ... arg1 arg2`` command directly.
- ``build_tool_args``: A list of arguments ``[barg1, barg2, ...]`` for the underlying build system that will be passed to the command line after the ``--``
  indicator: ``cmake --build ... -- barg1 barg2``


install()
+++++++++

.. code:: python

    def install(self, build_type=None):


Equivalent to run ``cmake --build . --target=install``

- ``build_type``: Use it only to override the value defined in the ``settings.build_type``. It
  can fail if the build is single configuration (e.g. Unix Makefiles), as in that case the build
  type must be specified at configure time, not build type.


test()
++++++

.. code:: python

    def test(self, build_type=None, target=None, cli_args=None, build_tool_args=None):


Equivalent to running :command:`cmake --build . --target=RUN_TESTS`.

- ``build_type``: Use it only to override the value defined in the ``settings.build_type``. It
  can fail if the build is single configuration (e.g. Unix Makefiles), as in that case the build
  type must be specified at configure time, not build type.
- ``target``: name of the build target to run, by default ``RUN_TESTS`` or ``test``.
- ``cli_args``: Same as above ``build()``
- ``build_tool_args``: Same as above ``build()``


conf
++++

- ``tools.microsoft.msbuild:verbosity`` will accept one of ``"Quiet", "Minimal", "Normal", "Detailed", "Diagnostic"`` to be passed
  to the ``CMake.build()`` command, when a Visual Studio generator (MSBuild build system) is being used for CMake. It is passed as
  an argument to the underlying build system via the call ``cmake --build . --config Release -- /verbosity:Diagnostic``

- ``tools.build:jobs`` argument for the ``--jobs`` parameter when running Ninja generator.

- ``tools.microsoft.msbuild:max_cpu_count`` argument for the ``/m`` (``/maxCpuCount``) when running
  ``MSBuild``
