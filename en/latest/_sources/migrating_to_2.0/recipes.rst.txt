
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


The ``self.requires()`` method allows in 1.X any ``**kwargs``, so something like ``self.requires(..., transitive_headers=True)`` is possible in
Conan 1.X. These ``**kwargs`` don't have any effect at all in Conan 1.X, they are not even checked for correctness. But they are allowed to exist,
so if new requirement traits are used in Conan 2.0, they will not error.


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



- In Conan 2, removing a setting, for example, ``del self.settings.compiler.libcxx`` in
  the ``configure()`` method, will raise an exception if the setting doesn't exist. It has
  to be protected with try/except. The ``self.settings.rm_safe()`` method already
  implements the try/except clause internally. Use it like:

  .. code-block:: python

    def configure(self):
        # it's a C library
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")


Options
-------

default_options
^^^^^^^^^^^^^^^

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
        # "pkg/*:some_option" or ""pkg/1.0:some_option" would be valid
        default_options = {"pkg/*:some_option": "value"}


ANY special value
^^^^^^^^^^^^^^^^^

The special value ``ANY`` has to be declared in a list:

.. code-block:: python
   :caption: **From:**

    from conans import ConanFile

    class Pkg(Conanfile):
        options = {"opt": "ANY"}


.. code-block:: python
   :caption: **To:**

    from conan import ConanFile

    class Pkg(Conanfile):
        options = {"opt": ["ANY"]}


In case the default value is ``None``, then it should be added as possible value to that option:

.. code-block:: python
   :caption: **To:**

    from conan import ConanFile

    class Pkg(Conanfile):
        options = {"opt": [None, "ANY"]}
        default_options = {"opt": None}


The validate() method
---------------------

Use always the ``self.settings`` instead of ``self.info.settings`` and ``self.options`` instead of ``self.info.options``.
The compatibility mechanism are not needed to verify if the configurations of potential ``compatible`` packages
are valid after the graph has been built.

.. code-block:: python
    :caption: **From:**

    class Pkg(Conanfile):

        def validate(self):
            if self.info.settings.os == "Windows":
                raise ConanInvalidConfiguration("This package is not compatible with Windows")


.. code-block:: python
    :caption: **To:**

    class Pkg(Conanfile):

        def validate(self):
            if self.settings.os == "Windows":
                raise ConanInvalidConfiguration("This package is not compatible with Windows")

.. note::

    For recipes where settings are cleared, using ``self.settings`` is still valid. For example,
    this applies to header only recipes that check for a specific ``self.settings.cppstd`` like:

    .. code-block:: python

        def package_id(self):
            self.info.clear()

        def validate(self):
            if self.settings.get_safe("compiler.cppstd"):
                check_min_cppstd(self, 17)

If you are not checking if the resulting binary is valid for the current configuration but need to check if a package
can be built or not for a specific configuration you must use the ``validate_build()`` method using ``self.settings``
and ``self.options`` to perform the checks:


.. code-block:: python

    from conan import ConanFile
    from conan.errors import ConanInvalidConfiguration

    class myConan(ConanFile):
        name = "foo"
        version = "1.0"
        settings = "os", "arch", "compiler"

        def package_id(self):
            # For this package, it doesn't matter what compiler is used for the binary package
            del self.info.settings.compiler

        def validate_build(self):
            # But we know this cannot be built with "gcc"
            if self.settings.compiler == "gcc":
                raise ConanInvalidConfiguration("This doesn't build in GCC")

        def validate(self):
            # We shouldn't check self.info.settings.compiler here because it has been removed in the package_id()
            # so it doesn't make sense to check if the binary is compatible with gcc because the compiler doesn't matter
            pass


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

        def layout(self):
            basic_layout(self, src_folder="source")

        def source(self):
            get(self, **self.conan_data["sources"][self.version], strip_root=True)


When declaring the layout, the variables ``self.source_folder`` and ``self.build_folder`` will point to the correct folder,
both in the cache or locally when using local methods, it is always recommended to use these when performing disk operations
(read, write, copy, etc).

If you are using ``editables``, the external template files are going to be removed.
Use the ``layout()`` method definition instead.

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


cpp_info libdir, bindir, includedir accessors when using layout() in Conan 1.X
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since `Conan 1.53.0 <https://github.com/conan-io/conan/releases/tag/1.53.0>`_ you can
access ``cpp_info.libdirs[0]``, ``cpp_info.bindirs[0]`` and
``cpp_info.includedirs[0]`` using ``cpp_info.libdir``, ``cpp_info.bindir`` and
``cpp_info.includedir``


The scm attribute
-----------------

The ``scm`` attribute won't exist in Conan 2.0. You have to start using the ``export()`` and ``source()`` methods
to mimic the same behavior:

