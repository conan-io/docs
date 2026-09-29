.. _package_layout:

Package layout
==============

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.
    The ``layout()`` feature will be fully functional only in the new build system integrations
    (:ref:`in the conan.tools space <conan_tools>`). If you are using other integrations, they
    might not fully support this feature.


Available since: `1.37.0 <https://github.com/conan-io/conan/releases/tag/1.37.0>`_

Before starting
---------------

To understand correctly how the ``layout()`` method can help us we need to recall first how Conan works.

Let's say we are working in a project, using, for example, CMake:

.. code-block:: text

    <my_project_folder>
    ├── conanfile.py
    └── src
        ├── CMakeLists.txt
        ├── hello.cpp
        ├── my_tool.cpp
        └── include
            └── hello.h

When we call ``conan create``, this is a simplified description of what happens:

1. Conan exports the recipe (conanfile.py) and the declared sources (exports_sources) to the cache. The folders in the
   cache would be something like:

   .. code-block:: text
        :caption: .conan/data/<some_cache_folder>

        ├── export
        │   └── conanfile.py
        └── export_source
            └── src
                ├── CMakeLists.txt
                ├── hello.cpp
                ├── my_tool.cpp
                └── include
                    └── hello.h

2. If the method ``source()`` exists, it might retrieve sources from the internet. Also, the ``export_source`` folder
   is copied to the ``source`` folder.

   .. code-block:: text
        :caption: .conan/data/<some_cache_folder>

        ├── export
        │   └── conanfile.py
        ├── export_source
        │   └── src
        │       ├── CMakeLists.txt
        │       ├── hello.cpp
        │       ├── my_tool.cpp
        │       └── include
        │           └── hello.h
        └── source
            └── src
                ├── CMakeLists.txt
                ├── hello.cpp
                ├── my_tool.cpp
                └── include
                    └── hello.h


3. Before calling the ``build()`` method, a build folder is created and the **sources** are copied there. Later, we call
   the ``build()`` method so the libraries and executables are built:

   .. code-block:: text
        :caption: .conan/data/<some_cache_folder>

        ├── export
        │   └── conanfile.py
        ├── export_source
        │   └── src
        │       ├── CMakeLists.txt
        │       ├── hello.cpp
        │       ├── my_tool.cpp
        │       └── include
        │           └── hello.h
        ├── source
        │   └── src
        │       ├── CMakeLists.txt
        │       ├── hello.cpp
        │       ├── my_tool.cpp
        │       └── include
        │           └── hello.h
        └── build
            └── <build_id>
                ├── say.a
                └── bin
                    └── my_app

4. At last, Conan calls the ``package()`` method to copy the built artifacts from the ``source`` (typically includes)
   and ``build`` folders (libraries and executables) to a **package** folder.

   .. code-block:: text
        :caption: .conan/data/<some_cache_folder>

        ├── export
        │   └── conanfile.py
        ├── export_source
        │   └── src
        │       ├── CMakeLists.txt
        │       ├── hello.cpp
        │       ├── my_tool.cpp
        │       └── include
        │           └── hello.h
        ├── source
        │   └── src
        │       ├── CMakeLists.txt
        │       ├── hello.cpp
        │       ├── my_tool.cpp
        │       └── include
        │           └── hello.h
        ├── build
        │   └── <build_id>
        │       ├── say.a
        │       └── bin
        │           └── my_app
        └── package
            └── <package_id>
                ├── lib
                │   └── say.a
                ├── bin
                │   └── my_app
                └── include
                    └── hello.h

5. The ``package_info(self)`` method will describe with the ``self.cpp_info`` object the contents of the ``package``
   folder, that is the one the consumers use to link against it. If we call `conan create` with different configurations
   the base folder in the cache is different and nothing gets messed.


   .. code-block:: python
       :caption: conanfile.py

       import os
       from conans import ConanFile
       from conan.tools.cmake import CMake


       class SayConan(ConanFile):
           name = "say"
           version = "0.1"
           exports_sources = "src/*"
           ...
           def package_info(self):
               # These are default values and doesn't need to be adjusted
               self.cpp_info.includedirs = ["include"]
               self.cpp_info.libdirs = ["lib"]
               self.cpp_info.bindirs = ["bin"]

               # The library name
               self.cpp_info.libs = ["say"]


So, this workflow in the cache works flawlessly but:

