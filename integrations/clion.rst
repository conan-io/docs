.. _clion:


|clion_logo| CLion
____________________




CLion uses **CMake** as the build system of projects, so you can use the :ref:`CMake generator<cmake>` to manage your requirements in your CLion project.

Just include the ``conanbuildinfo.cmake`` this way:

.. code-block:: cmake

   if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/build/conanbuildinfo.cmake) #Clion, with conanbuildinfo.cmake in build folder
       include(${CMAKE_CURRENT_SOURCE_DIR}/build/conanbuildinfo.cmake)
   else()
       include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake) # Not CLion
   endif()
   
   
.. note::
   In the example above we generated the ``conanbuildinfo.cmake`` in the **build** folder running: "conan install --file ../conanfile.txt" in that folder.
   You can use other directory or project root if you want, just change the route in CMakeLists include of ``conanbuildinfo.cmake`` file.



.. |clion_logo| image:: ../images/icon_CLion.png