- The ``export()`` method is responsible for capturing the "coordinates" of the current URL and commit.
  The new ``conan.tools.scm.Git`` can be used for this (do not use the legacy ``Git`` helper but this one)
- The ``export()`` method, after capturing the coordinates, can store them in the ``conandata.yml`` using
  the ``update_conandata()`` helper function
- The ``source()`` method can use the information in ``self.conan_data`` coming from the exported ``conandata.yml``
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

The export_sources() method
---------------------------

The ``self.copy`` method has been replaced by the explicit tool
:ref:`copy<conan_tools_files_copy>`. Typically you would copy from the
``conanfile.recipe_folder`` to the ``conafile.export_sources_folder``:

.. code-block:: bash
    :caption: **From:**

    def export_sources(self):
        ...
        self.copy("CMakeLists.txt")


.. code-block:: bash
    :caption: **To:**

    from conan.tools.files import copy

    def export_sources(self):
        ...
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)


.. _conan2_migration_guide_generate:

The generate() method
---------------------

This is a key method to understand how Conan 2.0 works. This method is called during the
Conan "install" step, before calling the :ref:`build()<conan2_migration_guide_build>` method.
All the information needed to build the current package has to be calculated and written in
disk (in the ``self.generators_folder``) by the ``generate()`` method. The goal of the
``generate()`` method is to **prepare the build** generating all the information that
could be needed while running the build step. That means things like:

- Write information about the dependencies for the build system. This is done by
  what we call "generators", which are tools like :ref:`CMakeDeps<CMakeDeps>`,
  :ref:`PkgConfigDeps<PkgConfigDeps>`, :ref:`MSBuildDeps
  <conan_tools_microsoft_msbuilddeps>`, :ref:`XcodeDeps<conan_tools_apple_xcodedeps>`,
  etc.

- Write information about the configuration (settings, options...). This is done by what
  we call "toolchains", which are tools like :ref:`CMakeToolchain<conan-cmake-toolchain>`,
  :ref:`AutotoolsToolchain<conan_tools_gnu_autotools_toolchain>`,
  :ref:`MSBuildToolchain<conan_tools_microsoft_msbuildtoolchain>`,
  :ref:`XcodeToolchain<conan_tools_apple_xcodetoolchain>`, etc.

- Write other files to be used in the build step, like scripts that inject environment
  variables (check the part on how to :ref:`migrate the
  environment<migration_guide_environment>` on this guide), files to pass to the build
  system, etc.

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

    # This will generate the config files from the dependencies and the toolchain
    $ conan install .

    # Windows
    $ cd build
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake
    $ cmake --build . --config=Release

    # Linux
    $ cd build/Release
    $ cmake ../.. -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
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

.. _conan2_migration_guide_build:

The build() method
------------------

There are no relevant changes in how the ``build()`` method works in Conan v2 compared to
v1. Just be aware that the ``generate()`` method should be used to **prepare the build**,
generating information used in the ``build()`` step. Please, learn how to do that in the
section of this guide about the :ref:`generate()<conan2_migration_guide_generate>`
method.

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

.. _conan2_migration_guide_recipes_package_info:

The package_info() method
-------------------------

Changed cpp_info default values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are some defaults in ``self.cpp_info`` object that are not the same in Conan 2.X than in Conan 1.X (except
for ``Conan >= 1.50`` if the ``layout()`` method is declared):

.. code-block:: text

    self.cpp_info.includedirs => ["include"]
    self.cpp_info.libdirs => ["lib"]
    self.cpp_info.resdirs => []
    self.cpp_info.bindirs => ["bin"]
    self.cpp_info.builddirs => []
    self.cpp_info.frameworkdirs => []

If you declare components, the defaults are the same, so you only need to change the defaults if they are not correct.


.. note::

    Remember that it's now possible to declare ``cpp_info`` in the :ref:`layout() method<conanv2_layout_cpp_objects>`
    using ``self.cpp.package`` instead of using ``self.cpp_info`` in the ``package_info()`` method.


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
    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0"

        def package_info(self):
            self.conf_info.define("user.myconf:foo", "bar")


In a consumer recipe:

.. code-block:: python

    import os
    from conan import ConanFile

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

- ``self.buildenv_info``: For the dependent recipes, the environment variables will be present during the build process.
- ``self.runenv_info``: For the dependent recipes, environment variables will be present during the runtime.

Read more about how to use them in the :ref:`environment management<conan_tools_env_environment_model>` of Conan 2.0.

Remember that if you want to pass general information to the dependent recipes, you should use the ``self.conf_info``
and not environment variables if they are not supposed to be reused as environment variables in the dependent recipes.


