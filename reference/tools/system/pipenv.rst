.. _conan_tools_system_pipenv:


PipEnv
======

.. include:: ../../../common/experimental_warning.inc

.. important::

    This is **only** for executable Python packages.
    This approach doesn't work for Python library packages that you would typically use via ``import``.

The ``PipEnv`` helper installs executable Python packages with **pip** inside a dedicated virtual environment (**venv**),
keeping them isolated so they don't interfere with system packages or the Conan package itself.

.. currentmodule:: conan.tools.system

.. autoclass:: PipEnv
    :members:
    :inherited-members:

It is designed to be used in two different ways:

1. Using a Python package in a recipe.
2. Use a tool installed as a Python package locally and reuse it in other recipes.

Using a Python package in a recipe
----------------------------------

To use a tool installed with Python, we have to install it using the ``PipEnv.install()`` method.
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


Use a tool installed as a Python package and reuse it in other recipes
----------------------------------------------------------------------

In this case, we want to locally embed the installation of a tool using pip and reuse it as a conan recipe.

To do this, we need to install our tool using ``PipEnv.install()``, but in this case we will specify that we want it
to create the virtualenv in the ``package_folder``.

In this case, we don't need to call the ``PipEnv.generate()`` method because we're not going to use the tool within this recipe.
We just want to make it reusable.

When creating a recipe to encapsulate a tool installed with Python, several things must be taken into account:

- The packages are installed in the finalize method. This ensures that the contents of the package folder do not change when the installed tools are run,
  because Python packages normally generate certain files when executed.
- We will add the properties ``build_policy = "missing"`` and ``upload_policy = "skip"`` to the recipe to ensure that it is only used locally
  and the resulting package will not be uploaded. This is important because **the generated package only works on the machine on which it was generated**
  due to how Python virtual environments work.

..  code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.system import PipEnv
    from conan.tools.layout import basic_layout


    class MesonPipPackage(ConanFile):
        name = "pip_meson"
        version = "0.1"
        build_policy = "missing"
        upload_policy = "skip"

        def layout(self):
            basic_layout(self)

        def finalize(self):
            PipEnv(self, self.package_folder).install(["meson==1.9.1"])

        def package_info(self):
            python_env_bin = PipEnv(self, self.package_folder).bin_dir
            self.buildenv_info.prepend_path("PATH", python_env_bin)

.. code-block:: bash

    $ conan create . --version 0.1

  -------- Installing package pip_meson/0.1 (1 of 1) --------
  ...
  pip_meson/0.1: Calling finalize()
  pip_meson/0.1: RUN: /Users/user/.conan2/p/b/pip_m19e45e29ec612/f/pip_venv_pip_meson/bin/python -m pip install --disable-pip-version-check meson==1.9.1
  Collecting meson==1.9.1
    Using cached meson-1.9.1-py3-none-any.whl.metadata (1.8 kB)
  Using cached meson-1.9.1-py3-none-any.whl (1.0 MB)
  Installing collected packages: meson
  Successfully installed meson-1.9.1

..  code-block:: python
    :caption: conanfile.py

    from conan import ConanFile


    class PipBuildPackage(ConanFile):
        name = "reuse_pip"
        version = "0.1"

        def requirements(self):
            self.tool_requires("pip_meson/0.1")

        def build(self):
            self.run("meson --version")

.. code-block:: bash

    $ conan build .

    ======== Computing dependency graph ========
    Graph root
        conanfile.py (reuse_pip/0.1): /Users/user/reuse_pip/conanfile.py
    Build requirements
        pip_meson/0.1#0f1f4d0fc28b2ef5951f42131ede4f99 - Cache

    ======== Computing necessary packages ========
    Build requirements
        pip_meson/0.1#0f1f4d0fc28b2ef5951f42131ede4f99:da39a3ee5e6b4b0d3255bfef95601890afd80709#0ba8627bd47edc3a501e8f0eb9a79e5e - Cache

    ======== Installing packages ========
    pip_meson/0.1: Already installed! (1 of 1)
    pip_meson/0.1: Finalized folder /Users/user/.conan2/p/b/pip_m19e45e29ec612/f

    ======== Finalizing install (deploy, generators) ========
    conanfile.py (reuse_pip/0.1): Generating aggregated env files
    conanfile.py (reuse_pip/0.1): Generated aggregated env files: ['conanbuild.sh', 'conanrun.sh']

    ======== Calling build() ========
    conanfile.py (reuse_pip/0.1): Calling build()
    conanfile.py (reuse_pip/0.1): RUN: meson --version
    1.9.1