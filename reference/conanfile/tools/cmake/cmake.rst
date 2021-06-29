
CMake
-----

.. warning::

    These tools are **experimental** and subject to breaking changes.


The ``CMake`` build helper is a wrapper around the command line invocation of cmake. It will abstract the
calls like ``cmake --build . --config Release`` into Python method calls. It will also add the argument
``-DCMAKE_TOOLCHAIN_FILE=conantoolchain.cmake`` to the ``configure()`` call.

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

    def __init__(self, conanfile, build_folder=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``build_folder``: Relative path to a folder to contain the temporary build files


configure()
+++++++++++

.. code:: python

    def configure(self, source_folder=None):

Calls ``cmake``, with the generator defined in the ``cmake_generator`` field of the
``conanbuild.json`` file, and passing ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake``.
If ``conanbuild.json`` file is not there, no generator will be passed.

- ``source_folder``: Relative path to the folder containing the root *CMakeLists.txt*


build()
+++++++

.. code:: python

    def build(self, build_type=None, target=None):


Calls the build system. Equivalent to :command:`cmake --build .` in the build folder.


- ``build_type``: Use it only to override the value defined in the ``settings.build_type`` for a multi-configuration generator (e.g. Visual Studio, XCode).
  This value will be ignored for single-configuration generators, they will use the one defined in the toolchain file during the install step.
- ``target``: name of the build target to run.


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

    def test(self, build_type=None, target=None, output_on_failure=False):


Equivalent to running :command:`cmake --build . --target=RUN_TESTS`.

- ``build_type``: Use it only to override the value defined in the ``settings.build_type``. It
  can fail if the build is single configuration (e.g. Unix Makefiles), as in that case the build
  type must be specified at configure time, not build type.
- ``target``: name of the build target to run, by default ``RUN_TESTS`` or ``test``.


conf
++++

- ``tools.microsoft.msbuild:verbosity`` will accept one of ``"Quiet", "Minimal", "Normal", "Detailed", "Diagnostic"`` to be passed
  to the ``CMake.build()`` command, when a Visual Studio generator (MSBuild build system) is being used for CMake. It is passed as
  an argument to the underlying build system via the call ``cmake --build . --config Release -- /verbosity:Diagnostic``

- ``tools.ninja:jobs`` argument for the ``--jobs`` parameter when running Ninja generator. (overrides
  the general ``tools.build:processes``).

- ``tools.microsoft.msbuild:max_cpu_count`` argument for the ``/m`` (``/maxCpuCount``) when running
  ``MSBuild`` (overrides the general ``tools.build:processes``).


Properties
++++++++++

The following properties affect the CMakeDeps generator:

- **cmake_file_name**: The config file generated for the current package will follow the ``<VALUE>-config.cmake`` pattern,
  so to find the package you write ``find_package(<VALUE>)``.
- **cmake_target_name**: Name of the target to be consumed. When set on the root ``cpp_info``,
  it changes the namespace of the target. When set to a component, it changes the name of the target
  (see the example below).
- **cmake_build_modules**: List of ``.cmake`` files (route relative to root package folder) that are automatically
  included when the consumer run the ``find_package()``.
- **skip_deps_file**: It tells the ``CMakeDeps`` generator to skip the creation of files for the package declaring
  this property. It can be used, for instance, to create a system wrapper package so the consumers find
  the config files in the CMake installation config path and not in the generated by Conan (because it has been skipped).

Example:

.. code-block:: python

    def package_info(self):
        ...
        # MyFileName-config.cmake
        self.cpp_info.set_property("cmake_file_name", "MyFileName")
        # Foo:: namespace for the targets (Foo::Foo if no components)
        self.cpp_info.set_property("cmake_target_name", "Foo")
        # Foo::Var target name for the component "mycomponent"
        self.cpp_info.components["mycomponent"].set_property("cmake_target_name", "Var")
        # Automatically include the lib/mypkg.cmake file when calling find_package()
        self.cpp_info.components["mycomponent"].set_property("cmake_build_modules", [os.path.join("lib", "mypkg.cmake")])

        # Skip this package when generating the files for the whole dependency tree in the consumer
        # note: it will make useless the previous adjustements.
        self.cpp_info.set_property("skip_deps_file", True)

