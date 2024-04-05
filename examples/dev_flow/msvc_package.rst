Packaging Visual Studio as a Conan package
==========================================

It is possible to package the Visual Studio tools into a Conan package and use it later as a ``tool_requires``.
This can be convenient in some scenarios, for example in CI, or in some developer setups.

In this example we are going to start with a standard Visual Studio 16 2019 installation on disk. The first
thing we'll do is to rename the folder ``C:/Program Files (x86)/Microsoft Visual Studio/2019`` to
``C:/Program Files (x86)/Microsoft Visual Studio/2019_2``. This is not strictly necessary, but in this way
we make sure that CMake or vswhere are not able to locate it, and we can validate better that the consumer
project is using VS from the Conan package and not from the system.

This is the recipe to package VS 2019:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.files import copy, save
    import os

    class x86_64_windows_msvc2017Conan(ConanFile):
        name = "msvc"
        version = "16"
        settings = "os", "arch"

        def package(self):
            # toolchain
            version_vs = "16.11.34601.136"  # This must be tuned, might be automatically obtained too
            toolchain = f'set(CMAKE_GENERATOR_INSTANCE "$ENV{{CONAN_MSVC_16_FOLDER}},version={version_vs}" CACHE INTERNAL "")'
            save(self, os.path.join(self.package_folder, "msvc_toolchain.cmake"), toolchain)
            # packaging
            vs_path = "C:/Program Files (x86)/Microsoft Visual Studio/2019_2/Community"
            copy(self, "*", src=vs_path, dst=self.package_folder)

        def package_info(self):
            f = os.path.join(self.package_folder, "msvc_toolchain.cmake")
            self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", f)
            pf = self.package_folder.replace("\\", "/")
            self.buildenv_info.define("CONAN_MSVC_16_FOLDER", pf)


Note a few important things:

- The ``package()`` method is creating a ``msvc_toolchain.cmake`` that defines the ``CMAKE_GENERATOR_INSTANCE``.
- The ``CMAKE_GENERATOR_INSTANCE`` should point to the location of VS, which is inside the Conan package. But this location
  will change from machine to machine, so it needs to be generalized.
- The ``version_vs = "16.11.34601.136"`` needs to match your installation. It can be obtained with ``vswhere``. It is possible
  to automate that in the recipe, but it is hardcoded for simplicity, like the ``vs_path``.
- A ``CONAN_MSVC_16_FOLDER`` environment variable, which value is defined in the ``package_info()`` method is used to 
  generalize the package folder location.
- The generated ``msvc_toolchain.cmake`` is passed to consumers with the ``tools.cmake.cmaketoolchain:user_toolchain`` configuration


We can use ``conan create .`` to create the Conan package containing a copy of the VS 2019 installation.

Then, we can define a profile like (assuming the ``default`` profile is a Windows-MSVC one):

.. code-block::
    :caption: msvc16_profile

    include(default)

    [settings]
    # Note that we need to align the settings with the tool-require
    compiler.version=192

    [tool_requires]
    msvc/16

And we can now use it to build a CMake package:

.. code-block:: bash

    $ conan new cmake_lib -d name=mypkg -d version=0.1
    $ conan create . -pr=msvc16_profile
    ...
    -- Check for working CXX compiler: C:/Users/mysuser/.conan2/p/b/msvcfa3a5055acf54/p/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64/cl.exe - skipped
    ...
    mypkg/0.1 (test package): RUN: Release\example
    mypkg/0.1: _MSC_VER1929

And it will use the compiler from within the ``msvc/16`` Conan package.



.. note::

    - This example is far from optimal. The whole IDE installation is packaged, which is very large. Most likely
      it is not necessary to package everything and packaging just a subset (MSBuild, compiler and tools) would be
      enough, be faster to package and use less space.
    - Please make sure to comply with the VS licenses while using their tools.
    - This example works only for CMake consumers. For other build systems, it might be necessary to improve the
      ``msvc`` recipe.