- What if I'm developing the recipe in my local project and want to use the local methods (**conan source**, **conan build**) and
  later call **export-pkg** to create the package?

  If you call **conan build** in your working directory, without specifying a ``--build-folder`` argument, you will end up
  with a bunch of files polluting your project. Moreover, if you want to build more configurations you will need to create
  several build folders by hand, this is inconvenient, error-prone, and wouldn't be easy for Conan to locate the correct
  artifacts if you want to call **export-pkg** later.

- What if I don't even want to call **conan build** but use my CLion IDE to build the project?

  By default, the CLion IDE will create the folders **cmake-build-release** and **cmake-build-debug** to put the build
  files there, so maybe your ``package()`` method is not able to locate the files in there and the **export-pkg** might
  fail.

- What if I want to use my project as an :ref:`editable package<editable_packages>`?

  If you want to keep developing your package but let the consumers link with the artifacts in your project instead of
  the files in the Conan cache, this will not work, because it only declares the location of headers and libraries in 
  the final packaged layout, but during development the files are typically in other locations.


So, just as we describe the package folder in the ``package_info()`` method, we can use ``layout()`` to describe the
``source`` and ``build`` folders (both in a local project and in the cache):

  - We can run the conan local commands (**conan source**, **conan build**, **conan export-pkg**) without taking care of
    specifying directories, always with the same syntax.
  - If you are using an IDE, you can describe the build folder naming in the layout, so the libraries and executables
    are always in a known place.
  - In the cache, the layout (like a build subfolder) is kept, so we can always know where the artifacts are before
    packaging them.
  - It enables tools like the :ref:`AutoPackager<conan_tools_files_autopackager>` to automate the **package()** method.
  - It out-of-the-box enables to use :ref:`editable packages<editable_packages>`, because the recipe describes
    where the contents will be, even for different configurations, so the consumers can link with the correct built
    artifacts.


Declaring the layout
--------------------

In the ``layout()`` method, you can set:

    - **self.folders**

         - **self.folders.source**: To specify a folder where your sources are.
         - **self.folders.build**: To specify a subfolder where the files from the build are (or will be).
         - **self.folders.generators**: To specify a subfolder where to write the files from the generators and the toolchains
           (e.g. the `xx-config.cmake` files from the ``CMakeDeps`` generator).
         - **self.folders.imports**: To specify a subfolder where to write the files copied when using the ``imports(self)``
           method in a ``conanfile.py``.
         - **self.folders.root**: To specify the relative path from the ``conanfile.py`` to the root of the project, in case 
           the ``conanfile.py`` is in a subfolder and not in the project root. If defined, all the other paths will be relative to
           the project root, not to the location of the ``conanfile.py``.

         Check the :ref:`complete reference<layout_folders_reference>` of the **self.folders** attribute.

    - **self.cpp.source** and **self.cpp.build**: The same you set the ``self.cpp.package`` to describe the package folder
      after calling the ``package()`` method, you can also describe the `source` and `build` folders.

    - **self.cpp.package**: You can use it as you use the **self.cpp_info** at the ``package_info(self)`` method.
      The **self.cpp_info** object will be populated with the information declared in the ``self.cpp.package``
      object, so you can complete it or modify it later in the ``package_info(self)`` method.

    - **self.layouts.source**, **self.layouts.build** and **self.layouts.package**, each one containing one instance of
      ``buildenv_info``, ``runenv_info`` and ``conf_info``. If the environment or configuration needs to define values 
      that depend on the current folders, it is necessary to define them in the ``layout()`` method.
  

Example: Everything together
----------------------------

Let's say we are working in the project introduced in the section above:

.. code-block:: text

    <my_project_folder>
    ├── conanfile.py
    └── src
        ├── CMakeLists.txt
        ├── hello.cpp
        ├── my_tool.cpp
        └── include
            └── hello.h

