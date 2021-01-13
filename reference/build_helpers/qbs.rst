.. _qbs_build_reference:

Qbs
===

If you are using **Qbs** as your build system, you can use the **Qbs** build helper.

.. code-block:: python

    from conans import ConanFile, tools, Qbs
    import os

    class ConanFileToolsTest(ConanFile):
        ...

        def build(self):
            qbs = Qbs(self)
            qbs.build()

Constructor
-----------

.. code-block:: python

    class Qbs(object):

        def __init__(self, conanfile, project_file=None)

Parameters:
    - **conanfile** (Required): Use ``self`` inside a ``conanfile.py``.
    - **project_file** (Optional, Defaulted to ``None``): Path to the root project file.

Attributes
----------

use_toolchain_profile
+++++++++++++++++++++

**Defaulted to**: ``conan_toolchain_profile``

Specifies the qbs profile to build the project for.

jobs
++++

**Defaulted to**: ``tools.cpu_count()``

Specifies the number of concurrent build jobs.

Methods
-------

add_configuration()
+++++++++++++++++++

.. code-block:: python

    def add_configuration(self, name, values)

Add a build configuration to use.

Parameters:
    - **name** (Required): Specifies build configuration name.
    - **values** (Required): A dict of properties set for this build configuration.


build()
+++++++

.. code-block:: python

    def build(self, products=None)

Build Qbs project.

Parameters:
    - **products** (Optional, Defaulted to ``None``): Specifies a list of products to build. If ``None`` build all products which have the qbs property ``buildByDefault`` set to ``true``.


build_all()
+++++++++++

.. code-block:: python

    def build_all(self)

Build all products of Qbs project, even products which set the qbs property ``buildByDefault`` set to ``false``


install()
+++++++++

.. code-block:: python

    def install(self)

Install products.


Example
-------

A typical usage of the Qbs build helper, if you want to be able to both execute :command:`conan create` and also build your package for a
library locally (in your user folder, not in the local cache), could be:

.. code-block:: python

    from conans import ConanFile, Qbs

    class HelloConan(ConanFile):
        name = "hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        generators = "qbs"
        exports_sources = "src/*", "*.qbs"
        no_copy_source = True
        requires = "zlib/1.2.11"

        def build(self):
            qbs = Qbs(self)
            qbs.add_configuration("default", {
                "project.Hello.conanBuildInfo", self.build_folder + "/conanbuildinfo.qbs"
            })
            qbs.build()

        def package(self):
            self.copy("*.h", dst="include", src="src")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["hello"]

Note the ``qbs`` generator, which generates the *conanbuildinfo.qbs* file, to process
dependencies information. Setting ``no_copy_source = True`` helps qbs to pick the right project file
and not get confused by the generated files.

The *hello.qbs* could be as simple as:

.. code-block:: text

    Project {
        readonly property path conanBuildInfo

        references: conanBuildInfo

        DynamicLibrary {
            name: "hello"
            version: "0.1.0"
            files: "src/hello.cpp"
            cpp.cxxLanguageVersion: "c++11"

            Depends { name: "cpp" }
            Depends { name: "zlib" }
        }
    }
