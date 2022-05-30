.. _conan-qbs-toolchain:

conan.tools.qbs
===============

QbsProfile
------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

Available since: `1.33.0 <https://github.com/conan-io/conan/releases/tag/1.33.0>`_

The ``QbsProfile`` can be used in the ``generate()`` method:


.. code:: python

    from conan import ConanFile
    from conan.tools.qbs import QbsProfile

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        options = {"shared": [True, False]}
        default_options = {"shared": False}

        def generate(self):
            tc = QbsProfile(self)
            tc.generate()


The ``QbsProfile`` will generate the following file during :command:`conan install`
command (or before calling the ``build()`` method when the package is being
built in the cache): *conan_toolchain_profile.qbs*. This file will contain a qbs profile
named *conan_toolchain_profile*.


*conan_toolchain_profile.qbs* will contain the definitions of all the Qbs properties
related to the Conan options and settings for the current package, platform,
etc. This includes the following:

  * Detection of compiler.

  * Based on the compiler set in environment variable ``CC``.

  * Uses detected system compiler based on Conan setting ``compiler`` if environment variable ``CC`` is not set.

* Detection of compiler flags from environment (as defined at https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html):

  * ``ASFLAGS``

  * ``CFLAGS``

  * ``CPPFLAGS``

  * ``CXXFLAGS``

  * ``LDFLAGS``

* Detection of sysroot from environment.

* Detection of ``build_type`` from Conan settings.

* Detection of ``arch`` from Conan settings.

* Detection of ``compiler.cxxstd`` from Conan settings.

* Detection of ``fPIC`` based on the existence of such option in the recipe.


Qbs
---

If you are using **Qbs** as your build system, you can use the **Qbs** build helper.

.. code-block:: python

    from conan import ConanFile
    from conan.tools.qbs import Qbs

    class ConanFileToolsTest(ConanFile):
        ...

        def build(self):
            qbs = Qbs(self)
            qbs.build()

Constructor
+++++++++++

.. code-block:: python

    class Qbs(object):

        def __init__(self, conanfile, project_file=None)

Parameters:
    - **conanfile** (Required): Use ``self`` inside a ``conanfile.py``.
    - **project_file** (Optional, Defaulted to ``None``): Path to the root project file.

Attributes
++++++++++

profile
*********************

**Defaulted to**: ``conan_toolchain_profile``

Specifies the qbs profile to build the project for.


Methods
+++++++

add_configuration()
*********************

.. code-block:: python

    def add_configuration(self, name, values)

Add a build configuration to use.

Parameters:
    - **name** (Required): Specifies build configuration name.
    - **values** (Required): A dict of properties set for this build configuration.


build()
*******

.. code-block:: python

    def build(self, products=None)

Build Qbs project.

Parameters:
    - **products** (Optional, Defaulted to ``None``): Specifies a list of products to build. If ``None`` build all products which have the qbs property ``buildByDefault`` set to ``true``.


build_all()
***********

.. code-block:: python

    def build_all(self)

Build all products of Qbs project, even products which set the qbs property ``buildByDefault`` set to ``false``


install()
*********

.. code-block:: python

    def install(self)

Install products.


Example
*******

A typical usage of the Qbs build helper, if you want to be able to both execute :command:`conan create` and also build your package for a
library locally (in your user folder, not in the local cache), could be:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.qbs import Qbs


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
                "project.conanBuildInfo", self.build_folder + "/conanbuildinfo.qbs"
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
