.. _premake:

premake
=======

|premake_logo| Premake
_________________________

Since conan 1.9.0, premake generator is built-in, so the following should be enough to use it:

.. code-block:: text

    [generators]
    premake

Example
-------

In order to use new generator within your project, use the following as a reference:

.. code-block:: lua

   -- premake5.lua

   require 'conanbuildinfo'

   workspace "ConanPremakeDemo"
     configurations { "Debug", "Release" }
     platforms { "Win32", "x64" }

     filter { "platforms:Win32" }
      system "Windows"
      architecture "x32"

     filter { "platforms:x64" }
      system "Windows"
      architecture "x64"

   project "ConanPremakeDemo"
     kind "ConsoleApp"
     language "C++"
     targetdir "bin/%{cfg.buildcfg}"

     includedirs { conan_includedirs }
     libdirs { conan_libdirs }
     links { conan_libs }
     linkoptions { conan_exelinkflags }

     files { "**.h", "**.cpp" }

     filter "configurations:Debug"
      defines { "DEBUG" }
      symbols "On"

     filter "configurations:Release"
      defines { "NDEBUG" }
      optimize "On"

Demo requires two remotes to run: ``bincrafters`` and ``conan-community``. Add them, if necessary:

.. code-block:: bash

    $ conan remote add conan-community https://api.bintray.com/conan/conan-community/conan
    $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan

Now let's get the premake project and build it:

.. code-block:: bash

    $ git clone https://github.com/SSE4/conan-premake-demo.git
    $ cd conan-premake-demo

then, on Windows run:

.. code-block:: bash

    $ ./run.cmd

on Linux or macOS, run:

.. code-block:: bash

    $ ./run.cmd

The following happens under the hood:

- conan installs ``OpenCV`` package
- conan installs ``premake_installer`` as build requirement
- conan generates ``conanbuildinfo.lua`` file which contains build information for premake
- conan generates ``activate.sh`` or ``activate.bat`` file with virtual environment which has ``premake5`` executable
- virtual environment is getting activated
- ``premake5`` invoked to generate native project files
- either ``make`` or ``msbuild`` used to build native project files

.. tip::

    This complete examples is stored in https://github.com/SSE4/conan-premake-demo

.. |premake_logo| image:: ../images/premake_logo.png

.. seealso::

    Check the complete reference of the :ref:`premake generator<premake_generator>`.
