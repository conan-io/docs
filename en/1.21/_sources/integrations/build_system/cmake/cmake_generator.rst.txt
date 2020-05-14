
``cmake`` generator
===================

If you are using CMake to build your project, you can use the ``cmake`` generator to define all your requirements in CMake syntax.
It creates a file named ``conanbuildinfo.cmake`` that can be imported from your ``CMakeLists.txt``.

.. code-block:: text
   :caption: *conanfile.txt*

   ...
   [generators]
   cmake

When :command:`conan install` is executed, a file named *conanbuildinfo.cmake* is created.

You can include *conanbuildinfo.cmake* in your project's *CMakeLists.txt* to manage your requirements.
The inclusion of *conanbuildinfo.cmake* doesn't alter the CMake environment at all. It simply provides ``CONAN_`` variables and some useful
macros.

Global variables approach
-------------------------

The simplest way to consume it would be to invoke the ``conan_basic_setup()`` macro, which will basically
set global include directories, libraries directories, definitions, etc. so typically it is enough to call:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

    add_executable(timer timer.cpp)
    target_link_libraries(timer ${CONAN_LIBS})

The ``conan_basic_setup()`` is divided into smaller macros that should be self explanatory. If you need to do
something different, you can just call them individually.

.. note::

    This approach makes all dependencies visible to all CMake targets and may also
    increase the build times due to unneeded include and library path components.
    This is particularly relevant if you have multiple targets with different dependencies.
    In that case, you should consider using the :ref:`cmake_targets_approach`.

.. _cmake_targets_approach:

Targets approach
----------------

For **modern cmake (>=3.1.2)**, you can use the following approach:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup(TARGETS)

    add_executable(timer timer.cpp)
    target_link_libraries(timer CONAN_PKG::poco)

Using ``TARGETS`` as argument, ``conan_basic_setup()`` will internally call the macro ``conan_define_targets()``
which defines cmake ``INTERFACE IMPORTED`` targets, one per package. These targets, named ``CONAN_PKG::PackageName`` can be used to link against, instead of using global cmake setup.

.. seealso::

    Check the :ref:`CMake generator<cmake_generator>` section to read more.

.. note::

    The ``CMAKE_MODULE_PATH`` and ``CMAKE_PREFIX_PATH`` contain the paths to the ``self.info.builddirs`` of every required package.
    By default, the root package folder is the only one declared in ``builddirs``. Check :ref:`cpp_info_attributes_reference` for
    more information.
