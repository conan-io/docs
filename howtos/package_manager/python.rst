Conan: A Python package manager
===============================


Conan is a C and C++ package manager, and to deal with the vast variability of C and C++ build systems, compilers, configurations, etc., it was designed with a great flexibility in mind, trying to let the users do almost what they want. This is one of the reasons to use Python as the scripting language for conan package recipes.
With this flexibility, conan is able to do very different tasks: it is able to package Visual Studio modules: http://blog.conan.io/2016/06/01/Building-and-packaging-C++-modules-in-VS2015.html,
also to :ref:`Conan as a Go package manager<go_package_manager>`, build packages from sources, from binaries retrieved from elsewhere, etc.


The story started when some users requested a solution to be able to share common python code among their package recipes. Maybe that python code could be managed separately, but being conan a package manager, they requested if they could put the common code in a conan package. So we thought, why not, we already did a proof of concept for other languages as go-lang, should be possible. And it turned out that with very little effort conan can be used as a package manager for Python too. Lets see how:



A basic python package
-----------------------

Let's begin with a simple python package, a "hello world" functionality that we want to package and reuse:


.. code-block:: python

    def hello():
        print("Hello World from Python!")


To create a package, all we need to do is create the following layout:


.. code-block:: text

    -| hello.py
     | __init__.py
     | conanfile.py



The ``__init__.py`` is blank.
It is not necessary to compile code, so the package recipe ``conanfile.py`` is quite simple:



.. code-block:: python

    from conans import ConanFile

    class HelloPythonConan(ConanFile):
        name = "HelloPy"
        version = "0.1"
        exports = '*'
        build_policy = "missing"

        def package(self):
            self.copy('*.py')

        def package_info(self):
            self.env_info.PYTHONPATH.append(self.package_folder)



The ``exports`` will copy both the ``hello.py`` and the ``__init__.py`` into the recipe. The ``package()`` method is also obvious: to construct the package just copy the python sources.


The ``package_info()`` adds the current package folder to the ``PYTHONPATH`` conan environment variable. It will not affect the real environment variable unless the end user want it.


It can be seen that this recipe would be practically the same for most python packages, so it could be factored in a ``PythonConanFile`` base class to further simplify it (open a feature request, or better a pull request :) )


With this recipe, all we have to do is:



.. code-block:: bash

    $ conan export memsharded/testing
    $ conan search



Of course if you want to share the package with your team, you can ``conan upload`` it to a remote server. But to create and test the package, we can do everything locally.

Now the package is ready for consumption. In another folder, we can create a ``conanfile.txt`` (or a ``conanfile.py`` if we prefer):


.. code-block:: text

    [requires]
    HelloPy/0.1@memsharded/testing


And install it with the following command:


.. code-block:: bash

    $ conan install -g virtualenv


Creating the above ``conanfile.txt`` might be unnecessary for this simple example, as you can directly run ``conan install HelloPy/0.1@memsharded/testing -g virtualenv``, however, using the file is the canonical way.


The specified ``virtualenv`` generator will create an ``activate`` script (in Windows ``activate.bat``), that basically contains the environment, in this case, the ``PYTHONPATH``. Once we activate it, we are able to find the package in the path and use it:



.. code-block:: bash

    $ activate
    $ python
    Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:19:22) [MSC v.1500 32 bit (Intel)] on win32
    ...
    >>> import hello
    >>> hello.hello()
    Hello World from Python!
    >>>



The above shows an interactive session, but you can import also the functionality in a regular python script!

And this is basically it! Everything you get from conan, you can easily use it for python: transitives dependencies, conflict resolution, dependency overriding... as well as all the advanced steps that conan provides: ``build()``, ``package()``, ``package_info()``, having different packages for different platforms, managing different remotes in git-like decentralized architecture...


