.. _examples_graph_tool_requires_protobuf:

Using the same requirement as a requires and as a tool_requires
=====================================================================

There are libraries which could behave as a library and as a tool requirement, e.g., `protobuf <https://github.com/conan-io/conan-center-index/tree/master/recipes/protobuf>`__
Those libraries normally contains headers/sources of the library itself, and, perhaps, some extra tools
(compilers, shell scripts, etc.). Both parts are used in different contexts, let's think of this scenario using
*protobuf* for instance:

* I want to create a library which includes a compiled protobuf message. The protobuf compiler (build context)
  needs to be invoked at build time, and the library with the compiled *.pb.cc* file needs to be linked against
  the protobuf library (host context).


Given that, we should be able to use protobuf in build/host context in the same Conan recipe. Basically, your package recipe
should look like:

.. code-block:: python

    def requirements(self):
        self.requires("protobuf/3.18.1")

    def build_requirements(self):
        self.tool_requires("protobuf/3.18.1")


This is the way to proceed with any other library used in both contexts. Nonetheless, let's see a detailed example to see
how the example looks like.

Please, first, clone the sources to recreate this project, you can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: shell

    git clone https://github.com/conan-io/examples2.git
    cd examples2/examples/graph/tool_requires/using_protobuf/myserver


The structure of the project is the following:

.. code-block:: text

    ./
    ├── conanfile.py
    ├── CMakeLists.txt
    ├── addressbook.proto
    ├── apple-arch-armv8
    ├── apple-arch-x86_64
    └── src
       └── myserver.cpp
    └── include
       └── myserver.h
    └── test_package
       ├── conanfile.py
       ├── CMakeLists.txt
       └── src
           └── example.cpp


The ``conanfile.py`` looks like:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import CMake, cmake_layout


    class myserverRecipe(ConanFile):
        name = "myserver"
        version = "1.0"
        package_type = "library"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}
        generators = "CMakeDeps", "CMakeToolchain"
        # Sources are located in the same place as this recipe, copy them to the recipe
        exports_sources = "CMakeLists.txt", "src/*", "include/*", "addressbook.proto"

        def config_options(self):
            if self.settings.os == "Windows":
                self.options.rm_safe("fPIC")

        def configure(self):
            if self.options.shared:
                self.options.rm_safe("fPIC")

        def requirements(self):
            self.requires("protobuf/3.18.1", transitive_headers=True)

        def build_requirements(self):
            self.tool_requires("protobuf/3.18.1")

        def layout(self):
            cmake_layout(self)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            cmake = CMake(self)
            cmake.install()

        def package_info(self):
            self.cpp_info.libs = ["myserver"]
            self.cpp_info.requires = ["protobuf::libprotobuf"]

As you can see, we're using *protobuf* at the same time but in different contexts.
The only difference is that the *requires* is using the ``transitive_headers`` to make it visible downstream, i.e.,
if any other user decides to use my recipe *myserver*.

.. seealso::

    Check the :ref:`requirements traits <reference_conanfile_methods_requirements>`.


The ``CMakeLists.txt`` shows how this example uses protobuf compiler and library:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.15)
    project(myserver LANGUAGES CXX)

    find_package(protobuf CONFIG REQUIRED)

    protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS addressbook.proto)

    add_library(myserver src/myserver.cpp ${PROTO_SRCS})
    target_include_directories(myserver PUBLIC include)

    target_include_directories(myserver PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
      $<INSTALL_INTERFACE:include>
    )

    target_link_libraries(myserver PUBLIC protobuf::libprotobuf)

    set_target_properties(myserver PROPERTIES PUBLIC_HEADER "include/myserver.h;${PROTO_HDRS}")
    install(TARGETS myserver)

To test that everything is working as expected, it includes a *test_package* folder where the *example.cpp* includes the
generated *addressbook.pb.h* header:

.. code-block:: cpp

    #include <iostream>
    #include <fstream>
    #include <string>
    #include "addressbook.pb.h"


    int main(int argc, char* argv[]) {

      GOOGLE_PROTOBUF_VERIFY_VERSION;


      tutorial::AddressBook address_book;
      auto * person = address_book.add_people();
      person->set_id(1337);
      std::cout << "Test(): created a person with id 1337\n";
      // Optional:  Delete all global objects allocated by libprotobuf.
      google::protobuf::ShutdownProtobufLibrary();

      return 0;
    }


So, let's see if it works fine:

.. code-block:: shell

    $ conan create . --build missing
    ...

    Requirements
        myserver/1.0#71305099cc4dc0b08bb532d4f9196ac1:c4e35584cc696eb5dd8370a2a6d920fb2a156438 - Build
        protobuf/3.18.1#ac69396cd9fbb796b5b1fc16473ca354:e60fa1e7fc3000cc7be2a50a507800815e3f45e0#0af7d905b0df3225a3a56243841e041b - Cache
        zlib/1.2.13#13c96f538b52e1600c40b88994de240f:d0599452a426a161e02a297c6e0c5070f99b4909#69b9ece1cce8bc302b69159b4d437acd - Cache
    Build requirements
        protobuf/3.18.1#ac69396cd9fbb796b5b1fc16473ca354:e60fa1e7fc3000cc7be2a50a507800815e3f45e0#0af7d905b0df3225a3a56243841e041b - Cache
    ...

    -- Install configuration: "Release"
    -- Installing: /Users/myuser/.conan2/p/b/myser03f790a5a5533/p/lib/libmyserver.a
    -- Installing: /Users/myuser/.conan2/p/b/myser03f790a5a5533/p/include/myserver.h
    -- Installing: /Users/myuser/.conan2/p/b/myser03f790a5a5533/p/include/addressbook.pb.h

    myserver/1.0: package(): Packaged 2 '.h' files: myserver.h, addressbook.pb.h
    myserver/1.0: package(): Packaged 1 '.a' file: libmyserver.a
    ....

    ======== Testing the package: Executing test ========
    myserver/1.0 (test package): Running test()
    myserver/1.0 (test package): RUN: ./example
    Test(): created a person with id 1337


After seeing it's running OK, let's try to use cross-building. Notice that this part is based on MacOS Intel systems,
and cross-compiling for MacOS ARM ones, but you could use your own profiles depending on your needs for sure.

.. warning::

    MacOS system is required to run this part of the example.


.. code-block:: shell

    $ conan create . --build missing -pr:b apple-arch-x86_64 -pr:h apple-arch-armv8
    ...

    -- Install configuration: "Release"
    -- Installing: /Users/myuser/.conan2/p/b/myser03f790a5a5533/p/lib/libmyserver.a
    -- Installing: /Users/myuser/.conan2/p/b/myser03f790a5a5533/p/include/myserver.h
    -- Installing: /Users/myuser/.conan2/p/b/myser03f790a5a5533/p/include/addressbook.pb.h

    myserver/1.0: package(): Packaged 2 '.h' files: myserver.h, addressbook.pb.h
    myserver/1.0: package(): Packaged 1 '.a' file: libmyserver.a
    ....

    ======== Testing the package: Executing test ========
    myserver/1.0 (test package): Running test()


Now, we cannot see the example running because of the host architecture. If we want to check that the *example* executable
is built for the correct one:

.. code-block:: shell

    $ file test_package/build/apple-clang-13.0-armv8-gnu17-release/example
    test_package/build/apple-clang-13.0-armv8-gnu17-release/example: Mach-O 64-bit executable arm64

Everything works as expected, and the executable was built for 64-bit executable arm64 architectures.
