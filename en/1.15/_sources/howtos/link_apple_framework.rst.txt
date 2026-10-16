.. _link_apple_framework:

How to link with Apple Frameworks
=================================

It is common in MacOS that your Conan package needs to link with a complete Apple framework,
and, of course, you want to propagate this information to all projects/libraries that use your package.

With regular libraries, use ``self.cpp_info.libs`` object to append to it all the libraries:

.. code-block:: python

    def package_info(self):

        self.cpp_info.libs = ["SDL2"]
        self.cpp_info.libs.append("OpenGL32")

With frameworks we need to declare the "-framework flag" as a linker flag:

.. code-block:: python

    def package_info(self):

        self.cpp_info.libs = ["SDL2"]

        self.cpp_info.exelinkflags.append("-framework Carbon")
        self.cpp_info.exelinkflags.append("-framework CoreAudio")
        self.cpp_info.exelinkflags.append("-framework Security")
        self.cpp_info.exelinkflags.append("-framework IOKit")

        self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags

In the previous example we are using ``self.cpp_info.exelinkflags``. If we are using CMake to consume this package, it will only link those
frameworks if we are building an executable and ``sharedlinkflags`` will only apply if we are building a shared library.

If we are not using CMake to consume this package ``sharedlinkflags`` and ``exelinkflags`` are used indistinctly.
In the example above, in the last line we are assigning ``sharedlinkflags`` with ``exelinkflags``, so no matter what the consumer will build,
it will indicate to the linker to link with the specified frameworks.


.. _package_apple_framework:


How to package Apple Frameworks
===============================

To package a **MyFramework** Apple framework, copy/create a folder
``MyFramework.framework`` to your package folder, where you should put all the subdirectories
(``Headers``, ``Modules``, etc).

.. code-block:: python

    def package(self):
        # If you have the framework folder built in your build_folder:
        self.copy("MyFramework.framework/*", symlinks=True)
        # Or build the destination folder:
        tools.mkdir("MyFramework.framework/Headers")
        self.copy("*.h", dst="MyFramework.framework/Headers")
        # ...

Declare the framework in the ``cpp_info`` object, pass a compiler flag ``-F`` with the
directory of the framework folder (self.package_folder) and linker flags with the ``-F`` and ``-framework`` with
the framework name.

.. code-block:: python

    def package_info(self):
        ...
        # Note that -F flags are not automatically adjusted in "cmake"
        # generator so it will be needed to declare its path like this:
        # self.cpp_info.exelinkflags.append("-F path/to/the/framework -framework MyFramework")

        f_location = '-F "%s"' % self.package_folder
        self.cpp_info.cflags.append(f_location) # or cpp_info.cppflags if cpp library
        self.cpp_info.sharedlinkflags.extend([f_location, "-framework MyFramework"])
        self.cpp_info.exelinkflags = self.cpp_info.sharedlinkflags
