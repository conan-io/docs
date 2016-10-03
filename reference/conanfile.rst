.. _conanfile:

conanfile.txt
=============

The ``conanfile.txt`` is just a simplified version of the ``conanfile.py`` that aims for a simpler consumption of existing packages, without having to write a full ``conanfile.py``. Package creators would typically want to create just ``conanfile.py``, not requiring this txt at all.

The conanfile has several sections, [requires], [generators], [options], [imports]. Please check the getting started for explanation of these sections (TODO: full reference here).


conanfile.py
============

Package meta information
------------------------

.. _package_url:

URL (recommended)
+++++++++++++++++

It is possible, even typical, if you are packaging a thid party lib, that you just develop
the packaging code. Such code is also subject to change, often via collaboration, so it should be stored
in a VCS like git, and probably put on GitHub or a similar service. If you do indeed maintain such a
repository, please indicate it in the ``url`` attribute, so that it can be easily found.
 
.. code-block:: python

   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       url = "https://github.com/memsharded/hellopack.git"
       license = "MIT"
       author = "John J. Smith (john.smith@company.com)"
     
           
The ``url`` is the url **of the package** repository, i.e. not necessarily the original source code.
It is optional, but highly recommended, that it points to GitHub, Bitbucket or your preferred
code collaboration platform. Of course, if you have the conanfile inside your library source,
you can point to it, and afterwards use the ``url`` in your ``source()`` method.

License (recommended)
+++++++++++++++++++++
This field is intended for the license of the **target** source code and binaries, i.e. the code
that is being packaged, not the ``conanfile.py`` itself. This info is used to be displayed by
the ``conan info`` command and possibly other search and report tools.

Author (optional)
+++++++++++++++++

Intended to add information about the author, in case it is different from the conan user. It is
possible that the conan user is the name of an organization, project, company or group, and many
users have permissions over that account. In this case, the author information can explicitely
define who is the creator/maintainer of the package


.. _retrieve_source:

Retrieving source code
----------------------

There are 2 ways of getting source code to build a package. The first one is to use the ``exports``
field, where you specify which sources are required, and they will be exported together with
the **conanfile.py**, and stored in the conan stores, both local and remote.

The ``exports`` field can be one single pattern, like ``exports="*"``, or several inclusion patterns.
For example, if we have the source code inside "include" and "src" folders, and there are other folders
that are not necessary for the package recipe, we could do:

.. code-block:: python

   exports = "include*", "src*"



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
       # exports = "hello/*"
   
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



Configuration
-------------

There are several things that can potentially affect a package being created, i.e. the final
package will be different (a different binay, for example), if some input is different.

Settings
++++++++
Development project-wide variables, like the compiler, its version, or the OS 
itself. These variables have to be defined, and they cannot have a default value listed in the
conanfile, as it would not make sense.

It is obvious that changing the OS produces a different binary in most cases. Changing the compiler
or compiler version changes the binary too, which might have a compatible ABI or not, but the
package will be different in any case.

But what happens for example to **header only libraries**? The final package for such libraries is not
binary and, in most cases it will be identical, unless it is automatically generating code.
We can indicate that in the conanfile:

.. code-block:: python

   from conans import ConanFile

   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       # We can just omit the settings attribute too
       settings = None
       
       def build(self):
            #empty too, nothing to build in header only
         
         
You can restrict existing settings and accepted values as well, by redeclaring the settings
attribute:

.. code-block:: python

   class HelloConan(ConanFile):
      settings = {"os": ["Windows"],
                  "compiler": {"Visual Studio": {"version": [11, 12]}},
                  "arch": None}
                  
In this example we have just defined that this package only works in Windows, with VS 10 and 11.
Any attempt to build it in other platforms with other settings will throw an error saying so.
We have also defined that the runtime (the MD and MT flags of VS) is irrelevant for us
(maybe we using a universal one?). Using None as a value means, *maintain the original values* in order
to avoid re-typing them. Then, "arch": None is totally equivalent to "arch": ["x86", "x86_64", "arm"]
Check the reference or your ~/.conan/settings.yml file.

As re-defining the whole settings attribute can be tedious, it is sometimes much simpler to
remove or tune specific fields in the ``config()`` method. For example, if our package is runtime
independent in VS, we can just remove that setting field:


