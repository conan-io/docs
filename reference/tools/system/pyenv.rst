.. _conan_tools_system_pyenv:


PyEnv
=====

.. include:: ../../../common/experimental_warning.inc

.. important::

    This is **only** for:
    - **Executable Python packages and its Python dependencies.** (for example, meson build system)
    - **Python package used during the source build process.** (for example, html5lib as a build dependency)
    This approach doesn't work for Python library packages that you would typically use via ``import`` inside your recipe.

The ``PyEnv`` helper installs executable Python packages with **pip** inside a dedicated virtual environment (**venv**),
keeping them isolated so they don't interfere with system packages or the Conan package itself.
It is designed to use a Python CLI tool inside a recipe during the build step.

By default, it attempts to create the virtualenv using the Python you have set on your system Path.
To use a different one, you can set a Python path in the ``tools.system.pyenv:python_interpreter`` :ref:`configuration<reference_config_files_global_conf>`.


.. currentmodule:: conan.tools.system

.. autoclass:: PyEnv
    :members:
    :inherited-members:

Using a Python package in a recipe
----------------------------------

To install a python package or use a tool installed with Python, we have to install it using the ``PyEnv.install()`` method.

When the ``py_version`` parameter is defined, Conan will automatically use `UV <https://docs.astral.sh/uv/>`_ to create and manage a temporary virtual environment
with that specific Python version.
**UV requires Python 3.8 or higher**, make sure you use a compatible Python version if you want to define the ``py_version``.

We also have to call the ``PyEnv.generate()`` method to create a **Conan Environment** that adds the **Python virtualenv path** to the system path.

These two steps appear in the following recipe in the ``generate()`` method.
Calling it in this method ensures that the **Python package** and the **Conan Environment** will be available in the following steps.
In this case, in the build step, which is where we will use the installed tool.

..  code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.system import PyEnv
    from conan.tools.layout import basic_layout


    class PipPackage(ConanFile):
        name = "pip_install"
        version = "0.1"

        def layout(self):
            basic_layout(self)

        def generate(self):
            pyenv = PyEnv(self)
            pyenv.install(["meson==1.9.1"])
            pyenv.generate()

        def build(self):
            self.run("meson --version")

If we run a ``conan build`` we can see how our Python package is installed when the generate step, and how it is called in the build step as if it were installed on the system.

.. code-block:: bash

    $ conan build .

    ...

    ======== Finalizing install (deploy, generators) ========
    conanfile.py (pip_install/0.1): Calling generate()
    conanfile.py (pip_install/0.1): Generators folder: /Users/user/pip_install/build/conan
    conanfile.py (pip_install/0.1): RUN: /Users/user/pip_install/build/pip_venv_pip_install/bin/python -m pip install --disable-pip-version-check meson==1.9.1
    Collecting meson==1.9.1
      Using cached meson-1.9.1-py3-none-any.whl.metadata (1.8 kB)
    Using cached meson-1.9.1-py3-none-any.whl (1.0 MB)
    Installing collected packages: meson
    Successfully installed meson-1.9.1

    conanfile.py (pip_install/0.1): Generating aggregated env files
    conanfile.py (pip_install/0.1): Generated aggregated env files: ['conanbuild.sh', 'conanrun.sh']

    ======== Calling build() ========
    conanfile.py (pip_install/0.1): Calling build()
    conanfile.py (pip_install/0.1): RUN: meson --version
    1.9.1


.. _conan_tools_system_pyenv_cmake:

Using the PyEnv Python from CMake
---------------------------------

Calling ``PyEnv.generate()`` adds the **bin** (or **Scripts** on Windows) folder of the virtual environment to the ``PATH``
of the Conan Environment. This is enough to run the installed tools from a ``self.run()`` call, but it is **not always enough**
for CMake's ``find_package(Python)``:

- **PATH priority**: the ``VirtualBuildEnv`` is generated automatically by Conan *after* the ``generate()`` method.
  If the profile contains something like ``[buildenv]`` ``PATH=+(path)C:/Python313``, that folder will end up with a higher priority
  than the virtual environment. To avoid it, generate the ``VirtualBuildEnv`` explicitly **before** calling ``PyEnv.generate()``.
- **CMake FindPython search order**: by default, `FindPython <https://cmake.org/cmake/help/latest/module/FindPython.html>`_ does not
  just look for ``python`` or ``python3`` in the ``PATH``. It also looks for *versioned* executables (like ``python3.13``),
  prefers the most recent version it can find, and takes into account frameworks and the Windows registry.
  So, it can find a different Python than the one in the virtual environment.

.. note::

    Conan does not set the ``VIRTUAL_ENV`` environment variable when generating the ``PyEnv`` environment, because it is read by Python
    itself and it could interfere with other Python executions.

To make sure that CMake uses the Python from the virtual environment, pass the hints explicitly to CMake
with :ref:`CMakeToolchain<conan_tools_cmaketoolchain>`. The ``PyEnv`` object exposes the ``env_dir`` (root folder of the virtual environment),
``env_exe`` (path to the Python executable) and ``bin_path`` (``bin``/``Scripts`` folder) attributes for this purpose.

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain
    from conan.tools.env import VirtualBuildEnv
    from conan.tools.system import PyEnv


    class Pkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            # Generate it first, so the PyEnv path has priority over the profile [buildenv] PATH
            buildenv = VirtualBuildEnv(self)
            buildenv.generate()

            pyenv = PyEnv(self)
            pyenv.install(["html5lib~=1.0"])
            pyenv.generate()

            tc = CMakeToolchain(self)
            # Option 1: look for Python in the PATH and in the venv root
            # (STANDARD ignores the VIRTUAL_ENV of any other activated venv)
            tc.cache_variables["Python_FIND_VIRTUALENV"] = "STANDARD"
            tc.cache_variables["Python_ROOT_DIR"] = pyenv.env_dir
            # Option 2: directly point to the executable, no search is done
            # tc.cache_variables["Python_EXECUTABLE"] = pyenv.env_exe
            tc.generate()

If other Python installations in the system are still found, these extra variables can also help:

.. code-block:: python

    tc.cache_variables["Python_FIND_UNVERSIONED_NAMES"] = "FIRST"
    tc.cache_variables["Python_FIND_STRATEGY"] = "LOCATION"
    tc.cache_variables["Python_FIND_REGISTRY"] = "NEVER"
