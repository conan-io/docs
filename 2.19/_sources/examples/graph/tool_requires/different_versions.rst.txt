Depending on different versions of the same tool-require
========================================================

.. note::

    This is an **advanced** use case. It shouldn't be necessary in the vast majority of cases.


In the general case, trying to do something like this:

.. code-block:: python

    def build_requirements(self):
        self.tool_requires("gcc/1.0")
        self.tool_requires("gcc/2.0")

Will generate a "conflict", showing an error like ``Duplicated requirement``. This is correct in most situations,
when it is obvious that it is not possible to use 2 versions of the same compiler to build the current package.

However there are some exceptional situations when something like that is desired. Let's recreate the potential
scenario. Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: shell

    git clone https://github.com/conan-io/examples2.git
    cd examples2/examples/graph/tool_requires/different_versions

There we have a ``gcc`` fake recipe with:

.. code-block:: python

    class Pkg(ConanFile):
        name = "gcc"
        
        def package(self):
            echo = f"@echo off\necho MYGCC={self.version}!!"
            save(self, os.path.join(self.package_folder, "bin", f"mygcc{self.version}.bat"), echo)
            save(self, os.path.join(self.package_folder, "bin", f"mygcc{self.version}.sh"), echo)
            os.chmod(os.path.join(self.package_folder, "bin", f"mygcc{self.version}.sh"), 0o777)


This is not an actual compiler, it fakes it with a shell or bat script that prints ``MYGCC=current-version`` when executed.
Note the binary itself is called ``mygcc1.0`` and ``mygcc2.0``, that is, it contains the version in the executable name itself.

We can create 2 different versions for ``gcc/1.0`` and ``gcc/2.0`` with:


.. code-block:: bash

    $ conan create gcc --version=1.0
    $ conan create gcc --version=2.0

Now, in the ``wine`` folder there is a ``conanfile.py`` like this:

.. code-block:: python

    class Pkg(ConanFile):
        name = "wine"
        version = "1.0"

        def build_requirements(self):
            # If we specify "run=False" they no longer conflict
            self.tool_requires("gcc/1.0", run=False)
            self.tool_requires("gcc/2.0", run=False)

        def generate(self):
            # It is possible to individually reference each one
            gcc1 = self.dependencies.build["gcc/1.0"]
            assert gcc1.ref.version == "1.0"
            gcc2 = self.dependencies.build["gcc/2.0"]
            assert gcc2.ref.version == "2.0"

        def build(self):
            ext = "bat" if platform.system() == "Windows" else "sh"
            self.run(f"mygcc1.0.{ext}")
            self.run(f"mygcc2.0.{ext}")


The first important point is the ``build_requirements()`` method, that does a ``tool_requires()`` to both versions,
but defining ``run=False``. **This is very important**: we are telling Conan that we actually don't need to run
anything from those packages. As ``tool_requires`` are not visible, they don't define headers or libraries, there is
nothing that makes Conan identify those 2 ``tool_requires`` as conflicting. So the dependency graph can be constructed
without errors, and the ``wine/1.0`` package will contain 2 different tool-requires to both ``gcc/1.0`` and ``gcc/2.0``.

Of course, it is not true that we won't run anything from those ``tool_requires``, but now Conan is not aware of it,
and it is completely the responsibility of the user to manage it.

.. warning::

    Using ``run=False`` makes the ``tool_requires()`` completely invisible, that means that profile ``[tool_requires]``
    will not be able to override its version, but it would create an extra tool-require dependency with the version
    injected from the profile. You might want to exclude specific packages with something like ``!wine/*: gcc/3.0``.

The recipe has still access in the ``generate()`` method to each different ``tool_require`` version, just by providing
the full reference like ``self.dependencies.build["gcc/1.0"]``.

Finally, the most important part is that the usage of those tools is completely the responsibility of the user. The ``bin``
folder of both ``tool_requires`` containing the executables will be in the path thanks to the ``VirtualBuildEnv`` generator
that by default updates the PATH env-var. In this case the executables are different like ``mygcc1.0.sh```and ``mygcc2.0.sh``,
so it is not an issue, and each one will be found inside its package.

But if the executable file was exactly the same like ``gcc.exe``, then it would be necessary to obtain the full folder
(typically in the ``generate()`` method) with something like ``self.dependencies.build["gcc/1.0"].cpp_info.bindir`` and
use the full path to disambiguate.


Let's see it working. If we execute:


.. code-block:: bash

    $ conan create wine
    ...
    wine/1.0: RUN: mygcc1.0.bat
    MYGCC=1.0!!

    wine/1.0: RUN: mygcc2.0.bat
    MYGCC=2.0!!