As advanced in the introduction, the real goal of this functionality was to have reusable python code among conan recipes for C and C++ packages. Let`s see how can it be done:


Reusing python code in your recipes
------------------------------------

As the conan recipes are python code itself, it is easy to reuse python packages in them. A basic recipe using the created package would be:


.. code-block:: python

    from conans import ConanFile, tools

    class HelloPythonReuseConan(ConanFile):
        requires = "HelloPy/0.1@memsharded/testing"

        def build(self):
            with tools.pythonpath(self):
                from hello import hello
                hello()



The ``requires`` section is just referencing the previously created package. The functionality of that package can be used in several methods of the recipe: ``source()``, ``build()``, ``package()`` and ``package_info()``, i.e. all of the methods used for creating the package itself. Note that in other places it is not possible, as it would require the dependencies of the recipe to be already retrieved, and such dependencies cannot be retrieved until the basic evaluation of the recipe has been executed.


In the above example, the code is reused in the ``build()`` method as an example. Note the use of a helper context, which basically activates/deactivates the ``PYTHONPATH`` environment variable with the value assigned in the package. We didn't want to do this activation implicit for all conan packages, but rather make it explicit.



.. code-block:: bash

    $ conan install 
    ...
    $ conan build .
    Hello World from Python!




A full python and C/C++ package manager
----------------------------------------

Once we realized what could be achieved with this functionality, we couldn't resist to try a full application. The real utility of this is that conan is a C and C++ package manager. So if we want to create a python package that wraps the functionality of, lets say the Poco C++ library, it can be easily done. Poco itself has transitive (C/C++) dependencies, but they are already handled by conan. Furthermore, a very interesting thing is that nothing has to be done in advance for that library, thanks to useful tools as **pybind11**, that allows to create python bindings easily.


So let's build a package with the following files:


- ``conanfile.py``: The package recipe
- ``__init__.py``: necessary file, blank
- ``pypoco.cpp``: The C++ code with the ``pybind11`` wrapper for Poco that generates a python extension (a shared library that can be imported from python)
- ``CMakeLists.txt``: cmake build file that is able to compile ``pypoco.cpp`` into a python extension (``pypoco.pyd`` in Windows, ``pypoco.so`` in Linux)
- ``poco.py``: A python file that makes use of the pypoco python binary extension built with ``pypoco.cpp``
- ``test_package/conanfile.py``: A test consumer recipe to create and test the package


The ``pypoco.cpp`` file can be coded easily thanks to the elegant ``pybind11`` library:



.. code-block:: cpp

    #include <pybind11/pybind11.h>
    #include "Poco/Random.h"

    using Poco::Random;
    namespace py = pybind11;

    PYBIND11_PLUGIN(pypoco) {
        py::module m("pypoco", "pybind11 example plugin");
        py::class_<Random>(m, "Random")
            .def(py::init<>())
            .def("nextFloat", &Random::nextFloat);
        return m.ptr();
    }


And the ``poco.py`` file is straigthforward:


.. code-block:: cpp

    import sys
    import pypoco

    def random_float():
        r = pypoco.Random()
        return r.nextFloat()


The ``conanfile.py`` has a few more lines than the above, but still quite easy to understand:

.. code-block:: python

    from conans import ConanFile, tools, CMake

    class PocoPyReuseConan(ConanFile):
        name = "PocoPy"
        version = "0.1"
        requires = "Poco/1.7.8p3@pocoproject/stable", "pybind11/any@memsharded/stable"
        settings = "os", "compiler", "arch", "build_type"
        exports = "*"
        generators = "cmake"
        build_policy = "missing"

        def build(self):
            cmake = CMake(self)
            pythonpaths = "-DPYTHON_INCLUDE_DIR=C:/Python27/include -DPYTHON_LIBRARY=C:/Python27/libs/python27.lib"
            self.run('cmake %s %s -DEXAMPLE_PYTHON_VERSION=2.7' % (cmake.command_line, pythonpaths))
            self.run("cmake --build . %s" % cmake.build_config)

        def package(self):
            self.copy('*.py*')
            self.copy("*.so")

        def package_info(self):
            self.env_info.PYTHONPATH.append(self.package_folder)

The recipe now declares 2 ``requires``, the Poco library and the pybind11 library that we will be using to create the binary extension.

As we are actually building some C++ code, we need a few important things:


- Input ``settings`` that define the OS, compiler, version and architecture we are using to build our extension. This is necessary, as we will see later, the binary we are building must match the architecture of the python interpreter that we will be using


- The ``build()`` method is used to actually invoke ``cmake``. See in my case I have had to hardcode the python path in the example, as the ``CMakeLists.txt`` call to ``find_package(PythonLibs)`` didn't find my python installed in ``C:/Python27``, quite a standard path. I have added the ``cmake generator`` too, to be able to easily use the declared ``requires`` build information inside my ``CMakeLists.txt``


- The ``CMakeLists.txt`` is not posted here, but is basically the one used by pybind11 example, with just 2 lines to include the conan generated cmake file for dependencies. It can be inspected in the github repo.


- Note that in my example I am just using Python 2.7 as an input option. If necessary, more options for other interpreters/architectures could be easily provided, as well as to avoiding the hardcoded paths. Even the python interpreter itself could be packaged in a conan package, we have been reported by some users doing so.


The above recipe will generate a different binary for different compilers or versions. As the binary is being wrapped by python, we could avoid this and use the same binary for different setups, modifying this behavior with the ``conan_info()`` method.



.. code-block:: bash

    $ conan export memsharded/testing
    $ conan install PocoPy/0.1@memsharded/testing -s arch=x86 -g virtualenv
    $ activate
    $ python
    >>> import poco
    >>> poco.random_float()
    0.697845458984375


Now the ``conan install`` first invocation will build retrieve the dependencies and build the package. Next invocation will use the cached binaries and be much faster. Note how we have to specify ``-s arch=x86`` to build matching the architecture of the python interpreter to be used, in our case, 32 bits.


Also, in the ``conan install`` output we can read the dependencies that are being pulled:



.. code-block:: bash

    Requirements
        OpenSSL/1.0.2l@conan/stable from conan.io
        Poco/1.7.8p3@pocoproject/stable from conan.io
        PocoPy/0.1@memsharded/testing from local
        pybind11/any@memsharded/stable from conan.io
        zlib/1.2.11@conan/stable from conan.io



This is the great thing about using conan for this task, by depending on Poco, other C and C++ transitive dependencies are being retrieved and used in the application.


If you want to have a further look to the code of these examples, you can check [this github repo](https://github.com/memsharded/python-conan-packages). The above examples and code have been tested only in Win10, VS14u2, but might work with other configurations with little or no extra work (but haven't tested)
