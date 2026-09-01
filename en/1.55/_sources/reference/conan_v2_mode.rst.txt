.. _conan_v2_mode:


CONAN_V2_MODE
=============

If defined in the environment, this variable will raise errors whenever a :ref:`Conan 2.0 <conan_v2>` deprecated feature
is used. It is a good mechanism to check the recipes future Conan 2.0 "compliance". Activating it should
not change behavior in any way, just raise error for deprecated things, but if it works, the same
result should be achieved. The number of deprecated features will increase in future Conan 1.X releases,
it could be a good practice to have it activated in some nightly job or the like, to report on current
status of your recipes.

So, if you are ready to experiment add the variable ``CONAN_V2_MODE`` to your
environment and, please, report your feedback about it.


The following is a current known list of features that will change in Conan 2.0 and might start raising
errors if CONAN_V2_MODE is activated:


Changes related to the default configuration
--------------------------------------------

* First level setting `cppstd` is removed.
* Revisions are enabled by default (adds ``revisions_enabled=1`` to *conan.conf*).
* No hooks activated by default.
* SCM data will be stored into *conandata.yml*.
* GCC >= 5 autodetected profile will use ``libstdc++11``.
* Directory ``<cache>/python`` is not added to Python ``sys.path``.


Changes in recipes
------------------

These changes could break existing recipes:

* Forbid access to ``self.cpp_info`` in ``conanfile::package_id()`` method.
* Deprecate ``conanfile::config()`` method.
* Deprecate old ``python_requires`` syntax.
* Forbid access to ``self.info`` in ``conanfile.package()``.
* ``default_options`` are required to be a dictionary.
* Raise if setting ``cppstd`` appears in the recipe.
* Forbid ``self.settings`` and ``self.options`` in ``conanfile::source()`` method.
* Deprecate ``tools.msvc_build_command``.
* Deprecate ``tools.build_sln_command``.
* Deprecate ``cpp_info.cppflags`` (use ``cxxflags`` instead).
* Deprecate environment variables ``CONAN_USERNAME`` and ``CONAN_CHANNEL``.
* ``PYTHONPATH`` is not added automatically to the environment before running consumer functions.
* Attribute ``self.version`` is ensured to be a string in all the functions and scenarios.
* Access to member ``name`` in ``deps_cpp_info`` objects is forbidden, use ``get_name(<generator>)``
  with the name of the generator.


Changes in profiles
-------------------

Could break existing profiles:

* Deprecate ``scopes`` section in profiles.


Other changes
-------------

* Package name used by the ``pkg_config`` generator uses the same rules as any other generator.
  Previously, if it was not explicit, it was using lowercase ``cpp_info.name`` when it was different
  from the package name.
* If ``build_type`` or ``compiler`` are not defined when using build helpers Conan will raise an error.

* New compiler detection algorithm is used (e.g. when running ``conan profile new <name> --detect``).
  Previously, ``<compiler> --version`` was parsed to detect the compiler and its version. Now, using
  ``CONAN_V2_MODE``, Conan will try to detect the compiler and its version via compiler's built-in macro definitions.

.. note::

   More changes will be added, some of them could be reverted and the behavior may
   change without further noticing. If you are using ``CONAN_V2_MODE``, **thanks!** We
   really appreciate your feedback about the future of Conan.
