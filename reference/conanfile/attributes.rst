Attributes
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
         cmake = CMake(self)
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

.. _version_ranges_reference:

version ranges
++++++++++++++

The syntax is using brackets:

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


.. container:: out_reference_box

    Go to :ref:`Mastering/Version Ranges<version_ranges>` if you want to learn more about version ranges.

build_requires
----------------

Build requirements are requirements that are only installed and used when the package is built from sources. If there is an existing pre-compiled binary, then the build requirements for this package will not be retrieved.

They can be specified as a comma separated tuple in the package recipe:

.. code-block:: python

    class MyPkg(ConanFile):
        build_requires = "ToolA/0.2@user/testing", "ToolB/0.2@user/testing"

Read more: :ref:`Build requiremens <build_requires>`


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

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

   exports = "*.py", "!*tmp.py"


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

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

   exports_sources = "include*", "src*", "!src/build/*"

This is an optional attribute, used typically when ``source()`` is not specify. The main difference with
``exports`` is that ``exports`` files are always retrieved (even if pre-compiled packages exist),
while ``exports_sources`` files are only retrieved when it is necessary to build a package from sources.

generators
----------

Generators specify which is the output of the ``install`` command in your project folder. By
default, a ``conanbuildinfo.txt`` file is generated, but you can specify different generators.

Check the full generators list in :ref:`Reference/Generators<generators>`

You can specify more than one generator:

.. code-block:: python

   class MyLibConan(ConanFile):
       generators = "cmake", "gcc"


build_policy
------------

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


no_copy_source
---------------

The attribute ``no_copy_source`` tells the recipe that the source code will not be copied from the ``source`` folder to the ``build`` folder. 
This is mostly an optimization for packages with large source codebases, to avoid extra copies. It is **mandatory** that the source code must not be modified at all by the configure or build scripts, as the source code will be shared among all builds.

To be able to use it, the package recipe can access the ``self.source_folder`` attribute, which will point to the ``build`` folder when ``no_copy_source=False`` or not defined, and will point to the ``source`` folder when ``no_copy_source=True``

folders
---------
In the package recipe methods, some attributes pointing to the relevant folders can be defined. Not all of them will be defined always, only in those relevant methods that might use them.

- ``self.source_folder``: the folder in which the source code to be compiled lives. When a package is built in the conan local cache, by default it is the ``build`` folder, as the source code is copied from the ``source`` folder to the ``build`` folder, to ensure isolation and avoiding modifications of shared common source code among builds for different configurations. Only when ``no_copy_source=True`` this folder will actually point to the package ``source`` folder in the local cache.
- ``self.build_folder``: the folder in which the build is being done
- ``self.package_folder``: the folder to copy the final artifacts for the package binary

When executing local conan commands (for a package not in the local cache, but in user folder), those fields would be pointing to the corresponding local user folder.

cpp_info
--------

Typically set in ``package_info()``, the ``cpp_info`` attribute has the following properties you can assign/append to:

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



conanfile_directory
-------------------

``self.conanfile_directory`` is a **read only property** that returns the directory in which the conanfile is
located.
