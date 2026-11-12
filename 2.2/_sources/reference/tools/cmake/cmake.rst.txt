.. _conan_tools_cmake_helper:

CMake
=====

The ``CMake`` build helper is a wrapper around the command line invocation of cmake. It will abstract the
calls like ``cmake --build . --config Release`` into Python method calls. It will also add the argument
``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake`` (from the generator ``CMakeToolchain``) to the ``configure()`` call,
as well as other possible arguments like ``-DCMAKE_BUILD_TYPE=<config>``. The arguments that will be used are obtained from a 
generated ``CMakePresets.json`` file.

The helper is intended to be used in the ``build()`` method, to call CMake commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conan import ConanFile
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



Reference
---------

.. currentmodule:: conan.tools.cmake.cmake

.. autoclass:: CMake
    :members:


conf
^^^^

The ``CMake()`` build helper is affected by these ``[conf]`` variables:

- ``tools.build:verbosity`` will accept one of ``quiet`` or ``verbose`` to be passed to the ``CMake.build()`` command,
  when a Visual Studio generator (MSBuild build system) is being used for CMake. It is passed as
  an argument to the underlying build system via the call ``cmake --build . --config Release -- /verbosity:Diagnostic``

- ``tools.compilation:verbosity`` will accept one of ``quiet`` or ``verbose`` to be passed to CMake,
  which sets ``-DCMAKE_VERBOSE_MAKEFILE`` if ``verbose``

- ``tools.build:jobs`` argument for the ``--jobs`` parameter when running Ninja generator.

- ``tools.microsoft.msbuild:max_cpu_count`` argument for the ``/m`` (``/maxCpuCount``) when running
  ``MSBuild``

- ``tools.cmake:cmake_program`` specify the location of the CMake executable, instead of using the one found in the ``PATH``.

- ``tools.cmake:install_strip`` will pass ``--strip`` to the ``cmake --install`` call if set to ``True``.
