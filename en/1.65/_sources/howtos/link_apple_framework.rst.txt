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

With frameworks we need to use ``self.cpp_info.frameworks`` in a similar manner:

.. code-block:: python

    def package_info(self):

        self.cpp_info.libs = ["SDL2"]

        self.cpp_info.frameworks.extend(["Carbon", "CoreAudio", "Security", "IOKit"])


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

Declare the framework in the ``cpp_info`` object, the
directory of the framework folder (self.package_folder) into the ``cpp_info.frameworkdirs`` and the framework name 
into the ``cpp_info.frameworks``.

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.frameworkdirs.append(self.package_folder)
        self.cpp_info.frameworks.append("MyFramework")
