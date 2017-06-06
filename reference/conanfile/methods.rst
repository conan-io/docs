Methods
=======


.. _retrieve_source:

source()
--------

The other way is to let conan retrieve the source code from any other external origin, github, or
just a regular download. This can be done in the ``source()`` method.

For example, in the previous section, we "exported" the source code files, together with the **conanfile.py** file,
which can be handy if the source code is not under version control. But if the source code is available in a repository,
you can directly get it from there:

.. code-block:: python

   from conans import ConanFile

   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       settings = "os", "compiler", "build_type", "arch"

       def source(self):
           self.run("git clone https://github.com/memsharded/hello.git")
           # You can also change branch, commit or whatever
           # self.run("cd hello && git checkout 2fe5...")


This will work, as long as ``git`` is in your current path (so in Win you probably want to run things in msysgit, cmder, etc).
You can also use another VCS or direct download/unzip. For that purpose, we have provided some helpers,
but you can use your own code or origin as well. This is a snippet of the conanfile of the POCO libray:


..  code-block:: python

   from conans import ConanFile
   from conans.tools import download, unzip, check_md5, check_sha1, check_sha256
   import os
   import shutil

   class PocoConan(ConanFile):
       name = "Poco"
       version = "1.6.0"

       def source(self):
           zip_name = "poco-1.6.0-release.zip"
           download("https://github.com/pocoproject/poco/archive/poco-1.6.0-release.zip", zip_name)
           # check_md5(zip_name, "51e11f2c02a36689d6ed655b6fff9ec9")
           # check_sha1(zip_name, "8d87812ce591ced8ce3a022beec1df1c8b2fac87")
           # check_sha256(zip_name, "653f983c30974d292de58444626884bee84a2731989ff5a336b93a0fef168d79")
           unzip(zip_name)
           shutil.move("poco-poco-1.6.0-release", "poco")
           os.unlink(zip_name)

The download, unzip utilities can be imported from conan, but you can also use your own code here
to retrieve source code from any origin. You can even create packages for pre-compiled libraries
you already have, even if you don't have the source code. You can download the binaries, skip
the ``build()`` method and define your ``package()`` and ``package_info()`` accordingly.

You can also use **check_md5**, **check_sha1** and **check_sha256** from the **tools** module to verify that a package is downloaded correctly.

build()
--------

Build helpers
+++++++++++++

You can use these classes to prepare your build system's command invocation:

- **CMake**: Prepares the invocation of cmake command with your settings.
- **AutoToolsBuildEnvironment**: If you are using configure/Makefile to build your project you can use this helper.
  Read more: :ref:`Building with Autotools <building_with_autotools>`.
- **VisualStudioBuildEnvironment**: If you are calling your Visual Studio compiler directly to build your project you can use this helper.
  Read more: :ref:`Building with Visual Studio <building_with_visual_studio>`.
- **tools.build_sln_command()**: If you have an ``sln`` project you can use this tool to build it.
  Read more: :ref:`Build an existing Visual Studio project <building_visual_project>`.
- **GCC generator**: If you are calling GCC or Clang directly to build your project you can use the ``gcc`` generator.
  Read more: :ref:`Building with GCC or Clang <building_with_gcc_clang>`.



(Unit) Testing your library
++++++++++++++++++++++++++++
We have seen how to run package tests with conan, but what if we want to run full unit tests on
our library before packaging, so that they are run for every build configuration?
Nothing special is required here. We can just launch the tests from the last command in our
``build()`` method:

.. code-block:: python

   def build(self):
      cmake = CMake(self)
      self.run("cmake . %s %s" % (cmake.command_line))
      self.run("cmake --build . %s" % cmake.build_config)
      # here you can run CTest, launch your binaries, etc
      self.run("ctest")


package()
---------
The actual creation of the package, once that it is build, is done in the ``package()`` method.
Using the ``self.copy()`` method, artifacts are copied from the build folder to the package folder.
The syntax of copy is as follows:

.. code-block:: python

   self.copy(pattern, dst, src, keep_path=False, symlinks=None, excludes=None)


- ``pattern`` is a pattern following fnmatch syntax of the files you want to copy, from the *build* to the *package* folders. Typically something like ``*.lib`` or ``*.h``
- ``dst`` is the destination folder in the package. They will typically be ``include`` for headers, ``lib`` for libraries and so on, though you can use any convention you like
- ``src`` is the folder where you want to search the files in the *build* folder. If you know that your libraries when you build your package will be in *build/lib*, you will typically use ``build/lib`` in this parameter. Leaving it empty means the root build folder.
- ``keep_path``, with default value=True, means if you want to keep the relative path when you copy the files from the source(build) to the destination(package). Typically headers, you keep the relative path, so if the header is in *build/include/mylib/path/header.h*, you write:
- ``symlinks``, with default value=None, set it to True to activate symlinks copying, like typical lib.so->lib.so.9
- ``excludes``, is a single pattern or a tuple of patterns to be excluded from the copy. If a file matches both the include and the exclude pattern, it will be excluded.


