.. _reference_conanfile_methods_generate:

generate()
==========

This method will run after the computation and installation of the dependency graph. This means that it will
run after a :command:`conan install` command, or when a package is being built in the cache, it will be run before
calling the ``build()`` method.

The purpose of ``generate()`` is to prepare the build, generating the necessary files. These files would typically be:

- Files containing information to locate the dependencies, as ``xxxx-config.cmake`` CMake config scripts, or ``xxxx.props``
  Visual Studio property files.
- Environment activation scripts, like ``conanbuild.bat`` or ``conanbuild.sh``, that define all the necessary environment
  variables necessary for the build.
- Toolchain files, like ``conan_toolchain.cmake``, that contains a mapping between the current Conan settings and options, and the
  build system specific syntax. ``CMakePresets.json`` for CMake users using modern versions.
- General purpose build information, as a ``conanbuild.conf`` file that could contain information for some toolchains like autotools to be used in the ``build()`` method.
- Specific build system files, like ``conanvcvars.bat``, that contains the necessary Visual Studio *vcvars.bat* call for certain
  build systems like Ninja when compiling with the Microsoft compiler.


The idea is that the ``generate()`` method implements all the necessary logic, making both the user manual builds after a :command:`conan install`
very straightforward, and also the ``build()`` method logic simpler. The build produced by a user in their local flow should result in
exactly the same one as the build done in the cache with a ``conan create`` without effort.

Generation of files happens in the ``generators_folder`` as defined by the current layout.

In many cases, the ``generate()`` method might not be necessary, and declaring the ``generators`` attribute could be enough:

.. code:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        generators = "CMakeDeps", "CMakeToolchain"


But the ``generate()`` method can explicitly instantiate those generators, use them conditionally (like using one build system in Windows,
and another build system integration in other platforms), customize them, or provide a complete custom
generation. 

.. code:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain

    class Pkg(ConanFile):

        def generate(self):
            tc = CMakeToolchain(self)
            # customize toolchain "tc"
            tc.generate()
            # Or provide your own custom logic


The current working directory for the ``generate()`` method will be the ``self.generators_folder`` defined in the current layout.

For custom integrations, putting code in a common ``python_require`` would be a good way to avoid repetition in
multiple recipes:

.. code:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain

    class Pkg(ConanFile):

        python_requires = "mygenerator/1.0"

        def generate(self):
            mygen = self.python_requires["mygenerator"].module.MyGenerator(self)
            # customize mygen behavior, like mygen.something= True
            mygen.generate()


In case it is necessary to collect or copy some files from the dependencies, it is also possible to do it in the ``generate()`` method, accessing ``self.dependencies``.
Listing the different include directories, lib directories from a dependency "mydep" would be possible like this:

.. code:: python

    from conan import ConanFile

    class Pkg(ConanFile):

        def generate(self):
            info = self.dependencies["mydep"].cpp_info
            self.output.info("**includedirs:{}**".format(info.includedirs))
            self.output.info("**libdirs:{}**".format(info.libdirs))
            self.output.info("**libs:{}**".format(info.libs))

And copying the shared libraries in Windows and OSX to the current build folder, could be done like:

.. code:: python

    from conan import ConanFile

    class Pkg(ConanFile):

        def generate(self):
            # NOTE: In most cases it is not necessary to copy the shared libraries
            # of dependencies to use them. Conan environment generators that create
            # environment scripts allow to use the shared dependencies without copying
            # them to the current location
            for dep in self.dependencies.values():
                # This code assumes dependencies will only have 1 libdir/bindir, if for some
                # reason they have more than one, it will fail. Use ``dep.cpp_info.libdirs``
                # and ``dep.cpp_info.bindirs`` lists for those cases.
                copy(self, "*.dylib", dep.cpp_info.libdir, self.build_folder)
                # In Windows, dlls are in the "bindir", not "libdir"
                copy(self, "*.dll", dep.cpp_info.bindir, self.build_folder)


