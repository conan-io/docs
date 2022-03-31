
.. _conan2_migration_guide_recipes:


Migrating the recipes
=====================

We introduced changes to ``Conan 1.X`` versions so you can start migrating your recipes to do a smooth transition to
``Conan 2.0``.


Python import statements
------------------------

- All the imports from the ``conans`` package have to be replaced. The Conan 2.0 ones are in the ``conan`` package. Note
  the plural.
- The "tools" functions are now organized in different packages, you can check the :ref:`complete reference here<conan_tools>`.

.. code-block:: python
   :caption: **From:**

    from conans import ConanFile, tools



.. code-block:: python
   :caption: **To:**

    from conan import ConanFile
    from conan.tools.files import save, load
    from conan.tools.gnu import AutotoolsToolchain, AutotoolsDeps
    from conan.tools.microsoft import unix_path, VCVars, is_msvc
    from conan.errors import ConanInvalidConfiguration
    from conan.errors import ConanException
    ...



Requirements
------------

- Use ``self.test_requires()`` to define test requirements instead of the legacy
  ``self.build_requires(..., force_host_context)``.
- Use ``self.tool_requires()`` to define the legacy build_requires.



.. code-block:: python
   :caption: **From:**

    from conans import ConanFile

    class Pkg(Conanfile):

          ...

          def build_requirements(self):
              self.build_requires("nasm/2.15.05")
              self.build_requires("gtest/0.1", force_host_context=True)



.. code-block:: python
   :caption: **To:**

    from conan import ConanFile

    class Pkg(Conanfile):

          ...

          def build_requirements(self):
              self.tool_requires("nasm/2.15.05")
              self.test_requires("gtest/0.1")




Settings
--------