Removed self.cpp_info.builddirs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default value (pointing to the package root folder) from ``self.cpp_info.builddirs`` has been removed.
Also assigning it will be discouraged because it affects how :ref:`CMakeToolchain<conan-cmake-toolchain>` and
:ref:`CMakeDeps<CMakeDeps>` locate executables, libraries, headers... from the right context (host vs build).

To be prepared for Conan 2.0:

- If you have *cmake modules* or *cmake config files* at the root of the package, it is strongly recommended to move them
  to a subfolder ``cmake`` and assign it: ``self.cpp_info.builddirs = ["cmake"]``
- If you are not assigning any ``self.cpp_info.builddirs`` assign an empty list: ``self.cpp_info.builddirs = []``.
- Instead of appending new values to the default list, assign it: ``self.cpp_info.builddirs = ["cmake"]``


The package_id() method
-----------------------

The ``self.info.header_only()`` method has been replaced with ``self.info.clear()``


.. code-block:: python
   :caption: **From:**

        def package_id(self):
            self.info.header_only()


.. code-block:: python
   :caption: **To:**

        def package_id(self):
            self.info.clear()




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
- **cmake_build_modules** property replaces the ``build_modules`` property. It can't be declared in a component, do it in ``self.cpp_info``.
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

All of these properties, except for ``cmake_file_name`` and ``cmake_module_file_name`` can be defined at the
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



Migrate conanfile.compatible_packages to the new compatibility() method
-----------------------------------------------------------------------

To declare compatible packages in a valid way for both Conan 1.X and 2.0, you should migrate
from using the :ref:`compatible_packages` method to the :ref:`method_compatibility` method.


.. code-block:: python
   :caption: **From:**

        def package_id(self):
            if self.settings.compiler == "gcc" and self.settings.compiler.version == "4.9":
                for version in ("4.8", "4.7", "4.6"):
                    compatible_pkg = self.info.clone()
                    compatible_pkg.settings.compiler.version = version
                    self.compatible_packages.append(compatible_pkg)


.. code-block:: python
   :caption: **To:**

        def compatibility(self):
            if self.settings.compiler == "gcc" and self.settings.compiler.version == "4.9":
                return [{"settings": [("compiler.version", v)]}
                        for v in ("4.8", "4.7", "4.6")]




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
    - **tools.microsoft.bash:active** (Default "None"): Used to define if Conan is already running inside a subsystem (Msys2) terminal.

Any command run with ``self.run``, if ``self.win_bash == True`` will run the command inside the specified shell.
Any command run with ``self.run(..., scope="run")`` if ``self.win_bash_run == True`` will run that command inside the shell.
In both cases running explicitly in the bash shell only happens if ``tools.microsoft.bash:active`` is not True, because
when it is True, it means that Conan is already running inside the shell.


Symlinks
^^^^^^^^

Conan won't alter any symlink while exporting or packaging files.
If any manipulation to the symlinks is required, the package :ref:`conan.tools.files.symlinks<conan_tools_files_symlinks>`
contains some tools to help with that.


New tools for managing system package managers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are some changes you should be aware of if you are migrating from
:ref:`systempackagetool` to the new :ref:`conan_tools_system_package_manager` to prepare
the recipe for Conan 2.0:

* Unlike in ``SystemPackageTool`` that uses ``CONAN_SYSREQUIRES_SUDO`` and is set to ``True``
  as default, the ``tools.system.package_manager:sudo`` configuration is ``False`` by default.
* :ref:`systempackagetool` is initialized with ``default_mode='enabled'`` but for these new
  tools ``tools.system.package_manager:mode='check'`` is set by default.


New package type attribute
^^^^^^^^^^^^^^^^^^^^^^^^^^

The new optional attribute ``package_type``, to help Conan package ID to choose a better default ``package_id_mode``.

.. code-block:: python

        from conan import ConanFile

        class FoobarAppConanfile(ConanFile):
            package_type = "application"


The valid values are:

    - **application**: The package is an application.
    - **library**: The package is a generic library. It will try to determine the type of library (from shared-library, static-library, header-library) reading the self.options.shared (if declared) and the self.options.header_only
    - **shared-library**: The package is a shared library only.
    - **static-library**: The package is a static library only.
    - **header-library**: The package is a header only library.
    - **build-scripts**: The package only contains build scripts.
    - **python-require**: The package is a python require.
    - **unknown**: The type of the package is unknown.


New Conan client version structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``__version__`` variable has been replaced by the ``conan_version`` structure:

.. code-block:: python

        from conan import ConanFile
        from conan import conan_version

        class pkg(ConanFile):
            ...

            if conan_version.major < 2:
                print("Running Conan 1")
            else:
                print("Running Conan 2")
