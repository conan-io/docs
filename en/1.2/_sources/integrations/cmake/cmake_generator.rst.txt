
``cmake`` generator
===================

If you are using **CMake** to build your project, you can use the ``cmake`` generator to define all your requirements information in cmake syntax.
It creates a file named ``conanbuildinfo.cmake`` that can be imported from your ``CMakeLists.txt``.


**conanfile.txt**

.. code-block:: text

   ...

   [generators]
   cmake


When **conan install** is executed, a file named ``conanbuildinfo.cmake`` is created.

We can include ``conanbuildinfo.cmake`` in our project's ``CMakeLists.txt`` to manage our requirements.
The inclusion of ``conanbuildinfo.cmake`` doesn't alter cmake environment at all, it just provides ``CONAN_`` variables and some useful macros.


Global variables approach
-------------------------------

The simplest way to consume it would be to invoke the ``conan_basic_setup()`` macro, which will basically
set global include directories, libraries directories, definitions, etc. so typically is enough to do:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

    add_executable(timer timer.cpp)
    target_link_libraries(timer ${CONAN_LIBS})

The ``conan_basic_setup()`` is split in smaller macros, that should be self explanatory. If you need to do
something different, you can just use them individually.


Targets approach
-------------------------------

For **modern cmake (>=3.1.2)**, you can use the following approach:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup(TARGETS)

    add_executable(timer timer.cpp)
    target_link_libraries(timer CONAN_PKG::Poco)
    
Using ``TARGETS`` as argument, ``conan_basic_setup()`` will internally call the macro ``conan_define_targets()``
which defines cmake ``INTERFACE IMPORTED`` targets, one per package. These targets, named ``CONAN_PKG::PackageName`` can be used to link with, instead of using global cmake setup.


.. seealso:: Check the section :ref:`Reference/Generators/cmake <cmake_generator>` to read more about this generator.