- Do not use dictionary expressions in your recipe ``settings`` definition (like ``settings = {"os": ["Windows", "Linux"]}``. This
  way of limiting supported configurations by one recipe will be removed. Use the ``validate()`` method instead to raise
  ``ConanInvalidConfiguration`` if strictly necessary to fail fast for unsupported configurations.

  .. code-block:: python

    from conan import ConanFile

    class Pkg(Conanfile):

          settings = "os", "arch", "compiler"

          ...

          def validate(self):
              if self.settings.os == "Macos":
                  raise ConanInvalidConfiguration("Macos not supported")





- In Conan 2, removing a setting, for example, ``del self.settings.compiler.libcxx`` in the ``configure()`` method, will
  raise an exception if the setting doesn't exist. It has to be protected with try/except:

  .. code-block:: python

    def configure(self):
        try:
           # In windows, with msvc, the compiler.libcxx doesn't exist, so it will raise.
           del self.settings.compiler.libcxx
        except Exception:
           pass


Options
-------

The definition of the ``default_options`` attribute has changed when referring to a dependency. It is related to the
:ref:`unified patterns in the command line<conan_v2_unified_arguments>`.


.. code-block:: python
   :caption: **From:**

    from conans import ConanFile

    class Pkg(Conanfile):
        default_options = {"pkg:some_option": "value"}


.. code-block:: python
   :caption: **To:**

    from conan import ConanFile

    class Pkg(Conanfile):
        # "pkg/*:some_option" or ""pkg/1.0:some_option" or "pkg*:some_option" would be valid
        default_options = {"pkg/*:some_option": "value"}




The layout() method
-------------------

The layout method is not mandatory but very recommended to:

- Give better support for ``editable`` packages.
- Work with local commands, ``conan install`` + ``conan source`` + ``conan build``.

If your recipe is using CMake, you might want to use the ``cmake_layout(self)``:

  .. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import cmake_layout

    class Pkg(Conanfile):

        def layout(self):
            cmake_layout(self)

A typical anti-pattern in the recipes that can be solved with a ``layout()`` declaration would be:

  .. code-block:: python
     :caption: **From:**

     from conans import ConanFile, tools

     class Pkg(Conanfile):

        @property
        def _source_subfolder(self):
            return "source_subfolder"

        def source(self):
            tools.get(**self.conan_data["sources"][self.version],
                      destination=self._source_subfolder, strip_root=True)


  .. code-block:: python
     :caption: **To:**

     from conan import ConanFile
     from conan.tools.layout import basic_layout
     from conan.tools.files import get

     class Pkg(Conanfile):

        @property
        def layout(self):
            basic_layout(self, src_folder="source")

        def source(self):
            get(self, **self.conan_data["sources"][self.version], strip_root=True)


Declaring the layout, the variables ``self.source_folder``, ``self.build_folder`` will point to the correct folder, both in
the cache or locally when using local methods, it is always recommended to use these when performing disk operations
(read, write, copy, etc).

If you are using ``editables``, the external template files are going to be removed. Use
the ``layout()`` method definition instead.

Read more about the :ref:`layout feature<package_layout>` and the :ref:`reference of the layout() method<layout_method_reference>`.

.. _conanv2_layout_cpp_objects:

Adjusting the cpp_info objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can adjust the cpp_info in the ``layout`` method too, not only for a package in the cache, that was typically done
in the ``package_info()`` method using the ``self.cpp_info``, but for editable packages (to reuse a conan package
that is being developed in a local directory):


.. code-block:: python

    def layout(self):

        # This will be automatically copied to self.cpp_info
        # This information is relative to the self.package_folder
        self.cpp.package.includedirs.append("other_includes")

        # This information is relative to the self.build_folder
        self.cpp.build.libdirs = ["."]
        self.cpp.build.bindirs = ["bin"]

        # This information is relative to the self.source_folder
        self.cpp.source.includedirs = ["."]





The scm attribute
-----------------

The ``scm`` attribute won't exist in Conan 2.0. You have to start using the ``export()`` and ``source()`` methods
to mimic the same behavior:

- The ``export()`` method is responsible for capturing the "coordinates" of the current URL and commit.
  The new ``conan.tools.scm.Git`` can be used for this (do not use the legacy ``Git`` helper but this one)
- The ``export()`` method, after capturing the coordinates, can store them in the ``conandata.yml`` using
  the ``update_conandata()`` helper function
- The ``source()`` method can use the information in ``self.conan_data`` coming from exported ``conandata.yml``
  file to do a clone and checkout of the matching code. The new ``conan.tools.scm.Git`` can be used for this
  purpose.


.. code-block:: python
    :caption: **From:**

    from conans import ConanFile, tools

    class Pkg(Conanfile):

        scm = {
             "type": "git",
             "url": "auto",
             "revision": "auto",
        }


.. code-block:: python
    :caption: **To:**

    from conan import ConanFile
    from conan.tools.scm import Git
    from conan.tools.files import load, update_conandata

    class Pkg(Conanfile):

       def export(self):
           git = Git(self, self.recipe_folder)
           scm_url, scm_commit = git.get_url_and_commit()
           update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

       def source(self):
           git = Git(self)
           sources = self.conan_data["sources"]
           git.clone(url=sources["url"], target=".")
           git.checkout(commit=sources["commit"])



Please **check the full example** on the :ref:`conan.tools.scm.Git section <conan_tools_scm_git>`.



The generate() method
---------------------

This is a key method to understand how Conan 2.0 works. This method is called during the "install" process, before
calling the "build()" method.
All information needed to build the current package has to be calculated and written in disk (in the ``self.generators_folder``)
by the ``generate()`` method. That information is about:

- The dependencies of the recipe: Typically called "generators".
- The configuration (settings, options...): Typically called "toolchains".

The goal of the ``generate()`` method is to have a very simple build process (the more dummy, the better),
calling the build system passing some files or arguments and activating some environment launchers.

This improves a lot the local development, a simple ``conan install`` will generate everything we need to build our
project in the IDE or just call the build system. This example is using the ``CMake`` integration, but if you use
other build systems, even a custom one, remember you should generate everything needed in the ``generate()`` method:


.. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout


    class Pkg(ConanFile):
        ...
        requires = "foo/1.0", "bar/1.0"

        def layout(self):
            cmake_layout(self)

        def generate(self):
            # This generates "conan_toolchain.cmake" in self.generators_folder
            tc = CMakeToolchain(self)
            tc.variables["MYVAR"] = "1"
            tc.preprocessor_definitions["MYDEFINE"] = "2"
            tc.generate()

            # This generates "foo-config.cmake" and "bar-config.cmake" in self.generators_folder
            deps = CMakeDeps(self)
            deps.generate()

        ...

If we are using that recipe for our project we can build it by typing:

.. code-block:: bash

    $ conan install .
    # This will generate the config files from the dependencies and the toolchain
    $ cmake . -DCMAKE_TOOLCHAIN_FILE=./cmake-build-release/conan/conan_toolchain.cmake
    $ cmake --build .

You can check all the generators and toolchains for different build systems in the :ref:`tools reference page<conan_tools>`.

It is also very important to know that every access to the information from the ``dependencies`` must be done in the
``generate()`` method using the `self.dependencies access <https://docs.conan.io/en/latest/reference/conanfile/dependencies.html#dependencies-interface>`_.
Do not use ``self.deps_cpp_info``, ``self.deps_env_info`` or ``self.deps_user_info``, these have been removed in 2.0.


.. note::

    If you don't need to customize anything in a generator you can specify it in the ``generators`` attribute and skip
    using the ``generate()`` method for that:

    .. code-block:: python

        from conan import ConanFile
        from conan.tools.cmake import CMake, cmake_layout


        class Pkg(ConanFile):
            ...
            requires = "foo/1.0", "bar/1.0"
            generators = "CMakeToolchain", "CMakeDeps"
            ...


The build() method
------------------

There is nothing special in the ``build()`` method, just emphasize the concept of ``dummy build`` explained before.


The package() method
--------------------

The ``self.copy`` has been replaced by the explicit tool :ref:`copy<conan_tools_files_copy>`.

.. code-block:: bash
    :caption: **From:**

    def package(self):
        ...
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)


