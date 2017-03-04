.. _conanfile:


conanfile
==========


description
------------
This is an optional, but strongly recommended text field, containing the description of the package,
and any information that might be useful for the consumers. The first line might be used as a
short description of the package.


.. code-block:: python

   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       description = """This is a Hello World library.
                        A fully featured, portable, C++ library to say Hello World in the stdout,
                        with incredible iostreams performance"""
       

.. _package_url:

url
---

It is possible, even typical, if you are packaging a thid party lib, that you just develop
the packaging code. Such code is also subject to change, often via collaboration, so it should be stored
in a VCS like git, and probably put on GitHub or a similar service. If you do indeed maintain such a
repository, please indicate it in the ``url`` attribute, so that it can be easily found.
 
.. code-block:: python

   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       url = "https://github.com/memsharded/hellopack.git"
     
           
The ``url`` is the url **of the package** repository, i.e. not necessarily the original source code.
It is optional, but highly recommended, that it points to GitHub, Bitbucket or your preferred
code collaboration platform. Of course, if you have the conanfile inside your library source,
you can point to it, and afterwards use the ``url`` in your ``source()`` method.

This is a recommended, but not mandatory attribute.

license
---------
This field is intended for the license of the **target** source code and binaries, i.e. the code
that is being packaged, not the ``conanfile.py`` itself. This info is used to be displayed by
the ``conan info`` command and possibly other search and report tools.

.. code-block:: python

   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       license = "MIT"
       
This attribute can contain several, comma separated licenses. It is a text string, so it can
contain any text, including hyperlinks to license files elsewhere.

This is a recommended, but not mandatory attribute.

author
------

Intended to add information about the author, in case it is different from the conan user. It is
possible that the conan user is the name of an organization, project, company or group, and many
users have permissions over that account. In this case, the author information can explicitely
define who is the creator/maintainer of the package

.. code-block:: python

   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       author = "John J. Smith (john.smith@company.com)"

This is an optional attribute

.. _user_channel:

user, channel
--------------

The fields ``user`` and ``channel`` can be accessed from within a ``conanfile.py``.
Though their usage is usually not encouraged, it could be useful in different cases,
e.g. to define requirements with the same user and
channel than the current package, which could be achieved with something like:

.. code-block:: python

    from conans import ConanFile
    
    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
    
        def requirements(self):
            self.requires("Say/0.1@%s/%s" % (self.user, self.channel))
            

Only package recipes that are in the conan local cache (i.e. "exported") have an user/channel assigned.
For package recipes working in user space, there is no current user/channel. The properties ``self.user``
and ``self.channel`` will then look for environment variables ``CONAN_USERNAME`` and ``CONAN_CHANNEL``
respectively. If they are not defined, an error will be raised.


.. _settings_property:

settings
----------

There are several things that can potentially affect a package being created, i.e. the final
package will be different (a different binary, for example), if some input is different.

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
       
.. _conanfile_options:
       
options, default_options
---------------------------
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

You can also specify options of the package dependencies:

.. code-block:: python
   
   class HelloConan(ConanFile):
      requires = "Pkg/0.1@user/channel"
      default_options = "Pkg:pkg_option=value"
      
If you need to dynamically set some dependency options, you could do:

.. code-block:: python
   
   class HelloConan(ConanFile):
      requires = "Pkg/0.1@user/channel"

      def configure(self):
          self.options["Pkg"].pkg_option = "value"

requires
---------

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

**override**: packages can define overrides of their dependencies, if they require the definition of
specific versions of the upstream required libraries, but not necessarily direct dependencies. For example, 
a package can depend on A(v1.0), which in turn could conditionally depend on Zlib(v2), depending on whether
the compression is enabled or not. Now, if you want to force the usage of Zlib(v3) you can:

..  code-block:: python

   class HelloConan(ConanFile):
      requires = ("A/1.0@user/stable", ("Zlib/3.0@other/beta", "override"))
      

This **will not introduce a new dependency**, it will just change Zlib v2 to v3 if A actually
requires it. Otherwise Zlib will not be a dependency of your package.

.. _version_ranges:

version ranges
++++++++++++++

From conan 0.16, version ranges expressions are supported, both in ``conanfile.txt`` and in
``conanfile.py`` requirements. The syntax is using brackets:

..  code-block:: python

   class HelloConan(ConanFile):
      requires = "Pkg/[>1.0,<1.8]@user/stable"

