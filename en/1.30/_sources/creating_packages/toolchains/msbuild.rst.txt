MSBuildToolchain
================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


The ``MSBuildToolchain`` can be used in the ``toolchain()`` method:


.. code:: python

    from conans import ConanFile, MSBuildToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        generators = "msbuild"
        options = {"shared": [True, False]}
        default_options = {"shared": False}

        def toolchain(self):
            tc = MSBuildToolchain(self)
            tc.write_toolchain_files()


The ``MSBuildToolchain`` will generate two files after a ``conan install`` command or
before calling the ``build()`` method when the package is building in the cache:

- The main *conan_toolchain.props* file, that can be used in the command line.
- A *conan_toolchain_<config>.props* file, that will be conditionally included from the previous
  *conan_toolchain.props* file based on the configuration, platform and toolset, e.g.:
  *conan_toolchain_Release_x86_v140.props*

Every invocation to ``conan install`` with different configuration will create a new properties ``.props``
file, that will also be conditionally included. This allows to install different sets of dependencies,
then switch among them directly from the Visual Studio IDE.

The toolchain files can configure:

- The Visual Studio runtime (MT/MD/MTd/MDd), obtained from Conan input settings
- The C++ standard, obtained from Conan input settings


Generators
----------

The ``MSBuildToolchain`` only works with the ``msbuild`` generator.
Please, do not use other generators, as they can have overlapping definitions that can conflict.


Using the toolchain in developer flow
-------------------------------------

One of the advantages of using Conan toolchains is that they can help to achieve the exact same build
with local development flows, than when the package is created in the cache.

With the ``MSBuildToolchain`` it is possible to do:

.. code:: bash

    # Lets start in the folder containing the conanfile.py
    $ mkdir build && cd build
    # Install both debug and release deps and create the toolchain
    $ conan install ..
    $ conan install .. -s build_type=Debug
    # Add ``conan_toolchain.props`` in your IDE to the project properties
    # No need to add the configuration .props files. This needs to be done only once
    # If you have dependencies, you will need to add the .props files of the dependencies
    # too, check the "msbuild" generator
    # Open Visual Studio IDE and build, switching configurations directly in the IDE


MSBuild build helper
---------------------

.. warning::

    The existing ``MSBuild`` helper is not suitable to be used with toolchain yet. A new
    helper will be added in future releases.


At the moment there is no build helper to work with the ``MSBuildToolchain``. Call directly
``msbuild`` in your recipes to build your project, something like:

.. code:: python

    def build(self):
        vs_path = vs_installation_path("15")
        vcvars_path = os.path.join(vs_path, "VC/Auxiliary/Build/vcvarsall.bat")

        platform_arch = "x86" if self.settings.arch == "x86" else "x64"
        build_type = self.settings.build_type
        cmd = ('set "VSCMD_START_DIR=%%CD%%" && '
                   '"%s" x64 && msbuild "MyProject.sln" /p:Configuration=%s '
                   '/p:Platform=%s ' % (vcvars_path, build_type, platform_arch))
        self.run(cmd)
