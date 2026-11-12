.. _cmakemulti_generator:


`cmake_multi`
==============

.. container:: out_reference_box

    This is the reference page for ``cmake_multi`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.

Usage
-----

.. code-block:: bash

    $ conan install -g cmake_multi -s build_type=Release ...
    $ conan install -g cmake_multi -s build_type=Debug ...

These commands will generate 3 files:

- ``conanbuildinfo_release.cmake``: Variables adjusted only for build_type Release
- ``conanbuildinfo_debug.cmake``: Variables adjusted only for build_type Debug
- ``conanbuildinfo_multi.cmake``: Which includes the other two, and enables its use

Variables in conanbuildinfo_release.cmake
-----------------------------------------

Same as :ref:`conanbuildinfo.cmake<conanbuildinfocmake_variables>` with suffix ``_RELEASE``


Variables in conanbuildinfo_debug.cmake
---------------------------------------

Same as :ref:`conanbuildinfo.cmake<conanbuildinfocmake_variables>` with suffix ``_DEBUG``


Available Methods
-----------------

Same as :ref:`conanbuildinfo.cmake<conanbuildinfocmake_methods>`