.. code-block:: bash
    :caption: **To:**

    from conan.tools.files import copy

    def package(self):
        ...
        copy(self, "*.h", self.source_folder, join(self.package_folder, "include"), keep_path=False)
        copy(self, "*.lib", self.build_folder, join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.dll", self.build_folder, join(self.package_folder, "bin"), keep_path=False)



The package_info() method
-------------------------

Removed cpp_info defaults in components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are some defaults in the general ``self.cpp_info`` object:

.. code-block:: text

    self.cpp_info.includedirs => ["include"]
    self.cpp_info.libdirs => ["lib"]
    self.cpp_info.resdirs => ["res"]
    self.cpp_info.bindirs => ["bin"]
    self.cpp_info.builddirs => []
    self.cpp_info.frameworkdirs => ["Frameworks"]

If you declare components, you need to explicitly specify these directories, because by default are empty:

.. code-block:: python

    def cpp_info(self):
        self.cpp_info.components["mycomponent"].includedirs = ["my_include"]
        self.cpp_info.components["myothercomponent"].bindirs = ["myother_bin"]


.. note::

    Remember that now is possible to declare the ``cpp_info`` in the :ref:`layout() method<conanv2_layout_cpp_objects>`
    using the ``self.cpp.package`` instead of using ``self.cpp_info`` in the ``package_info()``.


Removed self.user_info
^^^^^^^^^^^^^^^^^^^^^^

Replaced by the ``self.conf_info`` object, much more versatile than the previous ``self.user_info``.
Check the complete usage of :ref:`self.conf_info<conf_in_recipes>`.

Example:

.. code-block:: python
   :caption: **From:**

    import os
    from conans import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0"

        def package_info(self):
            self.user_info.FOO = "bar"


.. code-block:: python
   :caption: **To:**

    import os
    from conans import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0"

        def package_info(self):
            self.conf_info.define("user.myconf:foo", "bar")


In a consumer recipe:

.. code-block:: python

    import os
    from conans import ConanFile

    class Pkg(ConanFile):
        requires = "pkg/1.0"

        def generate(self):
           my_value = self.dependencies[pkg].conf_info.get("user.myconf:foo")
           ...


.. note::

    The consumer recipes will have a ``self.conf`` object available with the aggregated configuration from all the
    recipes in the ``build`` context:

    .. code-block:: python

        from conan import ConanFile

        class Pkg(ConanFile):
            settings = "os", "compiler", "build_type", "arch"
            generators = "CMakeToolchain"
            build_requires = "android_ndk/1.0"

            def generate(self):
                self.output.info("NDK: %s" % self.conf.get("tools.android:ndk_path"))


Removed self.env_info
^^^^^^^^^^^^^^^^^^^^^

The attribute ``self.env_info`` has been replaced by:

- ``self.buildenv_info``: For the dependant recipes, the environment variables will be present during the build process.
- ``self.runenv_info``: For the dependant recipes, environment variables will be present during the runtime.

Read more about how to use them in the :ref:`environment management<conan_tools_env_environment_model>` of Conan 2.0.

Remember that if you want to pass general information to the dependant recipes, you should use the ``self.conf_info``
and not environment variables if they are not supposed to be reused as environment variables in the dependent recipes.


Removed self.cpp_info.builddirs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default value (pointing to the package root folder) form  ``self.cpp_info.builddirs`` has been removed.
Also assigning it will be discouraged because it affects how :ref:`CMakeToolchain<conan-cmake-toolchain>` and
:ref:`CMakeDeps<CMakeDeps>` locate executables, libraries, headers... from the right context (host vs build).

To be prepared for Conan 2.0:

- If you have *cmake modules* or *cmake config files* at the root of the package, it is strongly recommended to move them
  to a subfolder ``cmake`` and assing it: ``self.cpp_info.builddirs = ["cmake"]``
- If you are not assigning any ``self.cpp_info.builddirs`` assign an empty list: ``self.cpp_info.builddirs = []``.
- Instead of appending new values to the default list, assign it: ``self.cpp_info.builddirs = ["cmake"]``


.. _conanv2_properties_model:

New properties model
^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :hidden:

   properties.rst


Using ``.names``, ``.filenames`` and ``.build_modules`` will not work anymore for new
generators, like :ref:`CMakeDeps<CMakeDeps>` and :ref:`PkgConfigDeps<PkgConfigDeps>`.
They have a new way of setting this information using ``set_property`` and
``get_property`` methods of the ``cpp_info`` object (available since Conan 1.36).

.. code-block:: python

    def set_property(self, property_name, value)
    def get_property(self, property_name):

New properties ``cmake_target_name``, ``cmake_file_name``, ``cmake_module_target_name``,
``cmake_module_file_name``, ``pkg_config_name`` and ``cmake_build_modules`` are defined to allow
migrating ``names``, ``filenames`` and ``build_modules`` properties to this model. In Conan 2.0 this
will be the default way of setting these properties for all generators and also passing
custom properties to generators.

.. important::

  The 2 mechanisms are completely independent:

  - Old way using ``.names``, ``.filenames`` will work exclusively for legacy generators like ``cmake_find_package``
  - New properties, like ``set_property("cmake_target_name")`` will work exclusively for new generators
    like ``CMakeDeps``. They have changed to be absolute, and that would break legacy generators.
  - Recipes that want to provide support for both generators need to provide the 2 definitions in their
    ``package_info()``

New properties defined for *CMake* generators family, used by :ref:`CMakeDeps<CMakeDeps>` generator:

- **cmake_file_name** property will define in ``CMakeDeps`` the name of the generated config file (``xxx-config.cmake``)
- **cmake_target_name** property will define the absolute target name in ``CMakeDeps``
- **cmake_module_file_name** property defines the generated filename for modules (``Findxxxx.cmake``)
- **cmake_module_target_name** defines the absolute target name for find modules.
- **cmake_build_modules** property replaces the ``build_modules`` property.
- **cmake_find_mode** will tell :ref:`CMakeDeps<CMakeDeps>` to generate config
  files, modules files, both or none of them, depending on the value set (``config``,
  ``module``, ``both`` or ``none``)


Properties related to *pkg_config*, supported by both legacy :ref:`pkg_config<pkg_config_generator>` and new :ref:`PkgConfigDeps<PkgConfigDeps>`:

- **pkg_config_name** property equivalent to the ``names`` attribute.
- **pkg_config_custom_content** property supported by both generators that will add user-defined content to the
  *.pc* files created by the generator
- **component_version** property supported by both generators that set a custom version to be used
  in the ``Version`` field belonging to the created ``*.pc`` file for that component.

Properties related to *pkg_config*, only supported by new :ref:`PkgConfigDeps<PkgConfigDeps>`:

- **pkg_config_aliases** property sets some aliases of any package/component name for the ``PkgConfigDeps`` generator only,
  it doesn't work in ``pkg_config``. This property only accepts list-like Python objects.

All of these properties, but ``cmake_file_name`` and ``cmake_module_file_name`` can be defined at the
global ``cpp_info`` level or at the component level.

The `set/get_property` model is very useful if you are creating a :ref:`custom generator<custom_generator>`.
Using ``set_property()`` you can pass the parameters of your choice and read them using the
``get_property()`` method inside the generator.

.. code-block:: python

    def package_info(self):
        ...
        # you have created a custom generator that reads the 'custom_property' property and you set here
        # the value to 'prop_value'
        self.cpp_info.components["mycomponent"].set_property("custom_property", "prop_value")
        ...

Please **check a detailed migration guide** in the :ref:`dedicated section <properties_migration>`.


Removed imports() method
------------------------

The ``def imports(self)`` method from the conanfile has been removed. If you need to import files from your
dependencies you can do it in the ``generate(self)`` method with the new ``copy`` tool:


.. code-block:: bash

    from conan.tools.files import copy

    def generate(self):
        for dep in self.dependencies.values():
            copy(self, "*.dylib", dep.cpp_info.libdirs[0], self.build_folder)
            copy(self, "*.dll", dep.cpp_info.libdirs[0], self.build_folder)



Changes in the test_package recipe
----------------------------------

.. _explicit_test_package_requirement:

In Conan 2.0, the ``test_package/conanfile.py`` needs to declare the requirement being tested explicitly.
To be prepared you have to set the attribute ``test_type="explicit"`` (this will be ignored in 2.0) to make Conan
activate the explicit mode, then declaring the requirement using the ``self.tested_reference_str`` that contains the
reference being tested.

.. code-block:: python

    from conan import ConanFile

    class MyTestPkg(ConanFile):
        test_type = "explicit"

        def requirements(self):
            # A regular requirement
            self.requires(self.tested_reference_str)

        def build_requirements(self):
            # If we want to test the package as a tool_require (formerly `test_type = "build_requires"`)
            # Keep both "requires()" and "tool_requires()" if you want to test the same package both as a regular
            # require and a tool_require (formerly `test_type = "build_requires", "requires"`)
            self.tool_requires(self.tested_reference_str)



Other recipe changes
--------------------

The environment management
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _migration_guide_environment:

The environment management has changed quite a bit. In Conan 1.X the environment was managed by modifying the environment
of Python (of the running process), often using the ``environment_append`` tool, which is not available in 2.0 anymore.
In Conan 2.0, all the applied environment variables are managed by script files
(sh, bat) that will be run just before calling the command specified in every ``self.run("mycommand")``.

These "environment launchers" can be organized by scopes. Conan will aggregate all the launchers of the same scope in a single
launcher called ``conan<scope_name>.bat/sh``.

For example, if you need to call your build system, passing some environment variables:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.env import Environment

    class MyTestPkg(ConanFile):
        ...
        def generate(self):
            env = Environment()
            env.define("foo", "var")
            # scope="build" is the default
            envvars = env.vars(self, scope="build")
            # This will generate a my_launcher.sh but also will create a "conan_build.sh" calling "my_launcher.sh"
            envvars.save_script("my_launcher")


        def build(self):
            # by default env="conanbuild"
            self.run("my_build_system.exe", env="conanbuild")


The resulting command executed in the build() method would be something like:

.. code-block:: shell

    $ conan_build.sh && my_build_system.exe

So the environment variable ``foo`` declared in the ``generate()`` method will be automatically passed to the ``my_build_system.exe``.


There are two generators managing the environment, the ``VirtualBuildEnv`` and the ``VirtualRunEnv``. By default, these
generators are automatically declared in Conan 2.0 but you have to explicitly declare them in Conan 1.X otherwise you
can set ``tools.env.virtualenv:auto_use=True`` in the ``global.conf``.


- **VirtualBuildEnv**: It will generate a *conanbuildenv* .bat or .sh script containing environment variables of the build time environment.
  That information is collected from the direct ``tool_requires`` in "build" context recipes from the ``self.buildenv_info``
  definition plus the ``self.runenv_info`` of the transitive dependencies of those ``tool_requires``.

  The scope used by the ``VirtualBuildEnv`` is ``build`` so, as explained before, it will be applied by default before calling any command.

  Check more details :ref:`here<conan_tools_env_virtualbuildenv>`.
- **VirtualRunEnv**: It will generate a *conanrunenv* .bat or .sh script containing environment variables of the run time environment.
  The launcher contains the runtime environment information, anything that is necessary for the environment to actually run
  the compiled executables and applications. The information is obtained from the ``self.runenv_info`` and also automatically
  deducted from the ``self.cpp_info`` definition of the package, to define ``PATH``, ``LD_LIBRARY_PATH``, ``DYLD_LIBRARY_PATH``,
  and ``DYLD_FRAMEWORK_PATH`` environment variables.

  The scope used by the ``VirtualRunEnv`` is ``run`` so if you need that environment applied you need to specify it in the ``self.run``
  command.

  An example of usage of the ``conanrun`` is the test_package of a recipe that builds a shared library:

  .. code-block:: python

        import os
        from conan import ConanFile
        from conan.tools.env import Environment

        class MyTestPkg(ConanFile):
            generators = "VirtualRunEnv"

            ...

            def test(self):
                my_app_path = os.path.join(self.cpp.build.bindirs[0], "my_app")
                # The default env is "conanbuild" but we want the runtime here to locate the shared library
                self.run(my_app_path, env="conanrun")


  Check more details :ref:`here<conan_tools_env_virtualrunenv>`.


Windows Subsystems
^^^^^^^^^^^^^^^^^^

If you want to run commands inside a Windows subsystem (e.g bash from msys2) you have to set the ``self.win_bash=True``
in your recipe, instead of using the deprecated ``self.run(..., win_bash=True)`` from 1.X.

You need to configure how to run the commands with two config variables:

    - **tools.microsoft.bash:subsystem**:  Possible values: 'msys2', 'msys', 'cygwin', 'wsl' and 'sfu'
    - **tools.microsoft.bash:path** (Default "bash"): Path to the shell executable.

Any command run with ``self.run``, if ``self.win_bash == True`` will run the command inside the specified shell.


Symlinks
^^^^^^^^

Conan won't alter any symlink while exporting or packaging files.
If any manipulation to the symlinks is required, the package :ref:`conan.tools.files.symlinks<conan_tools_files_symlinks>`
contains some tools to help with that.






