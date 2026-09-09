.. _creating_packages_package_method:

Package files: the package() method
===================================

We already used the ``package()`` method in our `hello` package to invoke CMake's install
step. In this tutorial, we will explain the use of the :ref:`CMake.install()
<conan_tools_cmake_helper>` in more detail and also how to modify this method to do things
like:

- Using :ref:`conan.tools.files <conan_tools_files>` utilities to copy the generated
  artifacts from the build folder to the package folder
- Copying package licenses
- Manage how to package symlinks

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/package_method


Using CMake install step in the package() method
------------------------------------------------

This is the simplest choice when you have already defined in your `CMakeLists.txt` the
functionality of extracting the artifacts (headers, libraries, binaries) from the build
and source folder to a predetermined place and maybe do some post-processing of those
artifacts. This will work without changes in your `CMakeLists.txt` because Conan will set
the ``CMAKE_INSTALL_PREFIX`` CMake variable to point to the recipe's :ref:`package_folder
<conan_conanfile_properties_package_folder>` attribute. Then, just calling `install()` in
the `CMakeLists.txt` over the created target is enough for Conan to move the built
artifacts to the correct location in the Conan local cache.

.. code-block:: text
    :caption: *CMakeLists.txt*
    :emphasize-lines: 10

    cmake_minimum_required(VERSION 3.15)
    project(hello CXX)

    add_library(hello src/hello.cpp)
    target_include_directories(hello PUBLIC include)
    set_target_properties(hello PROPERTIES PUBLIC_HEADER "include/hello.h")

    ...

    install(TARGETS hello)

.. code-block:: python
    :caption: *conanfile.py*
    :emphasize-lines: 3

    def package(self):
        cmake = CMake(self)
        cmake.install()

Let's build our package again and pay attention to the lines regarding the
packaging of files in the Conan local cache:

.. code-block:: bash
    :emphasize-lines: 7-14

    $ conan create . --build=missing -tf=""
    ...
    hello/1.0: Build folder /Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/b/build/Release
    hello/1.0: Generated conaninfo.txt
    hello/1.0: Generating the package
    hello/1.0: Temporary package folder /Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/p
    hello/1.0: Calling package()
    hello/1.0: CMake command: cmake --install "/Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/b/build/Release" --prefix "/Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/p"
    hello/1.0: RUN: cmake --install "/Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/b/build/Release" --prefix "/Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/p"
    -- Install configuration: "Release"
    -- Installing: /Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/p/lib/libhello.a
    -- Installing: /Users/user/.conan2/p/tmp/b5857f2e70d1b2fd/p/include/hello.h
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello.a
    hello/1.0: Package 'fd7c4113dad406f7d8211b3470c16627b54ff3af' created
    hello/1.0: Created package revision bf7f5b9a3bb2c957742be4be216dfcbb
    hello/1.0: Full package reference: hello/1.0#25e0b5c00ae41ef9fbfbbb1e5ac86e1e:fd7c4113dad406f7d8211b3470c16627b54ff3af#bf7f5b9a3bb2c957742be4be216dfcbb
    hello/1.0: Package folder /Users/user/.conan2/p/47b4c4c61c8616e5/p

As you can see both the *include* and *library* files were copied to the package folder after
calling to the ``cmake.install()`` method.


Use conan.tools.files.copy() in the package() method and packaging licenses
---------------------------------------------------------------------------

For the cases that you don't want to rely on CMake's install functionality or that you are
using another build-system, Conan provides the tools to copy the selected files to the
:ref:`package_folder <conan_conanfile_properties_package_folder>`. In this case, you can
use the :ref:`tools.files.copy <conan_tools_files_copy>` function to make that copy. We
can replace the previous ``cmake.install()`` step with a custom copy of the files and the
result would be the same.

Note that we are also packaging the ``LICENSE`` file from the library sources in the
*licenses* folder. This is a common pattern in Conan packages and could also be added to
the previous example using ``cmake.install()`` as the *CMakeLists.txt* will not copy this
file to the *package folder*.

.. code-block:: python
    :caption: *conanfile.py*

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "include"), dst=os.path.join(self.package_folder, "include"))
        copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, pattern="*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

Let's build our package one more time and pay attention to the lines regarding the
packaging of files in the Conan local cache:

.. code-block:: bash
    :emphasize-lines: 7-13

    $ conan create . --build=missing -tf=""
    ...
    hello/1.0: Build folder /Users/user/.conan2/p/tmp/222db0532bba7cbc/b/build/Release
    hello/1.0: Generated conaninfo.txt
    hello/1.0: Generating the package
    hello/1.0: Temporary package folder /Users/user/.conan2/p/tmp/222db0532bba7cbc/p
    hello/1.0: Calling package()
    hello/1.0: Copied 1 file: LICENSE
    hello/1.0: Copied 1 '.h' file: hello.h
    hello/1.0: Copied 1 '.a' file: libhello.a
    hello/1.0 package(): Packaged 1 file: LICENSE
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello.a
    hello/1.0: Package 'fd7c4113dad406f7d8211b3470c16627b54ff3af' created
    hello/1.0: Created package revision 50f91e204d09b64b24b29df3b87a2f3a
    hello/1.0: Full package reference: hello/1.0#96ed9fb1f78bc96708b1abf4841523b0:fd7c4113dad406f7d8211b3470c16627b54ff3af#50f91e204d09b64b24b29df3b87a2f3a
    hello/1.0: Package folder /Users/user/.conan2/p/21ec37b931782de8/p

Check how the *include* and *library* files are packaged. The LICENSE file is also copied
as we explained above.

Managing symlinks in the package() method
-----------------------------------------

Another thing you can do in the package method is managing how to package symlinks. Conan
won’t manipulate symlinks by default, so we provide several :ref:`tools
<conan_tools_files_symlinks>` to convert absolute symlinks to relative ones and removing
external or broken symlinks.

Imagine that some of the files packaged in the latest example were symlinks that point to
an absolute location inside the Conan cache. Then, calling to
``conan.tools.files.symlinks.absolute_to_relative_symlinks()`` would convert those
absolute links into relative paths and make the package relocatable.


.. code-block:: python
    :caption: *conanfile.py*

    from conan.tools.files.symlinks import absolute_to_relative_symlinks

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "include"), dst=os.path.join(self.package_folder, "include"))
        copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        ...

        absolute_to_relative_symlinks(self, self.package_folder)


Read more
---------

- ...

.. seealso::

    - :ref:`package() method reference<reference_conanfile_methods_package>`
