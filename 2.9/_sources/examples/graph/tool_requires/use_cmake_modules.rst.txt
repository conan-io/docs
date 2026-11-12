Use cmake modules inside a ``tool_requires`` transparently
==========================================================

When we want to reuse some ``.cmake`` scripts that are inside another Conan package
there are several possible different scenarios, like if the ``.cmake`` scripts are inside
a regular ``requires`` or a ``tool_requires``.

Also, it is possible to want 2 different approaches:

- The consumer of the scripts can do a explicit ``include(MyScript)`` in their CMakeLists.txt. This approach is nicely explicit and simpler to setup, just define ``self.cpp_info.builddirs`` in the recipe, and consumers with ``CMakeToolchain`` will automatically be able to do the ``include()`` and use the functionality. See the :ref:`example here<consume_cmake_macro>` 
- The consumer wants to have the dependency cmake modules automatically loaded when the ``find_package()`` is executed. This current example implements this case.


Let's say that we have a package, intended to be used as a ``tool_require``, with the following recipe:

.. code-block:: python
    :caption: myfunctions/conanfile.py

    import os
    from conan import ConanFile
    from conan.tools.files import copy

    class Conan(ConanFile):
        name = "myfunctions"
        version = "1.0"
        exports_sources = ["*.cmake"]

        def package(self):
            copy(self, "*.cmake", self.source_folder, self.package_folder)

        def package_info(self):
            self.cpp_info.set_property("cmake_build_modules", ["myfunction.cmake"])

And a ``myfunction.cmake`` file in:

.. code-block:: cmake
    :caption: myfunctions/myfunction.cmake

    function(myfunction)
        message("Hello myfunction!!!!")
    endfunction()

We can do a ``cd myfunctions && conan create .`` which will create the ``myfunctions/1.0`` package containing the cmake script.

Then, a consumer package will look like:

.. code-block:: python
    :caption: consumer/conanfile.py

    from conan import ConanFile
    from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
    
    class Conan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        tool_requires = "myfunctions/1.0"

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()

            deps = CMakeDeps(self)
            # By default 'myfunctions-config.cmake' is not created for tool_requires
            # we need to explicitly activate it
            deps.build_context_activated = ["myfunctions"]
            # and we need to tell to automatically load 'myfunctions' modules
            deps.build_context_build_modules = ["myfunctions"]
            deps.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()

And a ``CMakeLists.txt`` like:

.. code-block:: cmake
    :caption: consumer/CMakeLists.txt

    cmake_minimum_required(VERSION 3.0)
    project(test)
    find_package(myfunctions CONFIG REQUIRED)
    myfunction()


Then, the consumer will be able to automatically call the ``myfunction()`` from the dependency module:

.. code-block:: bash

    $ conan build .
    ...
    Hello myfunction!!!!

If for some reason the consumer wants to force the usage from the ``tool_requires()`` as a CMake module, the consumer could do ``deps.set_property("myfunctions", "cmake_find_mode", "module", build_context=True)``, and then ``find_package(myfunctions MODULE REQUIRED)`` will work.
