.. _reference_conanfile_methods_build_id:

build_id()
==========

The ``build_id()`` method allows you to **reuse a single build** to create multiple binary packages in the Conan cache,
saving time by avoiding unnecessary rebuilds.

It is primarily an optimization tool for situations where **building each configuration separately isn't feasible**.

There are a couple of scenarios where this could be useful, for example, when a package build:

* **Generates multiple configurations in a single build run**:
  Some build scripts always produce both Debug and Release artifacts together, without a way to build them separately.


* **Produces one configuration but different sets of artifacts**:
  The build could generate the main library plus some test executables, and you want to create:

  * one package with just the library (for general use), and
  * another package that includes both the library and the test binaries (for compliance, debugging, or reproducibility).

In these scenarios, **reusing the same build folder avoids recompiling the same sources multiple times** just because you need slightly different packaging.

How does the build folder relate to the package ID and the build ID?
--------------------------------------------------------------------

By default, Conan creates **one build folder per unique package ID**, where:

* Generally, the **package ID** depends on the combination of `settings`, `options`, and dependencies.
* Each different **package ID** triggers a separate ``build()`` execution and generates a separate build folder.

When you define the ``build_id()`` method, you can **force different package IDs to share the same build folder** by customizing `self.info_build`:

* ``self.info_build`` is like ``self.info``, but it only affects the computation of the **build ID**, not the final package ID.
* Any package IDs with the same build ID will reuse the same build folder and the same build step.


Example: sharing the build for Debug and Release
++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build_id(self):
        self.info_build.settings.build_type = "Any"

* With this recipe, Debug and Release will each produce their own package IDs (and thus their own binary packages),
  but they will **share the same build folder**, because the build ID ignores the ``build_type`` setting.
* **However, you still need to run one** :command:`conan create` **command per configuration** (e.g., once for Debug, once for Release).
  Conan will check if the build folder already exists (based on the shared build ID) and skip the actual compilation
  if it's already been built, only executing `package()` to create the corresponding package.

Example workflow:

.. code-block:: bash

    # First build: creates the build folder + packages the Debug package
    $ conan create . -s build_type=Debug

    # Second build: reuses the previous build folder + packages the Release package without rebuilding
    $ conan create . -s build_type=Release

This way, although we called :command:`conan create` twice (once per package ID), the actual build will only happen once.

.. note::

    You can also customize ``build_id()`` based on options:

    .. code-block:: python

        def build_id(self):
            self.info_build.options.myoption = "MyValue"
            self.info_build.options.fullsource = "Always"

Conditional usage of the build ID
---------------------------------

If the ``build_id()`` method does not modify the ``self.info_build`` data, and produces the same build ID as the package ID,
then the standard behavior will be applied. For example:

.. code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build_id(self):
        if self.settings.os == "Windows":
            self.info_build.settings.build_type = "Any"

This will only produce a different **build ID** if the package is for Windows, so it will only run the ``build()`` method once
for all the ``build_type`` values.

For any other OS, Conan will behave as usual (as if the ``build_id()`` method was not defined), running the ``build()`` method
for every ``build_type`` configuration.

.. note::

    **Best practices**

    The goal of the ``build_id()`` method is to deal with legacy build scripts that cannot easily be changed
    to compile one configuration at a time. We strongly recommend to just package **one package binary per package ID**
    for each different configuration.