We are using the following **CMakeLists.txt**:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.15)
   project(say CXX)

   add_library(say hello.cpp)
   target_include_directories(say PUBLIC "include")

   add_executable(my_tool my_tool.cpp)
   target_link_libraries(my_tool say)

   # The executables are generated at the "bin" folder
   set_target_properties(my_tool PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")


Let’s see how we describe our project in the ``layout()`` method:

.. code-block:: python
    :caption: conanfile.py

    import os
    from conans import ConanFile
    from conan.tools.cmake import CMake


    class SayConan(ConanFile):
        name = "say"
        version = "0.1"
        exports_sources = "src/*"
        ...
        def layout(self):
            self.folders.source = "src"
            build_type = str(self.settings.build_type).lower()
            self.folders.build = "cmake-build-{}".format(build_type)
            self.folders.generators = os.path.join(self.folders.build, "conan")

            self.cpp.package.libs = ["say"]
            self.cpp.package.includedirs = ["include"] # includedirs is already set to this value by
                                                       # default, but declared for completion

            # this information is relative to the source folder
            self.cpp.source.includedirs = ["include"]  # maps to ./src/include

            # this information is relative to the build folder
            self.cpp.build.libdirs = ["."]             # maps to ./cmake-build-<build_type>
            self.cpp.build.bindirs = ["bin"]           # maps to ./cmake-build-<build_type>/bin

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            # we can also know where the executable we are building is
            self.run(os.path.join(self.build_folder, self.cpp.build.bindirs[0], "my_tool"))


Let's review the ``layout()`` method changes:

- **self.folders**

   - As we have our sources in the ``src`` folder, ``self.folders.source`` is set to "**src**".
   - We set ``self.folders.build`` to be **cmake-build-release** or **cmake-build-debug** depending on the build_type.
   - The ``self.folders.generators`` folder is where all files generated by Conan will be stored so they don’t pollute the other folders.

   Please, note that the values above are for a single-configuration CMake generator. To support multi-configuration generators,
   such as Visual Studio, you should make some changes to this layout. For a complete layout that supports both single-config
   and multi-config, please check the :ref:`cmake_layout()<conan_tools_layout_predefined_layouts>` in the Conan documentation.

- **self.cpp**

   We can set the information about the package that the consumers need to use by setting the conanfile’s ``cpp.package`` attributes values:

   - Declaring ``self.cpp.package.libs`` inside the ``layout()`` method is equivalent to the “classic” ``self.cpp_info.libs`` declaration
     in the ``package_info()`` method.
   - Also, as you may know, ``self.cpp.package.includedirs`` is set to ``["include"]`` by default, so there’s no need in declaring it but we
     are leaving it here for completeness.

   We can also describe the ``source`` and ``build`` folders with the ``cpp.source`` and ``cpp.build`` objects:

   - We are setting ``self.cpp.source.includedirs = ["include"]``. The ``self.folders.source`` information will
     be automatically prepended to that path for consumers so, for example, when working with an editable package, Conan will try to get the
     include files from the **./my_project_folder/src/include** folder.
   - We set the ``self.cpp.build.libdirs`` to **["."]**, so we are declaring that, if we make the package ``editable``,
     the libraries will be at the **./cmake-build-<build_type>** folder.
   - We set the ``self.cpp.build.bindirs`` to **["bin"]**, because the ``CMakeLists.txt`` file is changing the ``RUNTIME_OUTPUT_DIRECTORY`` to
     that directory.

There is also an interesting line in the ``build(self)`` method:

.. code-block:: python
    :caption: conanfile.py

      def build(self):
         ...
         # we can also know where is the executable we are building
         self.run(os.path.join(self.build_folder, self.cpp.build.bindirs[0], "my_tool"))

We are using the ``self.cpp.build.bindirs[0]`` folder to locate the ``my_tool``. This is a very recommended
practice, especially when our layout depends on the build system. For example, when using CMake with Visual Studio,
the binaries are typically built at **Release/** or **Debug/** (multiconfiguration) but on Linux or macOS, the
output folder will typically be **"."**, so it is better to declare the layout ``self.cpp.build.bindirs`` following that logic and
then just access the correct path if we need to know where the resulting files of our build are. If you check the
:ref:`cmake_layout()<conan_tools_layout_predefined_layouts>`, you can see that the predefined ``cmake_layout`` is doing
exactly that when using a multiconfiguration build system.

So, now we can run the conan local methods without taking much care of the directories where the
files are or the build files should be, because everything is declared in the layout:

.. code:: bash

    # This will write the toolchains and generator files from the dependencies to cmake-build-debug/generators
    $ conan install . -if=my_install -s build_type=Debug

    # In case we needed it (not the case as we don't have a source() method), this would fetch the sources to the ./src folder
    $ conan source . -if=my_install

    # This will build the project using the declared source folder and cmake-build-debug as the build folder
    $ conan build . -if=my_install

.. note::

    Maybe you are wondering why the **install folder** is not parametrized and has to be specified with the ``-if``
    argument.
    Currently, Conan generates several files like the ``graph_info.json`` and the ``conanbuildinfo.txt`` that
    are read to restore the configuration saved (settings, options, etc) to be applied in the local commands.
    That configuration is needed before running the ``layout()`` method because the folders might depend on the settings
    like in the previous example. It is a kind of a chicken-egg issue. In Conan 2.0, likely, the
    configuration won't be stored, and the local methods like :command:`conan build .` will compute the graph
    from arguments (--profile, -s, -o...) and won't need the ``--if`` argument anymore, being always trivial to run.


Our current folder now looks like this:

.. code-block:: text

    <my_project_folder>
    ├── conanfile.py
    ├── src
    │   ├── CMakeLists.txt
    │   ├── hello.cpp
    │   ├── my_tool.cpp
    │   └── include
    │       └── hello.h
    └── cmake-build-debug
        ├── libsay.a
        └── bin
            └── my_tool


We could put the package in editable mode and other packages that require it would consume it in a
completely transparent way, even locating the correct **Release**/**Debug** artifacts.

.. code:: bash

    $ conan editable add . say/0.1

.. note:: When working with editable packages, the information set in ``self.cpp.source`` and ``self.cpp.build`` will be merged with the
          information set in ``self.cpp.package`` so that we don’t have to declare again something like ``self.cpp.build.libs = ["say"]`` that is
          the same for the consumers, independently of whether the package is in editable mode or not.


And of course, we can run also a ``conan create`` command. When the ``build(self)`` method is run in the conan cache, it is
also able to locate the ``my_tool`` correctly, because it is using the same ``folders.build``:


.. code-block:: text
     :caption: .conan/data/<some_cache_folder>
     :emphasize-lines: 9

     ├── source
     │   └── src
     │       ├── CMakeLists.txt
     │       ├── hello.cpp
     │       ├── my_tool.cpp
     │       └── include
     │           └── hello.h
     ├── build
     │   └── cmake-build-debug
     │       ├── say.a
     │       └── bin
     │           └── my_app
     └── package
         ├── lib
         │   └── say.a
         ├── bin
         │   └── my_app
         └── include
             └── hello.h


.. warning:: The ``conan package`` local command has been disabled (will raise an exception) when the ``layout()`` method
   is declared. If the package can be consumed "locally" in a handy way, the use case for the ``conan package`` method
   is only testing that the method is correctly coded, but that can also be done with the ``conan export-pkg`` method.
   Thus, as part of the migration to Conan 2.0, the ``conan package`` method will disappear.



Example: export_sources_folder
-------------------------------

If we have this project, intended to create a package for a third-party library which code is located externally:

.. code-block:: text

    ├── conanfile.py
    ├── patches
    │   └── mypatch
    └── CMakeLists.txt


The ``conanfile.py`` would look like this:

.. code-block:: python

      import os
      from conan import ConanFile


      class Pkg(ConanFile):
          name = "pkg"
          version = "0.1"
          exports_sources = "CMakeLists.txt", "patches*"

          def layout(self):
              self.folders.source = "src"
          
          def source(self):
              # we are inside a "src" subfolder, as defined by layout
              # download something, that will be inside the "src" subfolder
              # access to patches and CMakeLists, to apply them, replace files is done with:
              mypatch_path = os.path.join(self.export_sources_folder, "patches/mypatch")
              cmake_path = os.path.join(self.export_sources_folder, "CMakeLists.txt")
              # patching, replacing, happens here

          def build(self):
              # If necessary, the build() method also has access to the export_sources_folder
              # for example if patching happens in build() instead of source()
              cmake_path = os.path.join(self.export_sources_folder, "CMakeLists.txt")


We can see that the ``ConanFile.export_sources_folder`` can provide access to the root folder of the sources:

- Locally it will be the folder where the ``conanfile.py`` lives
- In the cache it will be the "source" folder, that will contain a copy of ``CMakeLists.txt`` and ``patches``,
  while the "source/src" folder will contain the actual downloaded sources.

Example: conanfile in subfolder
-------------------------------

If we have this project, intended to package the code that is in the same repo as the ``conanfile.py``, but
the ``conanfile.py`` is not in the root of the project:

.. code-block:: text

    ├── CMakeLists.txt
    └── conan
        └── conanfile.py


The ``conanfile.py`` would look like this:

.. code-block:: python

      import os
      from conan import ConanFile
      from conan.tools.files import load, copy


      class Pkg(ConanFile):
          name = "pkg"
          version = "0.1"

          def layout(self):
              # The root of the project is one level above
              self.folders.root = ".." 
              # The source of the project (the root CMakeLists.txt) is the source folder
              self.folders.source = "."  
              self.folders.build = "build"
        
          def export_sources(self):
              # The path of the CMakeLists.txt we want to export is one level above
              folder = os.path.join(self.recipe_folder, "..")
              copy(self, "*.txt", folder, self.export_sources_folder)
          
          def source(self):
              # we can see that the CMakeLists.txt is inside the source folder
              cmake = load(self, "CMakeLists.txt")

          def build(self):
              # The build() method can also access the CMakeLists.txt in the source folder
              path = os.path.join(self.source_folder, "CMakeLists.txt")
              cmake = load(self, path)

.. _package_layout_example_multiple_subprojects:

Example: Multiple subprojects
-----------------------------

Lets say that we have a project that contains multiple subprojects, and some of these subprojects need
to access some information that is at their same level (sibling folders). Each subproject would be 
a Conan package.

So we have the following folders and files:

.. code-block:: text

    ├── pkg
    │    ├── conanfile.py
    │    ├── app.cpp  # contains an #include "../common/myheader.h"
    │    └── CMakeLists.txt # contains include(../common/myutils.cmake)
    ├── common
    │    ├── myutils.cmake
    │    └── myheader.h
    └── othersubproject


The ``pkg`` subproject needs to use some of the files located inside the ``common`` folder (that might be
used and shared by other subprojects too), and it references them by their relative location.
Note that ``common`` is not intended to be a Conan package. It is just some common code that will be copied
into the different subproject packages.

We can use the ``self.folders.root = ".."`` layout specifier to locate the root of the project, then
use the ``self.folders.subproject = "subprojectfolder"`` to relocate back most of the layout to the
current subproject folder, as it would be the one containing the build scripts, sources code, etc.,
so other helpers like ``cmake_layout()`` keep working.


.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.cmake import cmake_layout, CMake
    from conan.tools.files import load, copy, save

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeToolchain"

        def layout(self):
            self.folders.root = ".."
            self.folders.subproject = "pkg"
            cmake_layout(self)

        def export_sources(self):
            source_folder = os.path.join(self.recipe_folder, "..")
            copy(self, "*", source_folder, self.export_sources_folder)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            self.run(os.path.join(self.cpp.build.bindirs[0], "myapp"))


Note it is very important the ``export_sources()`` method, that is able to maintain the same relative layout
of the ``pkg`` and ``common`` folders, both in the local developer flow in the current folder, but also
when those sources are copied to the Conan cache, to be built there with ``conan create`` or ``conan install --build=pkg``.
This is one of the design principles of the ``layout()``, the relative location of things must be consistent in the user
folder and in the cache.


Environment variables and configuration
---------------------------------------

There are some packages that might define some environment variables in their
``package_info()`` method via ``self.buildenv_info``, ``self.runenv_info``. Other 
packages can also use ``self.conf_info`` to pass configuration to their consumers.

This is not an issue as long as the value of those environment variables or configuration
do not require using the ``self.package_folder``. If they do, then their values will
not be correct for the "source" and "build" layouts. Something like this will be **broken**
when used in ``editable`` mode:

.. code-block:: python

    import os
    from conan import ConanFile

    class SayConan(ConanFile):
        ...
        def package_info(self):
            # This is BROKEN if we put this package in editable mode
            self.runenv_info.define_path("MYDATA_PATH",
                                         os.path.join(self.package_folder, "my/data/path"))

When the package is in editable mode, for example, ``self.package_folder`` is ``None``, as 
obviously there is no package yet. 
The solution is to define it in the ``layout()`` method, in the same way the ``cpp_info`` can
be defined there:

.. code-block:: python

    from conan import ConanFile

    class SayConan(ConanFile):
        ...
        def layout(self):
            # The final path will be relative to the self.source_folder
            self.layouts.source.buildenv_info.define_path("MYDATA_PATH", "my/source/data/path")
            # The final path will be relative to the self.build_folder
            self.layouts.build.buildenv_info.define_path("MYDATA_PATH2", "my/build/data/path")
            # The final path will be relative to the self.build_folder
            self.layouts.build.conf_info.define_path("MYCONF", "my_conf_folder")


The ``layouts`` object contains ``source``, ``build`` and ``package`` scopes, and each one contains
one instance of ``buildenv_info``, ``runenv_info`` and ``conf_info``.