.. code-block:: python

   self.copy("*.h", "include", "build/include") #keep_path default is True

so the final path in the package will be: ``include/mylib/path/header.h``, and as the *include* is usually added to the path, the includes will be in the form: ``#include "mylib/path/header.h"`` which is something desired

``keep_path=False`` is something typically desired for libraries, both static and dynamic. Some compilers as MSVC, put them in paths as *Debug/x64/MyLib/Mylib.lib*. Using this option, we could write:

.. code-block:: python

   self.copy("*.lib", "lib", "", keep_path=False)


And it will copy the lib to the package folder *lib/Mylib.lib*, which can be linked easily

.. note::

    If you are using CMake and you have an install target defined in your CMakeLists.txt, you
    might be able to reuse it for this ``package()`` method. Please check :ref:`reuse_cmake_install`


.. _package_info:

package_info()
---------------

cpp_info
+++++++++
Each package has to specify certain build information for its consumers. This can be done in
the ``cpp_info`` attribute within the ``package_info()`` method.

The ``cpp_info`` attribute has the following properties you can assign/append to:

.. code-block:: python

   self.cpp_info.includedirs = ['include']  # Ordered list of include paths
   self.cpp_info.libs = []  # The libs to link against
   self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
   self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc can be found
   self.cpp_info.bindirs = []  # Directories where executables and shared libs can be found
   self.cpp_info.defines = []  # preprocessor definitions
   self.cpp_info.cflags = []  # pure C flags
   self.cpp_info.cppflags = []  # C++ compilation flags
   self.cpp_info.sharedlinkflags = []  # linker flags
   self.cpp_info.exelinkflags = []  # linker flags


* includedirs: list of relative paths (starting from the package root) of directories where headers
  can be found. By default it is initialized to ['include'], and it is rarely changed.
* libs: ordered list of libs the client should link against. Empty by default, it is common
  that different configurations produce different library names. For example:

.. code-block:: python

   def package_info(self):
        if not self.settings.os == "Windows":
            self.cpp_info.libs = ["libzmq-static.a"] if self.options.static else ["libzmq.so"]
        else:
            ...

* libdirs: list of relative paths (starting from the package root) of directories in which to find
  library object binaries (.lib, .a, .so. dylib). By default it is initialize to ['lib'], and it is rarely changed.
* resdirs: list of relative paths (starting from the package root) of directories in which to find
  resource files (images, xml, etc). By default it is initialize to ['res'], and it is rarely changed.
* bindirs: list of relative paths (starting from the package root) of directories in which to find
  library runtime binaries (like windows .dlls). By default it is initialized to ['bin'], and it is rarely changed.
* defines: ordered list of preprocessor directives. It is common that the consumers have to specify
  some sort of defines in some cases, so that including the library headers matches the binaries:
* <c,cpp,exelink,sharedlink>flags, list of flags that the consumer should activate for proper
  behavior. Usage of C++11 could be configured here, for example, although it is true that the consumer may
  want to do some flag processing to check if different dependencies are setting incompatible flags
  (c++11 after c++14)

.. code-block:: python

   if self.options.static:
      if self.settings.compiler == "Visual Studio":
          self.cpp_info.libs.append("ws2_32")
      self.cpp_info.defines = ["ZMQ_STATIC"]

      if not self.settings.os == "Windows":
          self.cpp_info.cppflags = ["-pthread"]


.. _environment_information:

env_info
+++++++++

Each package can also define some environment variables that the package needs to be reused.
It's specially useful for :ref:`installer packages<create_installer_packages>`, to set the path with the "bin" folder of the packaged application.
This can be done in the ``env_info`` attribute within the ``package_info()`` method.

.. code-block:: python

  self.env_info.path.append("ANOTHER VALUE") # Append "ANOTHER VALUE" to the path variable
  self.env_info.othervar = "OTHER VALUE" # Assign "OTHER VALUE" to the othervar variable
  self.env_info.thirdvar.append("some value") # Every variable can be set or appended a new value


The :ref:`virtualenv<virtual_environment_generator>` generator will use the self.env_info variables to prepare a script to activate/deactive a virtual environment.

