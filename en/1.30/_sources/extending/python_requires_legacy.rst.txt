.. _python_requires_legacy:

Python requires (legacy)
========================

.. warning::

    This feature has been superseded by the new :ref:`python_requires`. Even if this is an **experimental**
    feature subject to breaking changes in future releases, this legacy ``python_requires`` syntax has not
    been removed yet, but it will be removed in Conan 2.0.

The ``python_requires()`` feature is a very convenient way to share files and code between
different recipes. A *Python Requires* is just like any other recipe, it is the way it is
required from the consumer what makes the difference.

The *Python Requires* recipe file, besides exporting its own required sources, can export
files to be used by the consumer recipes and also python code in the recipe file itself.

Let's have a look at an example showing all its capabilities (you can find all
the sources in `Conan examples repository`_):

 - Python requires recipe:

    .. code-block:: python

        import os
        import shutil
        from conans import ConanFile, CMake, tools
        from scm_utils import get_version


        class PythonRequires(ConanFile):
            name = "pyreq"
            version = "version"

            exports = "scm_utils.py"
            exports_sources = "CMakeLists.txt"


        def get_conanfile():

            class BaseConanFile(ConanFile):

                settings = "os", "compiler", "build_type", "arch"
                options = {"shared": [True, False]}
                default_options = {"shared": False}
                generators = "cmake"
                exports_sources = "src/*"

                def source(self):
                    # Copy the CMakeLists.txt file exported with the python requires
                    pyreq = self.python_requires["pyreq"]
                    shutil.copy(src=os.path.join(pyreq.exports_sources_folder, "CMakeLists.txt"),
                                dst=self.source_folder)

                    # Rename the project to match the consumer name
                    tools.replace_in_file(os.path.join(self.source_folder, "CMakeLists.txt"),
                                          "add_library(mylibrary ${sources})",
                                          "add_library({} ${{sources}})".format(self.name))


                def build(self):
                    cmake = CMake(self)
                    cmake.configure()
                    cmake.build()

                def package(self):
                    self.copy("*.h", dst="include", src="src")
                    self.copy("*.lib", dst="lib", keep_path=False)
                    self.copy("*.dll", dst="bin", keep_path=False)
                    self.copy("*.dylib*", dst="lib", keep_path=False)
                    self.copy("*.so", dst="lib", keep_path=False)
                    self.copy("*.a", dst="lib", keep_path=False)

                def package_info(self):
                    self.cpp_info.libs = [self.name]

            return BaseConanFile

 - Consumer recipe

    .. code-block:: python

        from conans import ConanFile, python_requires


        base = python_requires("pyreq/version@user/channel")

        class ConsumerConan(base.get_conanfile()):
            name = "consumer"
            version = base.get_version()

            # Everything else is inherited


We must make available for other to use the recipe with the *Python Requires*, this recipe
won't have any associated binaries, only the sources will be needed, so we only need to execute
the export and upload commands:

.. code-block:: bash

    $ conan export . pyreq/version@user/channel
    $ conan upload pyreq/version@user/channel -r=myremote

Now any consumer will be able to reuse the business logic and files available in the recipe,
let's have a look at the most common use cases.


Import a python requires
------------------------

To import a recipe as a *Python requires* it is needed to call the ``python_requires()``
function with the reference as the only parameter:

.. code-block:: python

    base = python_requires("pyreq/version@user/channel")

All the code available in the *conanfile.py* file of the imported recipe will be available
in the consumer through the ``base`` variable.