Expressions are those defined and implemented by [python node-semver](https://pypi.python.org/pypi/node-semver),
but using a comma instead of spaces. Accepted expressions would be:

..  code-block:: python

   >1.1,<2.1    # In such range
   2.8          # equivalent to =2.8
   ~=3.0        # compatible, according to semver
   >1.1 || 0.8  # conditions can be OR'ed

Version ranges expressions are evaluated at the time of building the dependencies graph, from
downstream to upstream dependencies. No joint-compatibility of the full graph is computed, instead,
version ranges are evaluated when dependencies are first retrieved.

This means, that if a package A, depends on another package B (A->B), and A has a requirement for
``C/[>1.2,<1.8]``, this requirements is evaluated first and it can lead to get the version ``C/1.7``. If
package B has the requirement to ``C/[>1.3,<1.6]``, this one will be overwritten by the downstream one,
it will output a version incompatibility error. But the "joint" compatibility of the graph will not
be obtained. Downstream packages or consumer projects can impose their own requirements to comply
with upstream constraints, in this case a override dependency to ``C/[>1.3,<1.6]`` can be easily defined
in the downstream package or project.

The order of search for matching versions is as follows:

- First, the local conan storage is searched for matching versions, unless the ``--update`` flag
  is provided to ``conan install``
- If a matching version is found, it is used in the dependency graph as a solution
- If no matching version is locally found, it starts to search in the remotes, in order. If some
  remote is specified with ``-r=remote``, then only that remote will be used.
- If the ``--update`` parameter is used, then the existing packages in the local conan cache will
  not be used, and the same search of the previous steps is carried out in the remotes. If new
  matching versions are found, they will be retrieved, so subsequents call to ``install`` will
  find them locally and use them.


exports
--------
If a package recipe ``conanfile.py`` requires other external files, like other python files that
it is importing (python importing), or maybe some text file with data it is reading, those files
must be exported with the ``exports`` field, so they are stored together, side by side with the
``conanfile.py`` recipe.

The ``exports`` field can be one single pattern, like ``exports="*"``, or several inclusion patterns.
For example, if we have some python code that we want the recipe to use in a ``helpers.py`` file,
and have some text file, ``info.txt``, we want to read and display during the recipe evaluation
we would do something like:

.. code-block:: python

   exports = "helpers.py", "info.txt"
   
This is an optional attribute, only to be used if the package recipe requires these other files
for evaluation of the recipe.

exports_sources
----------------
There are 2 ways of getting source code to build a package. Using the ``source()`` recipe method
and using the ``exports_sources`` field. With ``exports_sources`` you specify which sources are required, 
and they will be exported together with the **conanfile.py**, copying them from your folder to the
local conan cache. Using ``exports_sources``
the package recipe can be self-contained, containing the source code like in a snapshot, and then
not requiring downloading or retrieving the source code from other origins (git, download) with the 
``source()`` method when it is necessary to build from sources.

The ``exports_sources`` field can be one single pattern, like ``exports_sources="*"``, or several inclusion patterns.
For example, if we have the source code inside "include" and "src" folders, and there are other folders
that are not necessary for the package recipe, we could do:

.. code-block:: python

   exports_sources = "include*", "src*"
   
This is an optional attribute, used typically when ``source()`` is not specify. The main difference with
``exports`` is that ``exports`` files are always retrieved (even if pre-compiled packages exist),
while ``exports_sources`` files are only retrieved when it is necessary to build a package from sources.
   
generators
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
   
build_policy
--------------

With the ``build_policy`` attribute the package creator can change the default conan's build behavior.
The allowed ``build_policy`` values are:

- ``missing``: If no binary package is found, conan will build it without the need of invoke conan install with **--build missing** option.
- ``always``: The package will be built always, **retrieving each time the source code** executing the "source" method.


.. code-block:: python
   :emphasize-lines: 2

     class PocoTimerConan(ConanFile):
        build_policy = "always" # "missing"   
        
short_paths
------------

If one of the packages you are creating hits the limit of 260 chars path length in Windows, add
``short_paths=True`` in your conanfile.py:

..  code-block:: python

   from conans import ConanFile

   class ConanFileTest(ConanFile):
       ...
       short_paths = True

This will automatically "link" the ``source`` and ``build`` directories of the package to the drive root, 
something like `C:/.conan/tmpdir`. All the folder layout in the conan cache is maintained.

This attribute will not have any effect in other OS, it will be discarded.

From Windows 10 (ver. 10.0.14393), it is possible to opt-in disabling the path limits. Check `this link 
<https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx#maxpath>`_ for more info. Latest python installers might offer to enable this while installing python. With this limit removed, the ``short_paths`` functionality is totally unnecessary.


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

Check the :ref:`Managing your dependencies/Using conanfile.py <conanfile_py_managed_settings>` to view some examples of compile helpers' use. 



(Unit) Testing your library
++++++++++++++++++++++++++++
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
      
 
package()
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
- ``links``, with default value=False, you can activate it to copy symlinks, like typical lib.so->lib.so.9


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
        self.requires("zlib/1.2@drl/testing", private=True, override=False)
        
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
            installer.update() # Update the package database
            installer.install(pack_name) # Install the package 


SystemPackageTool methods:

- **update()**: Updates the system package manager database.
- **install(packages, update=True, force=False)**: Installs the ``packages`` (could be a list or a string). If ``update`` is True it will
  execute ``update()`` first if it's needed. The packages won't be installed if they are already installed at least of ``force``
  parameter is set to True.


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
  


Other
------

There are some helpers in the conanfile for colored output and running commands:

..  code-block:: python

   self.output.success("This is a good, should be green")
   self.output.info("This is a neutral, should be white")
   self.output.warn("This is a warning, should be yellow")
   self.output.error("Error, should be red")
   self.output.rewrite_line("for progress bars, issues a cr")
   
Check the source code. You might be able to produce different outputs with different colors.


``self.run()`` is a helper to run system commands and throw exceptions when errors occur,
so that command errors are do not pass unnoticed. It is just a wrapper for ``os.system()``

``self.conanfile_directory`` is a property that returns the directory in which the conanfile is
located.

.. _split_conanfile:

Splitting conanfile.py
-----------------------
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
because package recipes must be self-contained.

The code reuse can also be done in the form of a base class, something like a file ``base_conan.py``

..  code-block:: python

    from conans import ConanFile
    
    class ConanBase(ConanFile):
        # common code here
   
And then:

..  code-block:: python

    from conans import ConanFile
    from base_conan import ConanBase
    
    class ConanFileToolsTest(ConanBase):
        name = "test"
        version = "1.9"
       

