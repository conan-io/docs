.. _conanfile_dependencies:

Dependencies
============

.. important::

    This feature is still **under development**, while it is recommended and usable and we will try not to break them in future releases,
    some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.

Available since: `1.38.0 <https://github.com/conan-io/conan/releases/tag/1.38.0>`_

.. note::

    This is an advanced feature. Most users will not need to use it, it is intended for
    developing new build system integrations and similar purposes.
    For defining dependencies between packages, check the ``requires``, ``tool_requires`` and
    other attributes


Conan recipes provide access to their dependencies via the ``self.dependencies`` attribute.
This attribute is extensively used by generators like ``CMakeDeps`` or ``MSBuildDeps`` to
generate the necessary files for the build.

This section documents the ``self.dependencies`` attribute, as it might be used by users
both directly in recipe or indirectly to create custom build integrations and generators.

Dependencies interface
----------------------

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
  Any other use, please submit a Github issue.

The exposed fields of the dependency conanfile are:

- package_folder: The folder location of the dependency package binary
- recipe_folder: The folder containing the ``conanfile.py`` (and other exported files) of the dependency
- ref: an object that contains ``name``, ``version``, ``user``, ``channel`` and ``revision`` (recipe revision)
- pref: an object that contains ``ref``, ``package_id`` and ``revision`` (package revision)
- buildenv_info: ``Environment`` object with the information of the environment necessary to build
- runenv_info: ``Environment`` object with the information of the environment necessary to run the app
- cpp_info: includedirs, libdirs, etc for the dependency.
- settings: The actual settings values of this dependency
- settings_build: The actual build settings values of this dependency
- options: The actual options values of this dependency
- context: The context (build, host) of this dependency
- conf_info: Configuration information of this dependency, intended to be applied to consumers.
- dependencies: The transitive dependencies of this dependency
- is_build_context: Return ``True`` if ``context == "build"``.
- conan_data: The ``conan_data`` attribute of the dependency that comes from its ``conandata.yml`` file
- license: The ``license`` attribute of the dependency
- description: The ``description`` attribute of the dependency
- homepage: The ``homepage`` attribute of the dependency
- url: The ``url`` attribute of the dependency



Iterating dependencies
----------------------

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

These are the defined attributes in ``cpp_info``. All the paths are typically relative paths to
the root of the package folder that contains the dependency artifacts:

.. code-block:: python

    # ###### DIRECTORIES
    self.includedirs = None  # Ordered list of include paths
    self.srcdirs = None  # Ordered list of source paths
    self.libdirs = None  # Directories to find libraries
    self.resdirs = None  # Directories to find resources, data, etc
    self.bindirs = None  # Directories to find executables and shared libs
    self.builddirs = None
    self.frameworkdirs = None

    # ##### FIELDS
    self.system_libs = None  # Ordered list of system libraries
    self.frameworks = None  # Macos .framework
    self.libs = None  # The libs to link against
    self.defines = None  # preprocessor definitions
    self.cflags = None  # pure C flags
    self.cxxflags = None  # C++ compilation flags
    self.sharedlinkflags = None  # linker flags
    self.exelinkflags = None  # linker flags
    self.objects = None  # objects to link
