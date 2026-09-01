.. _create_installer_packages:

Creating conan packages to install dev tools
============================================

Conan 1.0 introduced two new settings, ``os_build`` and ``arch_build``. These settings represent the machine where Conan is running, and are
important settings when we are packaging tools.

These settings are different from ``os`` and ``arch``. These mean where the built software by the Conan recipe will run. When we are
packaging a tool, it usually makes no sense, because we are not building any software, but it makes sense if you are
:ref:`cross building software<cross_building>`.

We recommend the use of ``os_build`` and ``arch_build`` settings instead of ``os`` and ``arch`` if you are packaging a tool involved in the
building process, like a compiler, a build system etc. If you are building a package to be run on the **host** system you can use ``os`` and
``arch``.

A Conan package for a tool follows always a similar structure, this is a recipe for packaging the ``nasm`` tool for building assembler:

.. code-block:: python

   import os
   from conans import ConanFile
   from conans.client import tools


   class NasmConan(ConanFile):
       name = "nasm"
       version = "2.13.01"
       license = "BSD-2-Clause"
       url = "https://github.com/lasote/conan-nasm-installer"
       settings = "os_build", "arch_build"
       build_policy = "missing"
       description="Nasm for windows. Useful as a build_require."

       def configure(self):
           if self.settings.os_build != "Windows":
               raise Exception("Only windows supported for nasm")

       @property
       def nasm_folder_name(self):
           return "nasm-%s" % self.version

       def build(self):
           suffix = "win32" if self.settings.arch_build == "x86" else "win64"
           nasm_zip_name = "%s-%s.zip" % (self.nasm_folder_name, suffix)
           tools.download("http://www.nasm.us/pub/nasm/releasebuilds/"
                          "%s/%s/%s" % (self.version, suffix, nasm_zip_name), nasm_zip_name)
           self.output.warn("Downloading nasm: "
                            "http://www.nasm.us/pub/nasm/releasebuilds"
                            "/%s/%s/%s" % (self.version, suffix, nasm_zip_name))
           tools.unzip(nasm_zip_name)
           os.unlink(nasm_zip_name)

       def package(self):
           self.copy("*", dst="", keep_path=True)
           self.copy("license*", dst="", src=self.nasm_folder_name, keep_path=False, ignore_case=True)

       def package_info(self):
           self.output.info("Using %s version" % self.nasm_folder_name)
           self.env_info.path.append(os.path.join(self.package_folder, self.nasm_folder_name))

There are some remarkable things in the recipe:

- The configure method discards some combinations of settings and options, by throwing an exception. In this case this package is only for
  Windows.
- ``build()`` downloads the appropriate file and unzips it.
- ``package()`` copies all the files from the zip to the package folder.
- ``package_info()`` uses ``self.env_info`` to append to the environment variable ``path`` the package's bin folder.

This package has only 2 differences from a regular Conan library package:

- ``source()`` method is missing. That’s because when you compile a library, the source code is always the same for all the generated
  packages, but in this case we are downloading the binaries, so we do it in the build method to download the appropriate zip file according
  to each combination of settings/options. Instead of actually building the tools, we just download them. Of course, if you want to build it
  from source, you can do it too by creating your own package recipe.
- The ``package_info()`` method uses the new ``self.env_info`` object. With ``self.env_info`` the package can declare environment variables
  that will be set automatically before `build()`, `package()`, `source()` and `imports()` methods of a package requiring this build tool.
  This is a convenient method to use these tools without having to mess with the system path.

Using the tool packages in other recipes
----------------------------------------

The ``self.env_info`` variables will be automatically applied when you require a recipe that declares them. For example, take a look at the
MinGW *conanfile.py* recipe (https://github.com/conan-community/conan-mingw-installer):

.. code-block:: python
   :emphasize-lines: 5, 17

    class MingwInstallerConan(ConanFile):
        name = "mingw_installer"
        ...

        build_requires = "7z_installer/1.0@conan/stable"

        def build(self):
            keychain = "%s_%s_%s_%s" % (str(self.settings.compiler.version).replace(".", ""),
                                        self.settings.arch_build,
                                        self.settings.compiler.exception,
                                        self.settings.compiler.threads)

            files = {
               ...        }

            tools.download(files[keychain], "file.7z")
            self.run("7z x file.7z")

        ...

We are requiring a ``build_require`` to another package: ``7z_installer``. In this case it will be used to unzip the 7z compressed files
after downloading the appropriate MinGW installer.

That way, after the download of the installer, the 7z executable will be in the PATH, because the ``7z_installer`` dependency declares the
*bin* folder in its ``package_info()``.

.. important::

    Some build requires will need settings such as ``os``, ``compiler`` or ``arch`` to build themselves from sources. In that case the
    recipe might look like this:

    .. code-block:: python

        class MyAwesomeBuildTool(ConanFile):
            settings = "os_build", "arch_build", "arch", "compiler"
            ...

            def build(self):
                cmake = CMake(self)
                ...

            def package_id(self):
                self.info.include_build_settings()
                del self.info.settings.compiler
                del self.info.settings.arch

    Note ``package_id()`` deletes not needed information for the computation of the package ID and includes the build settings ``os_build``
    and ``arch_build`` that are excluded by default. Read more about
    :ref:`self.info.include_build_settings() <info_discard_include_build_settings>` in the reference section.

Using the tool packages in your system
--------------------------------------

You can use the :ref:`virtualenv generator <virtualenv_generator>` to get the requirements applied in your system. For example: Working in
Windows with MinGW and CMake.

1. Create a separate folder from your project, this folder will handle our global development environment.

.. code-block:: bash

    $ mkdir my_cpp_environ
    $ cd my_cpp_environ

2. Create a *conanfile.txt* file:

.. code-block:: bash

    [requires]
    mingw_installer/1.0@conan/stable
    cmake_installer/3.10.0@conan/stable

    [generators]
    virtualenv

Note that you can adjust the ``options`` and retrieve a different configuration of the required packages, or leave them unspecified in the
file and pass them as command line parameters.

3. Install them:

.. code-block:: bash

    $ conan install .

4. Activate the virtual environment in your shell:

.. code-block:: bash

   $ activate
   (my_cpp_environ)$ 

5. Check that the tools are in the path:

.. code-block:: bash

    (my_cpp_environ)$ gcc --version

    > gcc (x86_64-posix-seh-rev1, Built by MinGW-W64 project) 4.9.2

     Copyright (C) 2014 Free Software Foundation, Inc.
     This is free software; see the source for copying conditions.  There is NO
     warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    (my_cpp_environ)$ cmake --version

    > cmake version 3.10

      CMake suite maintained and supported by Kitware (kitware.com/cmake).

6. You can deactivate the virtual environment with the *deactivate.bat* script

.. code-block:: bash

    (my_cpp_environ)$ deactivate
