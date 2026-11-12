.. _conanfile_dependencies:

Dependencies
============

Introduced in Conan 1.38.

.. warning::

    These tools are **very experimental** and subject to breaking changes.
    It also contains some known bugs regarding ``build_requires``, to be addressed in next Conan 1.39



.. note::

    This is an advanced feature. Most users will not need to use it, it is intended for
    developing new build system integrations and similar purposes.
    For defining dependencies between packages, check the ``requires``, ``build_requires`` and
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

Not all fields of the dependency conanfile are exposed, the current fields are:

- package_folder: The folder location of the dependency package binary
- ref: an object that contains ``name``, ``version``, ``user``, ``channel`` and ``revision`` (recipe revision)
- pref: an object that contains ``ref``, ``package_id`` and ``revision`` (package revision)
- buildenv_info: ``Environment`` object with the information of the environment necessary to build
- runenv_info: ``Environment`` object with the information of the environment necessary to run the app
- new_cpp_info: (name to be changed): includedirs, libdirs, etc for the dependency
- settings: The actual settings values of this dependency
- settings_build: The actual build settings values of this dependency
- options: The actual options values of this dependency
- context: The context (build, host) of this dependency
- conf_info: Configuration information of this dependency, intended to be applied to consumers.
- dependencies: The transitive dependencies of this dependency
- is_build_context: Return ``True`` if ``context == "build"``.


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

- ``require.direct``: boolean, if it is direct dependency or not
- ``require.build``: boolean, if it is a build_require

The ``dependency`` dictionary value is the read-only object described above that access the dependency attributes.

The ``self.dependencies`` contains some helpers to filter based on some criteria:

- ``self.dependencies.host``: Will filter out requires with ``build=True``
- ``self.dependencies.direct_host``: Will filter out requires with ``build=True`` or ``direct=False``
- ``self.dependencies.build``: Will filter out requires with ``build=False``
- ``self.dependencies.direct_build``: Will filter out requires with ``build=False`` or ``direct=False``

They can be used in the same way:

.. code-block:: python

    requires = "zlib/1.2.11", "poco/1.9.4"

    def generate(self):
        cmake = self.dependencies.direct_build["cmake"]
        for require, dependency in self.dependencies.build.items():
            # do something, only build deps here
