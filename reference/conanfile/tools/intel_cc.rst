.. _conan_tools_intel_cc:


IntelCC
=========

.. warning::
    These tools are **experimental** and subject to breaking changes.


Available since: `1.41.0 <https://github.com/conan-io/conan/releases>`_


This section explains how to use the new Intel oneAPI `DPC++/C++ <https://software.intel.com/content/www/us/en/develop/documentation/oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top.html>`_ and
`Classic <https://software.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top.html>`_ compilers in Conan.

.. note::
    This new compiler is developed as a new component in ``conan.tools.intel`` and it will be automatically applied through ``CMakeToolChain`` or ``MSBuildToolchain`` generators.

.. warning::
    macOS* is not supported for the Intel oneAPI DPC++/C++ (icx/icpx or dpcpp) compilers. For macOS or Xcode* support, you'll have to use the Intel C++ Classic Compiler.


General use case
-----------------

It can be declared into your local profile like any other compiler as follows:


.. code-block:: text
    :caption: intelprofile

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

    [conf]
    tools.intel:installation_path=/opt/intel/oneapi


.. important::

    Remember to put this ``[conf]`` entry to find out the root path of your Intel oneAPI folder. Normally, it'll be installed by default:
    *   Linux, Darwin: ``/opt/intel/oneapi``
    *   Windows: ``C:\Program Files (x86)\Intel\oneAPI``


Whenever you choice the ``intel-cc`` compiler, it'll be automatically applied using ``CMakeToolChain`` or ``MSBuildToolchain`` generators.
For instance, if we are creating a package ``intelcc/1.0`` using one of those generators (remember you can use the command ``conan new intelcc/1.0 -m cmake_lib`` to create a simple project):

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.cmake import CMakeToolchain

    class HelloConan(ConanFile):
        name = "intelcc"
        version = "1.0"

        # ..

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()


Now, running ``conan create . -pr intelprofile -pr:b intelprofile``, you'll see something like this output:

.. code-block:: bash
    :caption: output

    ......
    intelcc/1.0: Generating the package
    intelcc/1.0: Package folder /home/franchuti/.conan/data/intelcc/1.0/_/_/package/7d9c7d5fa3c48c9705c2cb864656c00fa8672524
    intelcc/1.0: Calling package()
    intelcc/1.0: CMake command: cmake --build '/home/franchuti/.conan/data/intelcc/1.0/_/_/build/7d9c7d5fa3c48c9705c2cb864656c00fa8672524/cmake-build-release' '--target' 'install'
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
    Using Conan toolchain through /home/franchuti/.conan/data/intelcc/1.0/_/_/build/7d9c7d5fa3c48c9705c2cb864656c00fa8672524/cmake-build-release/conan/conan_toolchain.cmake.
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


As you can see, you have used one of these compilers, the DPC++ one and successfully generated the `libintelcc.a` file.

.. note::

    Conan is running the ``setvars.sh|bat`` automatically in order to enable all the needed environment variables to build the library.


Intel oneAPI Toolset and Microsoft Visual Studio
-------------------------------------------------

.. note::

    Ensure you have installed the Intel plugins for Microsoft Visual Studio before reading this section.


If you're working in a Microsoft Visual Studio project, you can add the Intel Toolset as a new *.props* file easily.
Let's suppose you have defined these files into your current project folder:

.. code-block:: python
    :caption: intelprofile

    [settings]
    os=Windows
    os_build=Windows
    arch=x86_64
    arch_build=x86_64
    compiler=intel-cc
    compiler.mode=classic
    compiler.version=2021.3
    compiler.runtime=dynamic
    build_type=Release
    [options]
    [build_requires]
    [env]
    [conf]
    tools.intel:installation_path="C:\Program Files (x86)\Intel\oneAPI"


.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.microsoft import MSBuildToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = MSBuildToolchain(self)
            tc.generate()

Running a ``conan install . -pr intelprofile`` you'll see a new *conantoolchain_release_x64.props* file generated in your current folder as the showed bellow:

.. code-block:: python
    :caption: conantoolchain_release_x64.props

    <?xml version="1.0" encoding="utf-8"?>
    <Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
      <ItemDefinitionGroup>
        <ClCompile>
          <PreprocessorDefinitions>
             ;%(PreprocessorDefinitions)
          </PreprocessorDefinitions>
          <RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>
          <LanguageStandard></LanguageStandard>
        </ClCompile>
      </ItemDefinitionGroup>
      <PropertyGroup Label="Configuration">
        <PlatformToolset>Intel C++ Compiler 19.2</PlatformToolset>
      </PropertyGroup>
    </Project>

Then, you'll be able to load this new properties into your current Microsoft Visual Studio project.


Custom definition
-----------------

Perhaps you want to define/override something else in your own, so you can invoke the environment variables generation from your conanfile.py as follows:

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.intel import IntelCC

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            intelcc = IntelCC(self)
            intelcc.generate()


References
-----------

These are some important points to take into account for this new compiler.

Modes
++++++

Intel oneAPI has different toolkits available, so you could have installed (among other ones):

* Intel oneAPI Base Toolkit, so you'll be able to use the new C++/DPC++ compilers (icx/icpx or dpcpp).
* Intel oneAPI HPC Toolkit, then you could use the Intel C++ Classic Compiler (icc for Linux and icl for Windows)

This is the main reason to declare the `mode` that you're using in your project and create different packages IDs between them.

.. note::

    Check all the settings available in the :ref:`settings.yml section<settings_yml>`.


conf
++++

- ``tools.intel:installation_path``: **(required)** argument to tells Conan the installation path, if it's not defined, Conan will try to find it out automatically.

- ``tools.intel:setvars_args``: **(optional)** it is used to pass whatever we want as arguments to our `setvars.sh|bat` file. You can check out all the possible ones from the Intel official documentation.