.. note::

    **Best practices**

    - Copying shared libraries to the current project in ``generate()`` is not a necessary in most cases, and shouldn't be done as a general approach. Instead, the Conan environment generators, which are enabled by default, will automatically generate environment scripts like ``conanbuild.bat|.sh`` or ``conanrun.bat|.sh`` with the necessary environment variables (``PATH``, ``LD_LIBRARY_PATH``, etc), to correctly locate and use the shared libraries of dependencies at runtime.
    - Accessing dependencies ``self.dependencies["mydep"].package_folder`` is possible, but it will be ``None`` when the dependency "mydep" is in "editable" mode. If you plan to use editable packages, make sure to always reference the ``cpp_info.xxxdirs`` instead.


.. seealso::

    - Follow the :ref:`tutorial about preparing build from source in recipes<creating_packages_preparing_the_build>`.


.. _conan_conanfile_model_dependencies:

self.dependencies
-----------------

Conan recipes provide access to their dependencies via the ``self.dependencies`` attribute.
This attribute is generally used by generators like ``CMakeDeps`` or ``MSBuildDeps`` to
generate the necessary files for the build.

This section documents the ``self.dependencies`` attribute, as it might be used by users
both directly in recipe or indirectly to create custom build integrations and generators.

Dependencies interface
++++++++++++++++++++++

It is possible to access each one of the individual dependencies of the current recipe, with
the following syntax:

.. code-block:: python

    class Pkg(ConanFile):
        requires = "openssl/0.1"

        def generate(self):
            openssl = self.dependencies["openssl"]
            # access to members
            openssl.ref.version
            openssl.ref.revision # recipe revision
            openssl.options
            openssl.settings

            if "zlib" in self.dependencies:
                # do something


Some **important** points:

- All the information is **read only**. Any attempt to modify dependencies information is
  an error and can raise at any time, even if it doesn't raise yet.
- It is not possible either to call any methods or any attempt to reuse code from the dependencies
  via this mechanism.
- This information does not exist in some recipe methods, only in those methods that evaluate
  after the full dependency graph has been computed. It will not exist in ``configure()``, ``config_options``,
  ``export()``, ``export_source()``, ``set_name()``, ``set_version()``, ``requirements()``,
  ``build_requirements()``, ``system_requirements()``, ``source()``, ``init()``, ``layout()``.
  Any attempt to use it in these methods can raise an error at any time.
- At the moment, this information should only be used in ``generate()`` and ``validate()`` methods.
  For any other use, please submit a Github issue.

Not all fields of the dependency conanfile are exposed, the current fields are:

- **package_folder**: The folder location of the dependency package binary
- **recipe_folder**: The folder containing the ``conanfile.py`` (and other exported files) of the dependency
- **recipe_metadata_folder**: The folder containing optional recipe metadata files of the dependency
- **package_metadata_folder**: The folder containing optional package metadata files of the dependency
- **immutable_package_folder**: The folder containing the immutable artifacts when ``finalize()`` method exists
- **ref**: An object that contains ``name``, ``version``, ``user``, ``channel`` and ``revision`` (recipe revision)
- **pref**: An object that contains ``ref``, ``package_id`` and ``revision`` (package revision)
- **buildenv_info**: ``Environment`` object with the information of the environment necessary to build
- **runenv_info**: ``Environment`` object with the information of the environment necessary to run the app
- **cpp_info**: includedirs, libdirs, etc for the dependency.
- **settings**: The actual settings values of this dependency
- **settings_build**: The actual build settings values of this dependency
- **options**: The actual options values of this dependency
- **context**: The context (build, host) of this dependency
- **conf_info**: Configuration information of this dependency, intended to be applied to consumers.
- **dependencies**: The transitive dependencies of this dependency
- **is_build_context**: Return ``True`` if ``context == "build"``.
- **conan_data**: The ``conan_data`` attribute of the dependency that comes from its ``conandata.yml`` file
- **license**: The ``license`` attribute of the dependency
- **description**: The ``description`` attribute of the dependency
- **homepage**: The ``homepage`` attribute of the dependency
- **url**: The ``url`` attribute of the dependency
- **package_type**: The ``package_type`` of the dependency
- **languages**: The ``languages`` of the dependency.