.. code-block:: python
   
   settings = "os", "compiler", "build_type", "arch"
   
   def config(self):
       self.settings.compiler["Visual Studio"].remove("runtime")
       
       
Options
+++++++
Options are similar to settings in the sense that they influence the final package. But they
can typically have a default value. A very common case would be the static/shared option of 
a compiled library, which could be defined as:


.. code-block:: python
   
   class HelloConan(ConanFile):
      ...
      options = {"static": [True, False]}
      default_options = "static=True"
   
      def build(self):
         static = "-DBUILD_SHARED_LIBS=ON" if not self.options.static else ""
         cmake = CMake(self.settings)
         self.run("cmake . %s %s" % (cmake.command_line, static))
         self.run("cmake --build . %s" % cmake.build_config)
         
Note that you have to consider the option properly in your build. In this case, we are using
the CMake way. You must also remove the **STATIC** linkage in the **CMakeLists.txt** file, 
and if you are using VS, you also need to change your code to correctly import/export symbols
for the dll.

You can use the ``ANY`` string to allow any value for a specified option. The range of values for
such an option will not be checked, and any value (as string) will be accepted. 

.. code-block:: python
   
   class HelloConan(ConanFile):
      ...
      options = {"commit": "ANY"}
      default_options = "commit=1234abcd"
      
This could be useful, for example, if you want to have an option so a package can actually reference any specific
commit of a git repository.


Variable configuration
++++++++++++++++++++++
If the package options and settings are related, and you want to configure either, you can do so
in the ``config()`` method. This is an example:

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


Generators
----------

Generators specify which is the output of the ``install`` command in your project folder. By
default, a ``conanbuildinfo.txt`` file is generated, but you can specify different generators:

- **gcc**: conanbuildinfo.gcc
- **cmake**: conanbuildinfo.cmake
- **txt**: conanbuildinfo.txt
- **qmake**: conanbuildinfo.pri
- **qbs**: conanbuildinfo.qbs
- **visual_studio**: conanbuildinfo.props
- **xcode**: conanbuildinfo.xcconfig

You can specify more than one:

.. code-block:: python

   class MyLibConan(ConanFile):
       generators = "cmake", "gcc"


Build policies
--------------

With the ``build_policy`` attribute the package creator can change the default conan's build behavior.
The allowed ``build_policy`` values are:

- ``missing``: If no binary package is found, conan will build it without the need of invoke conan install with **--build missing** option.
- ``always``: The package will be built always, **retrieving each time the source code** executing the "source" method.


.. code-block:: python
   :emphasize-lines: 2

     class PocoTimerConan(ConanFile):
        build_policy = "always" # "missing"



Build helpers
-------------

You can use these classes to prepare your build system's command invocation:

- **CMake**: Prepares the invocation of cmake command with your settings.
- **Gcc**: Prepares the invocation of gcc or g++ with your settings.
- **ConfigureEnvironment**: Sets environment variables with information about your settings and requirements. Useful for configure/make.

Check the :ref:`Managing your dependencies/Using conanfile.py <conanfile_py_managed_settings>` to view some examples of compile helpers' use. 


Requirements
------------

Specify package dependencies as a list of other packages:


.. code-block:: python

   class MyLibConan(ConanFile):
       requires = "Hello/1.0@user/stable", "OtherLib/2.1@otheruser/testing"

You can specify further information about the package requirements:

.. code-block:: python

   class MyLibConan(ConanFile):
      requires = (("Hello/0.1@user/testing"),
                  ("Say/0.2@dummy/stable", "override"),
                  ("Bye/2.1@coder/beta", "private"))

Requirements can be complemented by 2 different parameters:

**private**: a dependency can be declared as private if it is going to be fully embedded and hidden
from consumers of the package. Typical examples could be a header only library which is not exposed
through the public interface of the package, or the linking of a static library inside a dynamic
one, in which the functionality or the objects of the linked static library are not exposed through
the public interface of the dynamic library.

**override**: packages can define overrides of their dependencies, if they require the defininition of
specific versions of the upstream required libraries, but not necessarily direct dependencies. For example, 
a package can depend on A(v1.0), which in turn could conditionally depend on Zlib(v2), depending on whether
the compression is enabled or not. Now, if you want to force the usage of Zlib(v3) you can:

