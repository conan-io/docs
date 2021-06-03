.. _conan_tools_layout:

conan.tools.layout
==================

Available since: `1.37.0 <https://github.com/conan-io/conan/releases>`_

LayoutPackager
--------------

The ``LayoutPackager`` together with the :ref:`package layouts<package_layout>`
feature, allow to automatically package the files following the declared
information in the ``layout()`` method:

Usage:

.. code:: python

        from conans import ConanFile
        from conan.tools.layout import LayoutPackager

        class Pkg(ConanFile):

            def layout(self):
                ...

            def package(self):
                LayoutPackager(self).package()


It works by going through all the directories under ``self.cpp.source`` and
``self.cpp.build`` and copying files which match the patterns to the associated
destination directories under ``self.cpp.package``. The ``LayoutPackager`` has a
lot of assumptions baked in as defaults, which provides a lot of automatic
behavior for convenience. However, let's provide an example to show what it will
actually do. 

Here, we'll show a fully-declared ``layout`` method, to be packaged using the
``LayoutPackager`` class. Then, we'll show the equivalent ``self.copy()``
statements that one would write in the ``package()`` method.

Here is the fully-declared ``layout`` method:

.. code:: python

        def layout(self):
        
            # Declaring the roots of source and build directories
            # Used during package(), and when making packages editable
            self.folders.source = "src"
            self.folders.build = "build"

            # Declaring the layout of source and build directories
            # Used during package(), and when making packages editable
            self.cpp.source.includedirs = ["include"]
            self.cpp.build.libdirs = ["build_subdir"]
            self.cpp.build.bindirs = ["build_subdir"]
            
            # Declaring the patterns for files to-be-packaged
            # Only used when copying files during package()
            self.patterns.source.include = ["*.hpp"]
            self.patterns.build.lib = ["*.lib"]
            self.patterns.build.bin = ["*.dll"]


            # Declaring the destination directories for the final package
            # Only used when copying files during package()
            self.cpp.package.includedirs = ["include"]
            self.cpp.package.libdirs = ["lib"]
            self.cpp.package.bindirs = ["bin"]
            
        def package(self):
                LayoutPackager(self).package()
   
Here is the equivalent `package()` method:

.. code:: python
                
        def package(self):
            self.copy("*.hpp", src="src/include", dst="include")
            self.copy("*.lib", src="build/build_subdir", dst="lib")
            self.copy("*.dll", src="build/build_subdir", dst="bin")


In the example above, we defined explicit values for the directories and
patterns for illustration purposes. However, the many of the directories and
patterns have default values. So, here we show the equivalent `self.copy()`
statements for the case where ``LayoutPackager.package()`` is used with the
default values of `self.cpp` and `self.patterns`. 

.. code:: python

            def package(self):
                self.copy("*.h", src="include", dst="include")
                self.copy("*.hpp", src=include", dst="include")
                self.copy("*.hxx", src="include", dst="include")
                self.copy("*.a", src=".", dst="lib")
                self.copy("*.so", src=".", dst="lib")
                self.copy("*.so.*", src=".", dst="lib")
                self.copy("*.lib", src=".", dst="lib")
                self.copy("*.dylib", src=".", dst="lib")
                self.copy("*.dll", src=".", dst="bin")
                self.copy("*.exe", src=".", dst="bin")
