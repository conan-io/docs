.. _create_installer_packages:


Creating tool packages
======================

If you want to create conan packages for any tool it's easy, specially if you are familiar creating conan packages.
Let's see how the CMake recipe is done (https://www.conan.io/source/cmake_installer/0.1/lasote/testing):

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


- The config method is discarding some setting/options combination throwing an exception.
- The build method is downloading the right CMake file and unzipping it.
- The package method is copying all the files from the zip to the package folder.
- The package info is using the “self.env_info” to append to the environment variable “path” the package’s bin folder.

This package have only 2 different things than a regular conan library package:

- The source method is missing. That’s because when you compile a library, the source code is always the same for all the generated packages, but, in this case we are downloading the binaries, so we do it in the build method to download the different zip file for each settings/option combination. Instead of really building the tools, we are just downloading them. Of course if you want to build it from source, you can do it too, create your own package recipe
- The package_info method use the new “self.env_info” object. With “self.env_info” the package can declare environment variables that will be setted with the “virutalenv” generator.


The “self.env_info” variable can also be useful if a package tool depends on another tool.
Take a look to the MinGW conanfile.py recipe (https://www.conan.io/source/mingw_installer/0.1/lasote/testing):


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
           
           tools.download(files[keychain], "file.7z")
           env = ConfigureEnvironment(self)
           self.run("%s && 7z x file.7z" % env.command_line)
       
       def package(self):
           self.copy("*", dst="", src="mingw32")
           self.copy("*", dst="", src="mingw64")
   
       def package_info(self):
           self.env_info.path.append(os.path.join(self.package_folder, "bin"))
           self.env_info.CXX = os.path.join(self.package_folder, "bin", "g++.exe")
           self.env_info.CC = os.path.join(self.package_folder, "bin", "gcc.exe")


In the config method we are adding a require to another package, the 7z_installer that will use to unzip the mingw installers (with 7z compression).

In the build method we are downloading the right MinGW installer and using the helper 
``ConfigureEnvironment``. This helper will provide us a string with a command to set the environment variables. That means that the 7z executable will be in the path, because the 7z_installer dependency declares the “bin” folder in it’s “package_info” method.

In the package_info method we are declaring CC and CXX variables, used by CMake, autotools etc, to locate the compiler for C/C++ respectively. 
Also we are appending to “path” variable the bin folder, so we can invoke gcc, g++, make and other tools in the command line using the virtualenv generator when we execute the “activate” script.


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
   


Note that you can adjust the ``options`` and retrieve a different configuration of the required packages.


3. Install them:


.. code-block:: bash

   $ conan install --build


4. Activate the virtual environment in your shell:

.. code-block:: bash

   $ activate.bat
   $ (my_cpp_environ)


5. Check that the tools are in the path:


.. code-block:: bash

   $ gcc --version

   > gcc (x86_64-posix-seh-rev1, Built by MinGW-W64 project) 4.9.2

    Copyright (C) 2014 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

   $ cmake --version
   
   > cmake version 3.4.3

     CMake suite maintained and supported by Kitware (kitware.com/cmake).


6. You can deactivate the virtual environment with the "deactivate.bat" script

.. code-block:: bash

   $ deactivate.bat

