.. _howto_intel_compiler:

Working with Intel compilers
============================

intel
------

.. note::

    This compiler is aimed to manage legacy Intel Parallel Studio XE compiler versions. For new Intel oneAPI, check the
    information about the ``intel-cc`` compiler below.

The ``Intel`` compiler is a particular case, as it uses ``Visual Studio`` compiler in Windows environments
and ``gcc`` in Linux environments. If you are wondering how to manage the compatibility between the packages generated
with ``intel`` and the generated with the pure base compiler (``gcc`` or ``Visual Studio``) check the
:ref:`Compatible Packages<compatible_packages>` and :ref:`Compatible Compilers<compatible_compilers>` sections.


intel-cc
---------

.. warning::

    The support for this compiler is **experimental** and subject to breaking changes.


Available since: `1.41.0 <https://github.com/conan-io/conan/releases>`_

This new compiler is defined to manage the different Intel oneAPI `DPC++/C++ <https://software.intel.com/content/www/us/en/develop/documentation/oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top.html>`_ and
`Classic <https://software.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top.html>`_ ones.

.. warning::

    macOS is not supported for the Intel oneAPI DPC++/C++ (icx/icpx or dpcpp) compilers. For macOS or Xcode support, you'll have to use the Intel C++ Classic Compiler.


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

    [tool_requires]
    [env]
    CC=dpcpp
    CXX=dpcpp

    [conf]
    tools.intel:installation_path=/opt/intel/oneapi


.. important::

    Remember to put this ``[conf]`` entry to find out the root path of your Intel oneAPI folder. Normally, it'll be installed by default in either ``/opt/intel/oneapi`` (Linux and macOS) or ``C:\Program Files (x86)\Intel\oneAPI`` (Windows).


We're specifying the ``CC`` and ``CXX`` compilers and the ``compiler.mode`` subsetting. The possible values for ``compiler.mode`` are:


* ``icx`` for Intel oneAPI C++ (icx/icpx compilers).
* ``dpcpp`` for Intel oneAPI DPC++ (dpcpp compiler and dpcpp-cl for Windows only).
* ``classic`` for Intel C++ Classic (icc for Linux and icl for Windows).


To set up the compiler **without Conan** you need to run an Intel official script to set all the proper variables to use those compilers called ``setvars.sh|bat`` script.

If you are using either the ``CMakeToolChain`` or the ``MSBuildToolchain``, when using the ``intel-cc`` compiler, Conan automatically calls the ``setvars`` script.
Otherwise, you can use the :ref:`IntelCC generator<conan_tools_intel>`.

This is an example of a Conan package called ``hello/1.0`` using the ``CMakeToolchain``. Remember you can use the command :command:`conan new hello/1.0 -m cmake_lib`
to create a simple project like this one:

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.cmake import CMakeToolchain

    class HelloConan(ConanFile):
        name = "hello"
        version = "1.0"

        # more code here...

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()


Running :command:`conan create . -pr intelprofile -pr:b intelprofile`, you'll see something like this output:

.. code-block:: bash
    :caption: output

    ......
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
    .......


As you can observe, you have used one of these Intel compilers, the DPC++ one and successfully generated the ``libhello.a`` file.


intel-cc and Microsoft Visual Studio
+++++++++++++++++++++++++++++++++++++

.. note::

    Ensure you have installed the Intel plugins for Microsoft Visual Studio before reading this section.


If you're working on a Microsoft Visual Studio project, you can add the Intel Toolset as a new *.props* file.
Let's suppose you have defined these files into your current project folder:

.. code-block:: text
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
    [tool_requires]
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


Running a :command:`conan install . -pr intelprofile`, a file *conantoolchain_release_x64.props* is generated in your current folder:


.. code-block:: xml
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


Note that a ``PlatformToolset`` is set to ``Intel C++ Compiler 19.2``. You can import that file to your project or solution of Visual Studio.
Read more about the :ref:`MSBuildToolchain here<conan_tools_microsoft>`.


.. note::

    See the complete :ref:`IntelCC reference<conan_tools_intel>` for more information about that tool.