..  code-block:: python

   class HelloConan(ConanFile):
      requires = ("A/1.0@user/stable", ("Zlib/3.0@other/beta", "override"))
      

This **will not introduce a new dependency**, it will just change Zlib v2 to v3 if A actually
requires it. Otherwise Zlib will not be a dependency of your package.


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
        self.requires("zlib/1.2@drl/testing", private=True, override=False)
        
.. _system_requirements:

System requirements
-------------------
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
            installer.update() # Update the package database
            installer.install(pack_name) # Install the package 


The use of ``sudo`` in the internals of the ``install()`` method is controlled by the CONAN_SYSREQUIRES_SUDO
environment variable, so if the users don't need sudo permissions, it is easy to opt-in/out.

Conan will keep track of the execution of this method, so that it is not invoked again and again
at every conan command. The execution is done per package, since some packages of the same
library might have different system dependencies. If you are sure that all your binary packages
have the same system requirements, just add the following line to your method:

..  code-block:: python

    def system_requirements(self):
         self.global_system_requirements=True
         if ...


Packaging
---------
The actual creation of the package, once that it is build, is done in the ``package()`` method.
Using the ``self.copy()`` method, artifacts are copied from the build folder to the package folder.
The syntax of copy is as follows:

.. code-block:: python

   self.copy(pattern, dst, src, keep_path=False)


- ``pattern`` is a pattern following fnmatch syntax of the files you want to copy, from the *build* to the *package* folders. Typically something like ``*.lib`` or ``*.h``
- ``dst`` is the destination folder in the package. They will typically be ``include`` for headers, ``lib`` for libraries and so on, though you can use any convention you like
- ``src`` is the folder where you want to search the files in the *build* folder. If you know that your libraries when you build your package will be in *build/lib*, you will typically use ``build/lib`` in this parameter. Leaving it empty means the root build folder.
- ``keep_path``, with default value=True, means if you want to keep the relative path when you copy the files from the source(build) to the destination(package). Typically headers, you keep the relative path, so if the header is in *build/include/mylib/path/header.h*, you write:

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


(Unit) Testing your library
---------------------------
We have seen how to run package tests with conan, but what if we want to run full unit tests on
our library before packaging, so that they are run for every build configuration?
Nothing special is required here. We can just launch the tests from the last command in our
``build()`` method:

.. code-block:: python

   def build(self):
      cmake = CMake(self.settings)
      self.run("cmake . %s %s" % (cmake.command_line))
      self.run("cmake --build . %s" % cmake.build_config)
      # here you can run CTest, launch your binaries, etc
      self.run("ctest")
      
 
C++ build information
---------------------
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
  
Environment information
-----------------------

Each package can also define some environment variables that the package needs to be reused.
It's specially useful for :ref:`installer packages<create_installer_packages>`, to set the path with the "bin" folder of the packaged application.
This can be done in the ``env_info`` attribute within the ``package_info()`` method.

.. code-block:: python

  self.env_info.path.append("ANOTHER VALUE") # Append "ANOTHER VALUE" to the path variable
  self.env_info.othervar = "OTHER VALUE" # Assign "OTHER VALUE" to the othervar variable
  self.env_info.thirdvar.append("some value") # Every variable can be set or appended a new value 
  

The :ref:`virtualenv<virtual_environment_generator>` generator will use the self.env_info variables to prepare a script to activate/deactive a virtual environment.

This defined variables will be also read by the build helper ``ConfigureEnvironment``. It will provide us the command line to set the defined environment variables.
            
        
Importing files
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

Package information
-------------------
Each package will translate its settings, options and requirements to a unique sha1 signature.
A convention is established to define such mapping, but you could change it according to your needs.
For example, suppose that you are building a pure C library with a certain compiler and version, so you
define the package to have the usual settings. But then you realize than every consumer using a different
compiler will try to depend on a different package, re-building it from source if you have not generated it.
Since the ABI is compatible, you might want to only build one package, with your preferred compiler version.
You can *narrow* this setting as follows:

