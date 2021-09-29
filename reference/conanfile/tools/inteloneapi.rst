.. _conan_tools_inteloneapi:


IntelOneAPI
============

.. warning::

    These tools are **experimental** and subject to breaking changes.


Available since: `1.41.0 <https://github.com/conan-io/conan/releases>`_


This section explains how to use the new Intel oneAPI `DPC++/C++ <https://software.intel.com/content/www/us/en/develop/documentation/oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top.html>`_ and
`Classic <https://software.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top.html>`_ compilers in Conan.

.. note::
    This new compilers are only integrated with new toolchains.

.. note::
    Intel oneAPI DPC++/C++ only supports Linux and Windows.


How to use
----------

It can be declared into your local profile, e.g. *myprofile*, as follows:


.. code-block:: text
    :caption: *myprofile*

    [settings]
    ...
    compiler=intel-cc
    compiler.mode=dpcpp
    compiler.version=2021.3
    compiler.libcxx=libstdc++
    build_type=Release
    [options]

    [build_requires]
    [env]
    CC=dpcpp
    CXX=dpcpp


As it's only available for new implementations of `CMakeToolChain`, `MSBuildToolchain` or `VCVars`, it'd be enough to use one of these generators.
For instance, if we have these conan

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMake
    from conan.tools.layout import cmake_layout


    class HelloConan(ConanFile):
        name = "hello"
        version = "1.0"

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        # Sources are located in the same place as this recipe, copy them to the recipe
        exports_sources = "CMakeLists.txt", "src/*"

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC

        def layout(self):
            cmake_layout(self)

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            cmake = CMake(self)
            cmake.install()

        def package_info(self):
            self.cpp_info.libs = ["hello"]

 Now, if you create the package running `conan create . -pr myprofile -pr:b myprofile`, you'll see something like this output:

.. code-block:: bash
    :caption: output

    hello/1.0: Generating the package
    hello/1.0: Package folder /home/franchuti/.conan/data/hello/1.0/_/_/package/7d9c7d5fa3c48c9705c2cb864656c00fa8672524
    hello/1.0: Calling package()
    hello/1.0: CMake command: cmake --build '/home/franchuti/.conan/data/hello/1.0/_/_/build/7d9c7d5fa3c48c9705c2cb864656c00fa8672524/cmake-build-release' '--target' 'install'

    :: initializing oneAPI environment ...
       dash: SH_VERSION = unknown
    :: advisor -- latest
    :: ccl -- latest
    :: clck -- latest
    :: compiler -- latest
    :: dal -- latest
    :: debugger -- latest
    :: dev-utilities -- latest
    :: dnnl -- latest
    :: dpcpp-ct -- latest
    :: dpl -- latest
    :: inspector -- latest
    :: intelpython -- latest
    :: ipp -- latest
    :: ippcp -- latest
    :: ipp -- latest
    :: itac -- latest
    :: mkl -- latest
    :: mpi -- latest
    :: tbb -- latest
    :: vpl -- latest
    :: vtune -- latest
    :: oneAPI environment initialized ::

    Using Conan toolchain through /home/franchuti/.conan/data/hello/1.0/_/_/build/7d9c7d5fa3c48c9705c2cb864656c00fa8672524/cmake-build-release/conan/conan_toolchain.cmake.
    -- Conan toolchain: Setting CMAKE_POSITION_INDEPENDENT_CODE=ON (options.fPIC)
    -- Conan toolchain: Setting BUILD_SHARED_LIBS= OFF
    -- The CXX compiler identification is Clang 13.0.0
    -- Check for working CXX compiler: /opt/intel/oneapi/compiler/2021.3.0/linux/bin/dpcpp
    Using Conan toolchain through .
    -- Check for working CXX compiler: /opt/intel/oneapi/compiler/2021.3.0/linux/bin/dpcpp -- works
    -- Detecting CXX compiler ABI info
    Using Conan toolchain through .
    -- Detecting CXX compiler ABI info - done
    -- Detecting CXX compile features
    -- Detecting CXX compile features - done
    -- Configuring done
    -- Generating done

As you can see, you have used one of these compilers, the DPC++ one. Conan is running the `setvars.sh|bat` automatically in order to enable all the needed environment variables.

Modes
++++++

As you know, Intel oneAPI has different toolkits, so you could have installed:

* Intel oneAPI Base Toolkit, so you'll be able to use the new DPC++/C++ compilers (icx/icpx or dpcpp).
* Intel oneAPI HPC Toolkit, then you could use the Intel C++ Classic Compiler (icc for Linux and icl for Windows)



conf
++++

- ``tools.intel:setvars_args`` is used to pass whatever we want as arguments to our `setvars.sh|bat` file. You can check out all the possible ones.

- ``tools.intel:installation_path`` argument to tells Conan the installation path, if it's not defined, Conan will try to find it out automatically.
