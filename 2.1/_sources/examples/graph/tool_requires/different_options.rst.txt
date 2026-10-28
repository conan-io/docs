Depending on same version of a tool-require with different options
==================================================================

.. note::

    This is an **advanced** use case. It shouldn't be necessary in the vast majority of cases.


In the general case, trying to do something like this:

.. code-block:: python

    def build_requirements(self):
        self.tool_requires("gcc/1.0")
        self.tool_requires("gcc/1.0")

Will generate a "conflict", showing an error like ``Duplicated requirement``.

However there are some exceptional situations that we could need to depend on the same ``tool_requires`` version, 
but using different binaries of that ``tool_requires``. This can be achieved by passing different ``options`` to those
``tool_requires``. Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: shell

    git clone https://github.com/conan-io/examples2.git
    cd examples2/examples/graph/tool_requires/different_options

There we have a ``gcc`` fake recipe with:

.. code-block:: python

    class Pkg(ConanFile):
        name = "gcc"
        version = "1.0"
        options = {"myoption": [1, 2]}

        def package(self):
            # This fake compiler will print something different based on the option
            echo = f"@echo off\necho MYGCC={self.options.myoption}!!"
            save(self, os.path.join(self.package_folder, "bin", f"mygcc{self.options.myoption}.bat"), echo)
            save(self, os.path.join(self.package_folder, "bin", f"mygcc{self.options.myoption}.sh"), echo)
            os.chmod(os.path.join(self.package_folder, "bin", f"mygcc{self.options.myoption}.sh"), 0o777)


This is not an actual compiler, it fakes it with a shell or bat script that prints ``MYGCC=current-option`` when executed.
Note the binary itself is called ``mygcc1`` and ``mygcc2``, that is, it contains the option in the executable name itself.

We can create 2 different binaries for ``gcc/1.0`` with:


.. code-block:: bash

    $ conan create gcc -o myoption=1
    $ conan create gcc -o myoption=2

Now, in the ``wine`` folder there is a ``conanfile.py`` like this:

.. code-block:: python

    class Pkg(ConanFile):
        name = "wine"
        version = "1.0"
        
        def build_requirements(self):
            self.tool_requires("gcc/1.0", run=False, options={"myoption": 1})
            self.tool_requires("gcc/1.0", run=False, options={"myoption": 2})

        def generate(self):
            gcc1 = self.dependencies.build.get("gcc", options={"myoption": 1})
            assert gcc1.options.myoption == "1"
            gcc2 = self.dependencies.build.get("gcc", options={"myoption": 2})
            assert gcc2.options.myoption == "2"

        def build(self):
            ext = "bat" if platform.system() == "Windows" else "sh"
            self.run(f"mygcc1.{ext}")
            self.run(f"mygcc2.{ext}")


The first important point is the ``build_requirements()`` method, that does a ``tool_requires()`` to both binaries,
but defining ``run=False`` and ``options={"myoption": value}`` traits. **This is very important**: we are telling Conan 
that we actually don't need to run anything from those packages. As ``tool_requires`` are not visible, they don't define
headers or libraries and they define different ``options``, there is nothing that makes Conan identify those 2 ``tool_requires`` 
as conflicting. So the dependency graph can be constructed without errors, and the ``wine/1.0`` package will contain 
2 different tool-requires to both ``gcc/1.0`` with ``myoption=1`` and with ``myoption=2``.

Of course, it is not true that we won't run anything from those ``tool_requires``, but now Conan is not aware of it,
and it is completely the responsibility of the user to manage it.

.. warning::

    Using ``run=False`` makes the ``tool_requires()`` completely invisible, that means that profile ``[tool_requires]``
    will not be able to override its version, but it would create an extra tool-require dependency with the version
    injected from the profile. You might want to exclude specific packages with something like ``!wine/*: gcc/3.0``.

The recipe still has access in the ``generate()`` method to each different ``tool_require`` version, just by providing
the options values for the dependency that we want ``self.dependencies.build.get("gcc", options={"myoption": 1})``.

Finally, the most important part is that the usage of those tools is completely the responsibility of the user. The ``bin``
folder of both ``tool_requires`` containing the executables will be in the path thanks to the ``VirtualBuildEnv`` generator
that by default updates the PATH env-var. In this case the executables are different like ``mygcc1.sh```and ``mygcc2.sh``,
so it is not an issue, and each one will be found inside its package.

But if the executable file was exactly the same like ``gcc.exe``, then it would be necessary to obtain the full folder
(typically in the ``generate()`` method) with something like ``self.dependencies.build.get("gcc", options={"myoption": 1}).cpp_info.bindir`` and
use the full path to disambiguate.


Let's see it working. If we execute:


.. code-block:: bash

    $ conan create wine
    ...
    wine/1.0: RUN: mygcc1.bat
    MYGCC=1!!

    wine/1.0: RUN: mygcc2.bat
    MYGCC=2!!