.. code-block:: python

   class MyLibConan(ConanFile):
       name = "MyLib"
       version = "2.5"
       settings = "os", "compiler", "build_type", "arch"
       
       def conan_info(self):
           self.info.settings.compiler.version = "Any"
           
Note that this setting can take any value. It is not subject to validation. You can notice that
we actually have 2 instances of settings, the normal, "full" settings, ``self.settings`` and
``self.info.settings``. The latter is the one used to compute the sha1 signature and it is
initially a copy of ``self.settings``.

Both are shown in the **conaninfo.txt** file. ``[settings]`` is the latter, used to compute the sha1,
with the "Any" value, and ``[full_settings]`` is the former, the one passed as configuration, holding the actual
compiler version that has been used to create the package.

C++ ABI compatibility among different compiler and versions is not assumed, nor hardcoded.
g++ 4.8 will be generally considered different to g++ 4.9 and g++ 5.0. If you are sure your
package ABI compatibility is fine for versions 4.X, but changes with 5.0, you could try
something like:

.. code-block:: python
       
   def conan_info(self):
      v = self.settings.compiler.version
      if self.settings.compiler == "gcc" and (v == "4.8" or v == "4.9"):
         self.info.settings.compiler.version = "4.8-9"
   
This behavior can also be very useful if you want to specify compiler settings to be able to build
and run unit tests, but the library is actually header only. 

Similarly we can change the signature options (though this use case might be rare) and the
package requirements. For example, a typical **conaninfo.txt** requiring a stable dependency
could contain:


.. code-block:: text

   [requires]
       Hello/1.Y.Z
   
   [full_requires]
       Hello/1.1@demo/testing:73bce3fd7eb82b2eabc19fe11317d37da81afa56
       
This scheme asumes that changing the upstream Hello dependency will not affect my package, as
long as the major version is not changed. Let's say that the "Hello" lib does not follow semver,
and it breaks binary compatibility in each minor release. Then, we should change our ``info``
as follows:

.. code-block:: python

   def conan_info(self):
      hello_require = self.info.requires["Hello"]
      hello_require.version = hello_require.full_version.minor()
      
That will produce a **conaninfo.txt** file like:

.. code-block:: text

   [requires]
       Hello/1.1.Z
       
       
.. note::

   Remember that, following semver, versions<1.0 (0.Y.Z) are considered to be unstable, so they will
   be included in the [requires] section as they are, and influence the signature, forcing re-build
   of packages when upstream 0.Y.Z dependencies change, even for patches. Change it in your
   conan_info() method if you need to.


Windows path length limit
-------------------------
If one of the packages you are creating hits the limit of 260 chars path length in Windows, add
``short_paths=True`` in your conanfile.py:

..  code-block:: python

   from conans import ConanFile

   class ConanFileTest(ConanFile):
       ...
       short_paths = True

This will automatically "link" the ``source`` and ``build`` directories of the package to the drive root, 
something like `C:/.conan/tmpdir`. All the folder layout in the conan cache is maintained.


Relative imports
----------------
If you want to reuse common functionality between different packages, it can be written in their
own python files and imported from the main ``conanfile.py``. Lets write for example a ``msgs.py``
file and put it besides the ``conanfile.py``:

..  code-block:: python

   def build_msg(output):
      output.info("Building!")

And then the main ``conanfile.py`` would be:

..  code-block:: python

   from conans import ConanFile
   from msgs import build_msg

   class ConanFileToolsTest(ConanFile):
       name = "test"
       version = "1.9"
       exports = "msgs.py"  # Important to remember!
   
       def build(self):
           build_msg(self.output)
           # ...


It is important to note that such ``msgs.py`` file **must be exported** too when exporting the package, 
because package recipes must be self-contained

Other
-----
There are some helpers in the conanfile for colored output and running commands:

..  code-block:: python

   self.output.info("This is a warning, should be yellow")
   self.output.warn("This is a warning, should be yellow")
   self.output.error("Error, should be red")
   self.output.rewrite_line("for progress bars, issues a cr")
   
Check the source code. You might be able to produce different outputs with different colors.


``self.run()`` is a helper to run system commands and throw exceptions when errors occur,
so that command errors are do not pass unnoticed. It is just a wrapper for ``os.system()``

``self.conanfile_directory`` is a property that returns the directory in which the conanfile is
located.
