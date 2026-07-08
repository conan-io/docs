.. _examples_extensions_python_build_backend_build_python_extension_with_conan:

Build a Python C/C++ extension using Conan and conan-py-build
===============================================================

In this example, we are going to create a small Python package with a C++ extension
that uses `pybind11 <https://pybind11.readthedocs.io/>`_ to expose the C++ code to
Python and `fmt <https://fmt.dev/>`_ as a regular C++ dependency. Both dependencies
are downloaded and built by Conan, driven by
`conan-py-build <https://github.com/conan-io/conan-py-build>`_, a
`PEP 517 <https://peps.python.org/pep-0517/>`_ build backend that lets ``pip`` (or
``build``, or ``uv``) build the C/C++ part of a Python package through Conan.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/extensions/python_build_backend

The project has this structure:

.. code-block:: text

    .
    ├── pyproject.toml
    ├── conanfile.py
    ├── CMakeLists.txt
    ├── LICENSE
    ├── src
    │   └── myadder.cpp
    └── python
        └── myadder
            └── __init__.py

Let's have a look at the *pyproject.toml* file:

.. code-block:: toml
    :caption: **pyproject.toml**

    [build-system]
    requires = ["conan-py-build"]
    build-backend = "conan_py_build.build"

    [project]
    name = "myadder"
    version = "0.1.0"
    description = "A simple Python package with a C++ extension (pybind11 + fmt) built through Conan"
    license = "MIT"
    license-files = ["LICENSE"]
    requires-python = ">=3.8"

    [tool.conan-py-build.wheel]
    packages = ["python/myadder"]

Setting ``conan-py-build`` as the ``build-backend`` means that every time this
package is built (``pip wheel .``, ``pip install .``, ``python -m build``, etc.), the
backend will read the recipe declared in the standard *conanfile.py*, resolve and
install its dependencies through Conan, run the ``build()`` and ``package()`` methods,
and copy everything ``package()`` staged into the resulting wheel.

The ``[tool.conan-py-build.wheel]`` section tells the backend where the pure Python
part of the package lives, so it also gets copied into the wheel next to the compiled
extension. See the `configuration reference <https://conan-py-build.conan.io/configuration/>`_
for all the available options (dynamic versioning, extra Conan profiles/arguments,
entry points, sdist contents, etc.).

Now, the *conanfile.py* is a regular Conan recipe, no different from one used to
create a C++ package:

.. code-block:: python
    :caption: **conanfile.py**

    import sys

    from conan import ConanFile
    from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout


    class MyAdderConan(ConanFile):
        name = "myadder"
        settings = "os", "compiler", "build_type", "arch"

        def layout(self):
            cmake_layout(self)

        def requirements(self):
            self.requires("pybind11/3.0.1")
            self.requires("fmt/12.1.0")

        def generate(self):
            tc = CMakeToolchain(self)
            tc.cache_variables["Python3_EXECUTABLE"] = sys.executable
            tc.generate()
            deps = CMakeDeps(self)
            deps.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            cmake = CMake(self)
            cmake.install()

It declares **pybind11** and **fmt** as regular requirements, downloaded as
precompiled binaries from ConanCenter (or built from source if needed), and uses
:ref:`CMakeToolchain<conan_tools_cmaketoolchain>` and :ref:`CMakeDeps<conan_tools_cmakedeps>`
to configure and build the extension with CMake.

.. important::

    Setting ``Python3_EXECUTABLE`` to ``sys.executable`` keeps CMake on the
    same interpreter ``pip`` uses, avoiding a wrong ABI build.

.. important::

    For the compiled extension to be importable, it must land under a directory
    that matches the Python package name, so the ``.so``/``.pyd`` ends up next to
    ``__init__.py`` in the wheel. This is controlled by the ``DESTINATION`` argument
    of CMake's ``install(TARGETS ...)``.

The *CMakeLists.txt* builds the ``_core`` extension module with pybind11, links it
against ``fmt``, and installs it into a ``myadder`` folder to match the Python
package name:

