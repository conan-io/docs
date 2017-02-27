.. _create_installer_packages:


Creating conan packages to install dev tools
============================================


If you want to create conan packages for your development tools, it is easy, specially if you are already familiar with creating conan packages.
Let's see the conan recipe to install different versions of cmake in different platforms (https://www.conan.io/source/cmake_installer/0.1/lasote/testing):

.. code-block:: python

   from conans import ConanFile
   import os
   
   
   class CMakeInstallerConan(ConanFile):
       name = "cmake_installer"
       version = "0.1"
       license = "MIT"
       url = "http://github.com/lasote/conan-cmake-installer"
       settings = {"os": ["Windows", "Linux", "Macos"], "arch": ["x86", "x86_64"]}
       options = {"version": ["3.6.0", "3.5.2", "3.4.3", "3.3.2", 
                              "3.2.3", "3.1.3", "3.0.2", "2.8.12"]}
       default_options = "version=3.6.0"
       
       def config(self):
           if self.settings.os == "Macos" and self.settings.arch == "x86":
               raise Exception("Not supported x86 for OSx")
           if self.settings.os == "Linux" and self.options.version == "2.8.12" and self.settings.arch == "x86_64":
               raise Exception("Not supported 2.8.12 for x86_64 binaries")
   
       def get_filename(self):
           os = {"Macos": "Darwin", "Windows": "win32"}.get(str(self.settings.os), str(self.settings.os))
           arch = {"x86": "i386"}.get(str(self.settings.arch), 
                                      str(self.settings.arch)) if self.settings.os != "Windows" else "x86"
           return "cmake-%s-%s-%s" % (self.options.version, os, arch)
       
       def build(self):
           keychain = "%s_%s_%s" % (self.settings.os,
                                    self.settings.arch,
                                    str(self.options.version))
           minor = str(self.options.version)[0:3]
           ext = "tar.gz" if not self.settings.os == "Windows" else "zip"
           url = "https://cmake.org/files/v%s/%s.%s" % (minor, self.get_filename(), ext)
   
           dest_file = "file.tgz" if self.settings.os != "Windows" else "file.zip"
           self.output.warn("Downloading: %s" % url)
           tools.download(url, dest_file)
           tools.unzip(dest_file)
       
       def package(self):
           self.copy("*", dst="", src=self.get_filename())
   
       def package_info(self):
           self.env_info.path.append(os.path.join(self.package_folder, "bin"))


- The config method discards some combinations of settings and options, by throwing an exception.
- The build method downloads the appropriate CMake file and unzips it.
- The package method is copying all the files from the zip to the package folder.
- The package info is using the “self.env_info” to append to the environment variable “path” the package’s bin folder.

This package has only 2 differences from a regular conan library package:

- The source method is missing. That’s because when you compile a library, the source code is always the same for all the generated packages, but in this case we are downloading the binaries,
  so we do it in the build method to download the appropriate zip file according to each combination of settings/options.  Instead of actually building the tools, we just download them.
  Of course, if you want to build it from source, you can do it too, by creating your own package recipe.
- The package_info method uses the new “self.env_info” object.  With “self.env_info” the package can declare environment variables that will be set automatically before the `build`,
  `package`, `source` and `imports` methods of the conanfile requiring this package. This is a convenient method to use these tools without having to mess with the system PATH.


The “self.env_info” variable can also be useful if a package tool depends on another tool.
For example, take a look at the MinGW conanfile.py recipe (https://www.conan.io/source/mingw_installer/0.1/lasote/testing):


.. code-block:: python

   class MingwinstallerConan(ConanFile):
       name = "mingw_installer"
       version = "0.1"
       license = "MIT"
       url = "http://github.com/lasote/conan-mingw-installer"
       settings = {"os": ["Windows"]}
       options = {"threads": ["posix", "win32"],
                  "exception": ["dwarf2", "sjlj", "seh"], 
                  "arch": ["x86", "x86_64"],
                  "version": ["4.8", "4.9"]}
       default_options = "exception=sjlj", "threads=posix", "arch=x86_64", "version=4.9"
   
       def config(self):
           self.requires.add("7z_installer/0.1@lasote/testing", private=True)
           …
      
       def build(self):
           ...
           # The 7z package path is automatically inherited
           tools.download(files[keychain], "file.7z")
           self.run("7z x file.7z")
       
       def package(self):
           self.copy("*", dst="", src="mingw32")
           self.copy("*", dst="", src="mingw64")
   
       def package_info(self):
           self.env_info.path.append(os.path.join(self.package_folder, "bin"))
           self.env_info.CXX = os.path.join(self.package_folder, "bin", "g++.exe")
           self.env_info.CC = os.path.join(self.package_folder, "bin", "gcc.exe")


In the config method we add a require to another package, the 7z_installer, which will be used to unzip the mingw installers (with 7z compression).

In the build method we download the appropriate MinGW installer. The 7z executable will be in the PATH, because the 7z_installer dependency declares the “bin” folder in its “package_info” method.

In the package_info method we declare the CC and CXX variables, used by CMake, autotools etc, to locate the compiler for C and C++ respectively. 
We also append the bin folder to the “path” variable, so that we can invoke gcc, g++, make and other tools in the command line using the virtualenv generator when we execute the “activate” script.


Using the tool packages
.......................


Let's see an example. If you are working in Windows, with MinGW and CMake.

1. Create a separate folder from your project, this folder will handle our global development environment. 


.. code-block:: bash

   mkdir my_cpp_environ
   cd my_cpp_environ

2. Create a 'conanfile.txt' file:


.. code-block:: bash

   [requires]
   mingw_installer/0.1@lasote/testing
   cmake_installer/0.1@lasote/testing
   
   [generators]
   virtualenv
   
   [options]
   mingw_installer:exception=seh
   mingw_installer:version=4.9
   cmake_installer:version=3.4.3
   


Note that you can adjust the ``options`` and retrieve a different configuration of the required packages,
or leave them unspecified in the file and pass them as command line parameters.


3. Install them:


.. code-block:: bash

   $ conan install


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
   
   > cmake version 3.4.3

     CMake suite maintained and supported by Kitware (kitware.com/cmake).


6. You can deactivate the virtual environment with the "deactivate.bat" script

.. code-block:: bash

   (my_cpp_environ)$ deactivate
   $
