.. _conan_tools_system_pipenv:


PipEnv
======

.. include:: ../../../common/experimental_warning.inc

.. important::

    This is **only** for:
    - **Executable Python packages and its Python dependencies.** (for example, meson build system)
    - **Python package used during the source build process.** (for example, html5lib as a build dependency)
    This approach doesn't work for Python library packages that you would typically use via ``import`` inside your recipe.

The ``PipEnv`` helper installs executable Python packages with **pip** inside a dedicated virtual environment (**venv**),
keeping them isolated so they don't interfere with system packages or the Conan package itself.
It is designed to use a Python CLI tool inside a recipe during the build step.

By default, it attempts to create the virtualenv using the Python you have set on your system Path.
To use a different one, you can set a Python path in the ``tools.system.pipenv:python_interpreter`` :ref:`configuration<reference_config_files_global_conf>`.


.. currentmodule:: conan.tools.system

.. autoclass:: PipEnv
    :members:
    :inherited-members:

Using a Python package in a recipe
----------------------------------

To install a python package or use a tool installed with Python, we have to install it using the ``PipEnv.install()`` method.
We also have to call the ``PipEnv.generate()`` method to create a **Conan Environment** that adds the **Python virtualenv path** to the system path.

These two steps appear in the following recipe in the ``generate()`` method.
Calling it in this method ensures that the **Python package** and the **Conan Environment** will be available in the following steps.
In this case, in the build step, which is where we will use the installed tool.

..  code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.system import PipEnv
    from conan.tools.layout import basic_layout


    class PipPackage(ConanFile):
        name = "pip_install"
        version = "0.1"

        def layout(self):
            basic_layout(self)

        def generate(self):
            PipEnv(self).install(["meson==1.9.1"])
            PipEnv(self).generate()

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