Iterating dependencies
++++++++++++++++++++++

It is possible to iterate in a dict-like fashion all dependencies of a recipe.
Take into account that ``self.dependencies`` contains all the current dependencies,
both direct and transitive. Every upstream dependency of the current one that has some
effect on it, will have an entry in this ``self.dependencies``.

Iterating the dependencies can be done as:

.. code-block:: python

    requires = "zlib/1.2.11", "poco/1.9.4"

    def generate(self):
        for require, dependency in self.dependencies.items():
            self.output.info("Dependency is direct={}: {}".format(require.direct, dependency.ref))

will output:

.. code-block:: bash

    conanfile.py (hello/0.1): Dependency is direct=True: zlib/1.2.11
    conanfile.py (hello/0.1): Dependency is direct=True: poco/1.9.4
    conanfile.py (hello/0.1): Dependency is direct=False: pcre/8.44
    conanfile.py (hello/0.1): Dependency is direct=False: expat/2.4.1
    conanfile.py (hello/0.1): Dependency is direct=False: sqlite3/3.35.5
    conanfile.py (hello/0.1): Dependency is direct=False: openssl/1.1.1k
    conanfile.py (hello/0.1): Dependency is direct=False: bzip2/1.0.8


Where the ``require`` dictionary key is a "requirement", and can contain specifiers of the relation
between the current recipe and the dependency. At the moment they can be:

- ``require.direct``: boolean, ``True`` if it is direct dependency or ``False`` if it is a transitive one.
- ``require.build``: boolean, ``True`` if it is a ``build_require`` in the build context, as ``cmake``.
- ``require.test``: boolean, ``True`` if its a ``build_require`` in the host context (defined with ``self.test_requires()``), as ``gtest``.

The ``dependency`` dictionary value is the read-only object described above that access the dependency attributes.

The ``self.dependencies`` contains some helpers to filter based on some criteria:

- ``self.dependencies.host``: Will filter out requires with ``build=True``, leaving regular dependencies like ``zlib`` or ``poco``.
- ``self.dependencies.direct_host``: Will filter out requires with ``build=True`` or ``direct=False``
- ``self.dependencies.build``: Will filter out requires with ``build=False``, leaving only ``tool_requires`` in the build context, as ``cmake``.
- ``self.dependencies.direct_build``: Will filter out requires with ``build=False`` or ``direct=False``
- ``self.dependencies.test``: Will filter out requires with ``build=True`` or with ``test=False``, leaving only test requirements as ``gtest`` in the host context.


They can be used in the same way:

.. code-block:: python

    requires = "zlib/1.2.11", "poco/1.9.4"

    def generate(self):
        cmake = self.dependencies.direct_build["cmake"]
        for require, dependency in self.dependencies.build.items():
            # do something, only build deps here


Dependencies ``cpp_info`` interface
+++++++++++++++++++++++++++++++++++

The ``cpp_info`` interface is heavily used by build systems to access the data.
This object defines global and per-component attributes to access information like the include
folders:

.. code-block:: python

    def generate(self):
        cpp_info = self.dependencies["mydep"].cpp_info
        cpp_info.includedirs
        cpp_info.libdirs

        cpp_info.components["mycomp"].includedirs
        cpp_info.components["mycomp"].libdirs


All the paths declared in the ``cppinfo`` object (like ``cpp_info.includedirs``) are absolute paths and works whether
the dependency is in the cache or is an :ref:`editable package<editable_packages>`.

.. seealso::

   - :ref:`CppInfo<conan_conanfile_model_cppinfo>` model.