.. code-block:: cmake
    :caption: **CMakeLists.txt**

    cmake_minimum_required(VERSION 3.15)
    project(myadder LANGUAGES CXX)

    find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
    set(PYBIND11_FINDPYTHON ON)
    find_package(pybind11 CONFIG REQUIRED)
    find_package(fmt REQUIRED)

    pybind11_add_module(_core src/myadder.cpp)
    target_link_libraries(_core PRIVATE pybind11::module fmt::fmt)

    install(TARGETS _core DESTINATION myadder)

The C++ source exposes an ``add()`` function to Python, using **fmt** to print
the result in bold green text:

.. code-block:: cpp
    :caption: **src/myadder.cpp**

    #include <pybind11/pybind11.h>
    #include <fmt/core.h>
    #include <fmt/color.h>

    namespace py = pybind11;

    double add(double a, double b) {
        double result = a + b;
        fmt::print(fg(fmt::color::green) | fmt::emphasis::bold,
                   "{} + {} = {}\n", a, b, result);
        return result;
    }

    PYBIND11_MODULE(_core, m) {
        m.doc() = "Simple Python extension using fmt via Conan.";
        m.def("add", &add, "Add two numbers and print the result formatted with fmt.",
              py::arg("a"), py::arg("b"));
    }

And finally, *python/myadder/__init__.py* just re-exports the function from the
compiled module:

.. code-block:: python
    :caption: **python/myadder/__init__.py**

    from myadder._core import add

    __all__ = ["add"]

Build and test
--------------

Build the wheel with ``pip``. There's no need to install ``conan-py-build``
beforehand: since it's declared under ``[build-system] requires`` in
*pyproject.toml*, ``pip`` installs it (and Conan itself) into an isolated
build environment automatically:

.. code-block:: bash

    $ pip wheel . -w dist/

Conan will install **pybind11** and **fmt**, build the extension with CMake, and
``conan-py-build`` will assemble the resulting wheel and save it into the *dist*
folder, e.g. *dist/myadder-0.1.0-cp312-cp312-macosx_14_0_arm64.whl* (the exact
filename depends on your platform and Python version).

A wheel is just a zip file, so you can check what got packaged without
installing it:

.. code-block:: bash

    $ python -m zipfile -l dist/myadder-*.whl
    File Name                                             Modified             Size
    myadder/__init__.py                            2026-07-08 14:01:30           49
    myadder/_core.cpython-312-darwin.so            2026-07-08 14:41:12       233288
    myadder-0.1.0.dist-info/METADATA               2026-07-08 14:41:08          212
    myadder-0.1.0.dist-info/WHEEL                  2026-07-08 14:41:12          101
    myadder-0.1.0.dist-info/licenses/LICENSE       2026-07-08 14:01:32         1083
    myadder-0.1.0.dist-info/RECORD                 2026-07-08 14:41:12          471

Note how the compiled ``_core`` extension, the one Conan's ``package()`` staged
during the build, ends up right next to ``__init__.py`` under ``myadder/`` —
exactly the layout the ``DESTINATION`` in *CMakeLists.txt* was set up for.

Now install it and try it out:

.. code-block:: bash

    $ pip install dist/myadder-*.whl
    $ python -c "from myadder import add; add(2, 3)"
    2 + 3 = 5

The line above is printed by the C++ extension in bold green, courtesy of
**fmt** — a visible sign that the compiled code, not Python, produced it.

.. seealso::

    - :ref:`Python integration<integrations_python>`
    - `conan-py-build documentation <https://conan-py-build.conan.io>`_, for configuration
      options like dynamic versioning, custom Conan profiles, entry points, and shared
      library handling with ``auditwheel``/``delocate``/``delvewheel``.
    - `Introducing conan-py-build <https://blog.conan.io/cpp/conan/python/2026/05/05/Introducing-conan-py-build.html>`_
      blog post.
    - `conan-py-build examples <https://github.com/conan-io/conan-py-build/tree/main/examples>`_,
      including Meson, nanobind, and cibuildwheel-based builds.
