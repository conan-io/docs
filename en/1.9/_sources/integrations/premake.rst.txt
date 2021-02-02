.. _premake:

|premake_logo| Premake
======================

Since Conan 1.9.0 the ``premake`` generator is built-in and works with :command:`premake5`, so the following should be enough to use it:

.. code-block:: text

    [generators]
    premake

Example
-------

We are going to use the same example from :ref:`getting_started`, a MD5 Encrypter app.

This is the main file for it:

.. code-block:: cpp
   :caption: main.cpp

    #include "Poco/MD5Engine.h"
    #include "Poco/DigestStream.h"

    #include <iostream>


    int main(int argc, char** argv)
    {
        Poco::MD5Engine md5;
        Poco::DigestOutputStream ds(md5);
        ds << "abcdefghijklmnopqrstuvwxyz";
        ds.close();
        std::cout << Poco::DigestEngine::digestToHex(md5.digest()) << std::endl;
        return 0;
    }

As this project has relies on the Poco Libraries we are going to create a *conanfile.txt* with our requirement and declare there the
Premake generator too:

.. code-block:: text
   :caption: conanfile.txt

    [requires]
    Poco/1.9.0@pocoproject/stable

    [generators]
    premake

In order to use new generator within your project, use the following Premake script as a reference:

.. code-block:: lua
   :caption: premake5.lua

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
        defines { "DEBUG", conan_cppdefines }
        symbols "On"

        filter "configurations:Release"
        defines { "NDEBUG", conan_cppdefines }
        optimize "On"

Now we are going to let Conan retrieve the dependencies and generate the dependency information in a *conanbuildinfo.lua*:

.. code-block:: bash

    $ conan install .

Then let's call :command:`premake` to generate our project:

- Use this command for Windows Visual Studio:

  .. code-block:: bash

      $ premake5 vs2017  # Generates a .sln

- Use this command for Linux or macOS:

  .. code-block:: bash

      $ premake5 gmake  # Generates a makefile

Now you can build your project with Visual Studio or Make.


.. |premake_logo| image:: ../images/premake_logo.png

.. seealso::

    Check the complete reference of the :ref:`premake generator<premake_generator>`.
