.. _python_requires:

Python requires: reusing code [EXPERIMENTAL]
============================================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The ``python_requires()`` feature is a very convenient way to share files and code between
different recipes. A *Python Requires* is just like any another recipe, it is the way it is
required from the consumer what makes the difference.

The *Python Requires* recipe file, besides exporting its own required sources, can export
files to be used by the consumer recipes and also python code in the recipe file itself.

Let's have a look at an example showing all its capabilities (you can find all
the sources in ....):

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
                default_options = "shared=False"
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

To import a recipe as a *Python requires* it is needed to call the `python_requires()``
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
we have exported together with the ``pyreq/version@user/channel`` recipe using the
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


You can find the full example in th


The ``python_requires()`` feature allows to extend the recipes reusing code from other **conanfile.py** easily, even for inheritance
approaches. The code to be reused will be in a *conanfile.py* recipe, and will be managed as any other Conan package.

Let's create for example some reusable base class:

.. code-block:: python

    from conans import ConanFile

    class MyBase(ConanFile):
        def source(self):
            self.output.info("My cool source!")
        def build(self):
            self.output.info("My cool build!")
        def package(self):
            self.output.info("My cool package!")
        def package_info(self):
            self.output.info("My cool package_info!")

With this conanfile, we can export it to the local cache to make it available, and also upload to our remote:

.. code-block:: bash

    $ conan export . MyBase/0.1@user/channel
    $ conan upload MyBase/0.1@user/channel -r=myremote

It is not necessary to "create" any package binaries, or to ``upload --all``, because there are no binaries for this recipe.

Now, using the ``python_requires()`` we can write a new package recipe like:

.. code-block:: python

    from conans import python_requires

    base = python_requires("MyBase/0.1@user/channel")

    class PkgTest(base.MyBase):
        pass

If we run a ``conan create``, of this recipe, we can see how it is effectively reusing the above code:

.. code-block:: bash

    $ conan create . Pkg/0.1@user/channel

    Pkg/0.1@lasote/testing: Installing package
    Requirements
        Pkg/0.1@lasote/testing from local cache - Cache
    Python requires
        MyConanfileBase/1.1@lasote/testing
    Packages
        Pkg/0.1@lasote/testing:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Build
    ...
    Pkg/0.1@lasote/testing: Configuring sources
    Pkg/0.1@lasote/testing: My cool source!
    ...
    Pkg/0.1@lasote/testing: Calling build()
    Pkg/0.1@lasote/testing: My cool build!
    ...
    Pkg/0.1@lasote/testing: Calling package()
    Pkg/0.1@lasote/testing: My cool package!
    ...
    Pkg/0.1@lasote/testing: My cool package_info!


It is not compulsory to extend the reused ``MyBase`` class, it is possible to reuse just functions too:

.. code-block:: python

    from conans import ConanFile

    def my_build(settings):
        # doing custom stuff based on settings

    class MyBase(ConanFile):
        pass

.. code-block:: bash

    $ conan export . MyBuild/0.1@user/channel
    $ conan upload MyBuild/0.1@user/channel -r=myremote

.. code-block:: python

    from conans import ConanFile, python_requires

    base = python_requires("MyBuild/0.1@user/channel")

    class PkgTest(ConanFile):
        ...
        def build(self):
            base.my_build(self.settings)


Version ranges are possible with the version ranges notation ``[]``, similar to regular requirements.
Multiple ``python_requires()`` are also possible

.. code-block:: python
    :caption: **conanfile.py**

    from conans import python_requires

    base = python_requires("MyBase/[~0.1]@user/channel")
    other = python_requires("Other/1.2@user/channel")

    class Pkg(base.MyBase):
        def source(self):
            other.some_function()

It is possible to structure the code in different files too:

.. code-block:: python
    :caption: **conanfile.py**

    from conans import ConanFile
    import mydata # reuse the strings from here
    class MyConanfileBase(ConanFile):
        exports = "*.py"
        def source(self):
            self.output.info(mydata.src)

.. code-block:: python
    :caption: **mydata.py**

    src = "My cool source!"
    build = "My cool build!"
    pkg = "My cool package!"
    info = "My cool package_info!"

This would be created with the same ``conan export`` and consumed with the same ``base = python_requires("MyBase/0.1@user/channel")`` as above.



There are a few important considerations regarding ``python_requires()``:

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