In previous conan versions you needed to use `ConfigureEnvironment` helper (now deprecated) to reuse these variables, but it's not needed anymore.
They will be automatically applied before calling the consumer conanfile.py methods `source`, `build`, `package` and `imports`.


.. _configure_config_options:

configure(), config_options()
-----------------------------

Note: ``config()`` method has been deprecated, used ``configure()`` instead.

If the package options and settings are related, and you want to configure either, you can do so
in the ``configure()`` and ``config_options()`` methods. This is an example:

..  code-block:: python

   class MyLibConan(ConanFile):
       name = "MyLib"
       version = "2.5"
       settings = "os", "compiler", "build_type", "arch"
       options = {"static": [True, False],
                   "header_only": [True False]}

       def config(self):
           # If header only, the compiler, etc, does not affect the package!
           if self.options.header_only:
               self.settings.clear()
               self.options.remove("static")

The package has 2 options set, to be compiled as a static (as opposed to shared) library,
and also not to involve any builds, because header-only libraries will be used. In this case,
the settings that would affect a normal build, and even the other option (static vs shared)
do not make sense, so we just clear them. That means, if someone consumes MyLib with the
``header_only: True`` option, the package downloaded and used will be the same, irrespective of
the OS, compiler or architecture the consumer is building with.

The most typical usage would be the one with ``configure()`` while ``config_options()`` should be
used more sparingly. ``config_options()`` is used to configure or constraint the available
options in a package, **before** they are given a value. So when a value is tried to be assigned,
it will raise an error. For example, let's suppose that a certain package library cannot be
built as shared library in Windows, it can be done:

..  code-block:: python

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

This will be executed before the actual assignment of ``options`` (then, such ``options`` values
cannot be used inside this function), so the command ``$ conan install -o Pkg:shared=True`` will
raise an Exception in Windows saying that ``shared`` is not an option for such package.


requirements()
--------------

Besides the ``requires`` field, more advanced requirement logic can be defined in the
``requirements()`` optional method, using for example values from the package ``settings`` or
``options``:


..  code-block:: python

   def requirements(self):
        if self.options.myoption:
            self.requires("zlib/1.2@drl/testing")
        else:
            self.requires("opencv/2.2@drl/stable")

This is a powerful mechanism for handling **conditional dependencies**.

When you are inside the method, each call to ``self.requires()`` will add the corresponding
requirement to the current list of requirements. It also has optional parameters that allow
defining the special cases, as is shown below:

..  code-block:: python

   def requirements(self):
        self.requires("zlib/1.2@drl/testing", private=True, override=False, dev=False)


``self.requires`` method parameters:

- **override**: Default False. True means that this is not an actual requirement, but something to
  be passed upstream and override possible existing values.
- **private**: Default False. True means that this requirement will be somewhat embedded (like
  a static lib linked into a shared lib), so it is not required to link.
- **dev**: Default False. True means that this requirement is only needed at dev time, e.g. only
  needed for building or testing, but not affects the package hash at all.

build_requirements()
-----------------------

Build requirements are requirements that are only installed and used when the package is built from sources. If there is an existing pre-compiled binary, then the build requirements for this package will not be retrieved.

This method is useful for defining conditional build requirements, for example:

.. code-block:: python

    class MyPkg(ConanFile):

        def build_requirements(self):
            if self.settings.os == "Windows":
                self.build_requires("ToolWin/0.1@user/stable")

Read more: :ref:`Build requiremens <build_requires>`


.. _system_requirements:

system_requirements()
----------------------
It is possible to install system-wide packages from conan. Just add a ``system_requirements()``
method to your conanfile and specify what you need there.

You can use ``conans.tools.os_info`` object to detect the operating system, version and distribution (linux):

- ``os_info.is_linux`` True if Linux
- ``os_info.is_windows`` True if Windows
- ``os_info.is_macos`` True if OSx
- ``os_info.os_version`` OS version
- ``os_info.os_version_name`` Common name of the OS (Windows 7, Mountain Lion, Wheezy...)
- ``os_info.linux_distro`` Linux distribution name (None if not Linux)

Also you can use ``SystemPackageTool`` class, that will automatically invoke the right system package tool: **apt**, **yum** or **brew** depending on the system we are running.

