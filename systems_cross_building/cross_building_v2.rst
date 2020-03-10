.. _cross_building_v2:

Cross building (v2)
===================

.. todo::

    In the section "Package apps and devtools" we are talking about "Creating Conan packages
    to install dev tools" which introduces the `os_build` and `arch_build` settings. We need
    to reorganize all of this.


.. warning::
    This is a quick draft of the new cross building feature.



.. note::
    This docs are a draft to work with the PR https://github.com/conan-io/conan/pull/5594,
    implementation, words here and examples linked will change for sure.


This new implementation of the cross building feature (hope it is the right one, thanks for
reading this an testing anyway) deprecates the old ``os_build`` and ``arch_build`` in favor
of a full profile for the build machine. It has several advantages:

* Profiles for application and libraries in the *build machine* can be different from those
  used to compiled the actual applications and libraries for the *host machine*.
* A full profile is needed by Conan if the packages for the *build machine* are to be generated.
* Recipes for *installers* are no longer different from regular recipes. It means that
  there is no need to divide them into libraries and executables.


Along this document we'll be following an example where we are building an application that
uses CMake from Conan to compile and a couple of dependencies, it will also use a tool in
order to run the tests. This is the graph we are going to reproduce (we use the rectangles
to denote that the package has to be compiled for the *host_machine* and the ellipses
for the *build machine*):


.. graphviz::
    :align: center

    digraph foo {
        rankdir = BT
        
        # Host nodes        
        app [shape=rectangle label = "app"]
        library [shape=rectangle label = "library"]
        zlibh [shape=rectangle label = "zlib"]
        testtool [shape=rectangle label = "testtool"]
        testlib [shape=rectangle label = "testlib"]
        
        # Build nodes
        cmake [shape=ellipse label = "cmake" color=darkgreen fontcolor=darkgreen]
        cmakelib [shape=ellipse label = "cmakelib" color=darkgreen fontcolor=darkgreen]
        zlibb [shape=ellipse label = "zlib" color=darkgreen fontcolor=darkgreen]
        
        
        app -> library -> zlibh
        testtool -> testlib -> zlibh
        app -> testtool [label="BR(host)"]
        
        cmake -> cmakelib -> zlibb
        app -> cmake [label="BR"]
    }


You can find all these recipes in this [this repository](https://github.com/jgsogo/conan-xbuild),
all the packages has the same structure, these are the relevant points:

* Same set of settings, nothing different for executables, tools or libraries:

  .. code-block:: python
    
     settings = "os", "arch", "compiler", "build_type"

* The ``build()`` method add a message with the settings values to be used by the C++ code (very useful
  to know the settings used to compile):

  .. code-block:: python

     def build(self):
         cmake = CMake(self)
         cmake.definitions["MESSAGE:STRING"] = "|".join(map(str, [self.settings.os, self.settings.arch, self.settings.compiler, self.settings.build_type]))
         cmake.configure()
         cmake.build()

* Every package contains a library. ``app``, ``testtool`` and ``cmake`` also contains a executable. libraries
  link to the libraries of the requirements. Executables link to the libraries in their package.

* C++ implementatio is quite simple: there is function and an inline function in every library (useful to check shared builds),
  both of them identifies the library and show the message. Functions call to their requirements too.

  This is the output for the ``cmake_ese`` application compiled with a ``Debug`` profile, for example:

  .. code-block:: bash

     > cmake_exe: Macos|x86_64|apple-clang|Debug
     > cmake_header: Macos|x86_64|apple-clang|Debug
     > cmake: Macos|x86_64|apple-clang|Debug (shared!)
         > cmakelib_header: Macos|x86_64|apple-clang|Debug
         > cmakelib: Macos|x86_64|apple-clang|Debug (shared!)
             > zlib_header: Macos|x86_64|apple-clang|Debug
             > zlib: Macos|x86_64|apple-clang|Debug shared!

  Note the cascade calls and the ``shared`` flag that is printed from the libraries.


User interface
--------------

Command line
++++++++++++

In order to start using the new cross-building feature you need to provide a profile for the *build_machine* too, so every
command now accepts the arguments ``--profile:host`` (``-pr:h``) and ``--profile:build`` (``-pr:b``). The old argument
``--profile`` (``-p``) can still be used and it will be assigned to the profile for the *host machine*.

Other command line options like ``--settings``, ``--options`` and ``--env`` have been unfolded as well and
should be assigned to the matching profile.

For example, given the recipes in the [repository mentioned above](https://github.com/jgsogo/conan-xbuild), after
exporting the recipe, the following command will generate our ``app`` for the ``profile_host`` using some tools
like ``cmake`` built with the ``profile_build``:

.. code-block:: bash

   conan conan install app/0.1@user/testing --build --profile:host=profiles/profile_host --profile:build=profiles/profile_build


Context switch
++++++++++++++

By default, this new cross building implementation, will consider all the ``build_requires`` as tools that need to be available
in the *build machine* so Conan will compile them using the corresponding profile. In our graph above, those are the ``cmake``
branch according to the ``app`` recipe:

.. code-block:: python

    class app(ConanFile):
        name = "app"
        version = "0.1"
        settings = "os", "arch", "compiler", "build_type"
        options = {"shared": [True, False]}
        default_options = {"shared": False}
        exports = "*"

        
        generators = "cmake", "cmake_find_package"

        def requirements(self):
            self.requires("library/0.1@user/testing")

        def build_requirements(self):
            self.build_requires("cmake/0.1@user/testing")
            self.build_requires("testtool/0.1@user/testing", force_host_context=True)
            

Note that the *default* ``build_requires`` declaration for ``cmake`` has nothing special, while the declaration for a tool
that has to be deployed to the *host machine* needs to be stated: ``force_host_context=True``.

.. warning::

   Defaulting the ``build_requires`` to the *build machine* is the most important change here.