.. important::

    There are **several important considerations** regarding ``python_requires()``:

    - They are required at every step of the conan commands. If you are creating a package that ``python_requires("MyBase/...")``,
      the ``MyBase`` package should be already available in the local cache or to be downloaded from the remotes. Otherwise, conan
      will raise a "missing package" error.
    - They do not affect the package binary ID (hash). Depending on different version, or different channel of
      such ``python_requires()`` do not change the package IDs as the normal dependencies do.
    - They are imported only once. The python code that is reused is imported only once, the first time it is required.
      Subsequent requirements of that conan recipe will reuse the previously imported module. Global initialization at
      parsing time and global state are discouraged.
    - They are transitive. One recipe using ``python_requires()`` can be also consumed with a ``python_requires()`` from
      another package recipe.
    - They are not automatically updated with the ``--update`` argument from remotes.
    - Different packages can require different versions in their ``python_requires()``. They are private to each recipe,
      so they do not conflict with each other, but it is the responsibility of the user to keep consistency.
    - They are not overridden from downstream consumers. Again, as they are private, they are not affected by other packages,
      even consumers


Reuse python sources
--------------------

In the example proposed we are using two functions through the ``base``
variable: ``base.get_conanfile()`` and ``base.get_version()``. The first one is defined
directly in the *conanfile.py* file, but the second one is in a different source file that
was exported together with the ``pyreq/version@user/channel`` recipe using the
``exports`` attribute.

This works without any Conan magic, it is just plain Python and you can even return a
class from a function and inherit from it. That's just what we are proposing in this
example: all the business logic in contained in the *Python Requires* so every recipe
will reuse it automatically. The consumer only needs to define the ``name`` and ``version``:

.. code-block:: python

    from conans import ConanFile, python_requires


    base = python_requires("pyreq/version@user/channel")

    class ConsumerConan(base.get_conanfile()):
        name = "consumer"
        version = "version"

        # Everything else is inherited

while all the functional code is defined in the *python requires* recipe file:

.. code-block:: python

    from conans import ConanFile, python_requires

    [...]

    def get_conanfile():

        class BaseConanFile(ConanFile):
            def source(self):
                [...]

            def build(self):
                [...]


Reuse source files
------------------

Up to now, we have been reusing python code, but we can also package files within the
*python requires* recipe and consume them afterward, that's what we are doing with a
*CMakeList.txt* file, it will allow us to share the CMake code and ensure that all
the libraries using the same *python requires* will have the same build script. These
are the relevant code snippets from the example files:

 - The *python requires* exports the needed sources (the file exists next to this *conanfile.py*):

    .. code-block:: python


        class PythonRequires(ConanFile):
            name = "pyreq"
            version = "version"

            exports_sources = "CMakeLists.txt"

            [...]

   The file will be exported together with the recipe ``pyreq/version@user/channel``
   during the call to ``conan export . pyreq/version@user/channel`` as it is expected
   for any Conan package.

 - The consumer recipe will copy the file from the *python requires* folder, we need to
   make this copy ourselves, there is nothing run automatically during the
   ``python_requires()`` call:

    .. code-block:: python


        class BaseConanFile(ConanFile):
            [...]

            def source(self):
                # Copy the CMakeLists.txt file exported with the python requires
                pyreq = self.python_requires["pyreq"]
                shutil.copy(src=os.path.join(pyreq.exports_sources_folder, "CMakeLists.txt"),
                            dst=self.source_folder)

                # Rename the project to match the consumer name
                tools.replace_in_file(os.path.join(self.source_folder, "CMakeLists.txt"),
                                      "add_library(mylibrary ${sources})",
                                      "add_library({} ${{sources}})".format(self.name))

   As you can see, in the inherited ``source()`` method, we are copying the *CMakeLists.txt*
   file from the *exports_sources* folder of the python requires (take a look at
   the :ref:`python_requires attribute<python_requires_attribute>`), and modifying a line to
   name the library with the current recipe name.

   In the example, our ``ConsumerConan`` class will also inherit the ``build()``,
   ``package()`` and ``package_info()`` method, turning the actual *conanfile.py* of the
   library into a mere declaration of the name and version.


You can find the full example in the `Conan examples repository`_.

.. _`Conan examples repository`: https://github.com/conan-io/examples/tree/master/features/
