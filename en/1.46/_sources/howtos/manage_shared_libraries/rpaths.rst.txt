Manage RPATHs
=============

The **rpath** is encoded inside dynamic libraries and executables and helps the linker to find its
required shared libraries.

If we have an executable, **my_exe**, that requires a shared library, **shared_lib_1**,
and **shared_lib_1**, in turn, requires another **shared_lib_2**.

So the **rpaths** values are:

+--------------+-----------------------+
| File         | rpath                 |
+==============+=======================+
| my_exe       | /path/to/shared_lib_1 |
+--------------+-----------------------+
| shared_lib_1 | /path/to/shared_lib_2 |
+--------------+-----------------------+
| shared_lib_2 |                       |
+--------------+-----------------------+

In **Linux** if the linker doesn't find the library in **rpath**, it will continue the search in
**system defaults paths** (LD_LIBRARY_PATH... etc)
In OSX, if the linker detects an invalid **rpath** (the file does not exist there), it will fail.

Default Conan approach
----------------------

The consumer project of dependencies with shared libraries needs to import them to the executable
directory to be able to run it:

**conanfile.txt**

.. code-block:: text

    [requires]
    poco/1.9.4

    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder

On **Windows** this approach works well, importing the shared library to the directory containing
your executable is a very common procedure.

On **Linux** there is an additional problem, the dynamic linker doesn't look by default in the
executable directory, and you will need to adjust the `LD_LIBRARY_PATH` environment variable like this:


.. code-block:: bash

    LD_LIBRARY_PATH=$(pwd) && ./mybin

On **OSX** if absolute rpaths are hardcoded in an executable or
shared library and they don't exist the executable will fail to run. This is the most common problem when
we reuse packages in a different environment from where the artifacts have been generated.

So for **OSX**, Conan, by default, when you build your library with **CMake**, the rpaths will be
generated without any path:

+--------------------+--------------------+
| File               | rpath              |
+====================+====================+
| my_exe             | shared_lib_1.dylib |
+--------------------+--------------------+
| shared_lib_1.dylib | shared_lib_2.dylib |
+--------------------+--------------------+
| shared_lib_2.dylib |                    |
+--------------------+--------------------+

The ``conan_basic_setup()`` macro will set the ``set(CMAKE_SKIP_RPATH 1)`` in OSX.

You can skip this default behavior by passing the ``KEEP_RPATHS`` parameter to the ``conan_basic_setup`` macro:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup(KEEP_RPATHS)

    add_executable(timer timer.cpp)
    target_link_libraries(timer ${CONAN_LIBS})


If you are using ``autotools`` Conan won't auto-adjust the rpaths behavior. if you want to follow this
default behavior you will probably need to replace the ``install_name`` in the **configure** or **MakeFile**
generated files in your recipe to not use $rpath:

.. code-block:: python


    replace_in_file("./configure", r"-install_name \$rpath/", "-install_name ")


Different approaches
--------------------

You can adjust the **rpaths** in the way that adapts better to your needs.

If you are using ``CMake`` take a look to the `CMake RPATH handling`_ guide.

Remember to pass the ``KEEP_RPATHS`` variable to the ``conan_basic_setup``:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup(KEEP_RPATHS)

Then, you could, for example, use the ``@executable_path`` in OSX and ``$ORIGIN`` in Linux  to adjust a relative path from the executable.
Also, enabling `CMAKE_BUILD_WITH_INSTALL_RPATH`_ will build the application with the RPATH value of ``CMAKE_INSTALL_RPATH`` and avoid
the need to be relinked when installed.

.. code-block:: cmake

    if (APPLE)
        set(CMAKE_INSTALL_RPATH "@executable_path/../lib")
    else()
        set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
    endif()

    set(CMAKE_BUILD_WITH_INSTALL_RPATH ON)

You can use this imports statements in the consumer project:

.. code-block:: text

    [requires]
    poco/1.9.4

    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
    lib, *.dylib* -> ./lib # Copies all dylib files from packages lib folder to my "lib" folder
    lib, *.so* -> ./lib # Copies all so files from packages lib folder to my "lib" folder

And your final application can follow this layout:


.. code-block:: text

  bin
   |_____ my_executable
   |_____ mylib.dll
   |
  lib
   |_____ libmylib.so
   |_____ libmylib.dylib


You could move the entire application folder to any location and the shared libraries will be located
correctly.

.. _`CMake RPATH handling`: https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/RPATH-handling
.. _`CMAKE_BUILD_WITH_INSTALL_RPATH`: https://cmake.org/cmake/help/v3.0/variable/CMAKE_BUILD_WITH_INSTALL_RPATH.html