..  code-block:: python

    from conans.tools import os_info, SystemPackageTool

    def system_requirements(self):
        pack_name = None
        if os_info.linux_distro == "ubuntu":
            if os_info.os_version > "12":
                pack_name = "package_name_in_ubuntu_10"
            else:
                pack_name = "package_name_in_ubuntu_12"
        elif os_info.linux_distro == "fedora" or os_info.linux_distro == "centos":
            pack_name = "package_name_in_fedora_and_centos"
        elif os_info.is_macos:
            pack_name = "package_name_in_macos"

        if pack_name:
            installer = SystemPackageTool()
            installer.install(pack_name) # Install the package, will update the package database if pack_name isn't already installed


SystemPackageTool methods:

- **update()**: Updates the system package manager database. It's called automatically from the ``install()`` method by default.
- **install(packages, update=True, force=False)**: Installs the ``packages`` (could be a list or a string). If ``update`` is True it will
  execute ``update()`` first if it's needed. The packages won't be installed if they are already installed at least of ``force``
  parameter is set to True. If ``packages`` is a list the first available package will be picked (short-circuit like logical **or**).


The use of ``sudo`` in the internals of the ``install()`` and ``update()`` methods is controlled by the CONAN_SYSREQUIRES_SUDO
environment variable, so if the users don't need sudo permissions, it is easy to opt-in/out.

Conan will keep track of the execution of this method, so that it is not invoked again and again
at every conan command. The execution is done per package, since some packages of the same
library might have different system dependencies. If you are sure that all your binary packages
have the same system requirements, just add the following line to your method:

..  code-block:: python

    def system_requirements(self):
         self.global_system_requirements=True
         if ...



imports()
---------------
Importing files copies files from the local store to your project. This feature is handy
for copying shared libraries (dylib in Mac, dll in Win) to the directory of your executable, so that you don't have
to mess with your PATH to run them. But there are other use cases:

- Copy an executable to your project, so that it can be easily run. A good example is the google
  **protobuf** code generator, go to the examples section to check it out.
- Copy package data to your project, like configuration, images, sounds... A good example is the
  OpenCV demo, in which face detection XML pattern files are required.

Importing files is also very convenient in order to redistribute your application, as many times
you will just have to bundle your project's bin folder.

A typical ``imports()`` method for shared libs could be:

.. code-block:: python

   def imports(self):
      self.copy("*.dll", "", "bin")
      self.copy("*.dylib", "", "lib")

If you want to be able to customize the output user directory to work with both the ``cmake`` and ``cmake_multi`` generators, then you can do:

.. code-block:: python

    def imports(self):
        dest = os.getenv("CONAN_IMPORT_PATH", "bin")
        self.copy("*.dll", dst=dest, src="bin")
        self.copy("*.dylib*", dst=dest, src="lib")


And then use, for example: ``conan install -e CONAN_IMPORT_PATH=Release -g cmake_multi``


conan_info()
------------

Deprecated, use ``package_id()`` method instead.


package_id()
------------

Conan keeps the compatibility between binary packages using ``settings``.
When a recipe author specifies some settings in the :ref:`settings_property` property, is telling that any change at any
of those settings will require a different binary package.

But sometimes you would need to alter the general behavior, for example, to have only one binary package for several different compiler versions.

Please, check the section :ref:`how_to_define_abi_compatibility` to get more details.

.. _build_id:

build_id()
------------

In the general case, there is one build folder for each binary package, with the exact same hash/ID
of the package. However this behavior can be changed, there are a couple of scenarios that this might
be interesting:

- You have a build script that generates several different configurations at once, like both debug
  and release artifacts, but you actually want to package and consume them separately. Same for
  different architectures or any other setting
- You build just one configuration (like release), but you want to create different binary packages
  for different consuming cases. For example, if you have created tests for the library in the build
  step, you might want to create to package, one just containing the library for general usage, but
  another one also containing the tests, as a reference and a tool to debug errors.

In both cases, if using different settings, the system will build twice (or more times) the same binaries,
just to produce a different final binary package. With the ``build_id()`` method this logic can be
changed. ``build_id()`` will create a new package ID/hash for the build folder, and you can define
the logic you want in it, for example:

..  code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build_id(self):
       self.info_build.settings.build_type = "Any"


So this recipe will generate a final different package for each debug/release configuration. But
as the ``build_id()`` will generate the same ID for any ``build_type``, then just one folder and
one build will be done. Such build should build both debug and release artifacts, and then the
``package()`` method should package them accordingly to the ``self.settings.build_type`` value.
Still different builds will be executed if using different compilers or architectures. This method
is basically an optimization of build time, avoiding multiple re-builds.

Other information as custom package options can also be changed:

..  code-block:: python

    def build_id(self):
        self.info_build.options.myoption = 'MyValue' # any value possible
        self.info_build.options.fullsource = 'Always'

