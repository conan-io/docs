.. _conan_tools_cpp_info:

conan.tools.CppInfo
===================

The ``CppInfo`` class represents the basic C++ usage information of a given package, like the ``includedirs``, ``libdirs``, library names, etc. It is the information that the consumers of the package need in order to be able to find the headers and link correctly with the libraries.

The ``self.cpp_info`` object in the ``package_info()`` is a ``CppInfo`` object, so in most cases it will not be necessary to explicitly instantiate it, and using it as explained in :ref:`the package_info()<reference_conanfile_methods_package_info>` section would be enough.


This section describes the other, advanced uses cases of the ``CppInfo``.

Aggregating information in custom generators
--------------------------------------------

.. include:: ../../common/experimental_warning.inc

Some generators, like the built-in ``NMakeDeps``, contains the equivalent to this code, that collapses all information from all dependencies into one single ``CppInfo`` object that aggregates all the information

.. code-block:: python

  from conan.tools import CppInfo
  
  ...
  
  def generate(self):
      aggregated_cpp_info = CppInfo(self)
      deps = self.dependencies.host.topological_sort
      deps = [dep for dep in reversed(deps.values())]
      for dep in deps:
          # We don't want independent components management, so we collapse
          # the "dep" components into one CppInfo called "dep_cppinfo"
          dep_cppinfo = dep.cpp_info.aggregated_components()
          # Then we merge and aggregate this dependency "dep" into the final result
          aggregated_cpp_info.merge(dep_cppinfo)
      
      aggregated_cpp_info.includedirs  # All include dirs from all deps, all components
      aggregated_cpp_info.libs  # All library names from all deps, all components
      aggregated_cpp_info.system_libs # All system-libs from all deps
      ....
      # Creates a file with this information that the build system will use


This aggregation could be useful in cases where the build system cannot easily use independent dependencies or components. For example ``NMake`` or ``Autotools`` mechanism to provide dependencies information would be via ``LIBS``, ``CXXFLAGS`` and similar variables. These variables are global, so passing all the information from all dependencies is the only possibility.

The public documented interface (besides the defined one in :ref:`the package_info()<reference_conanfile_methods_package_info>`) is:

- ``CppInfo(conanfile)``: Constructor. Receives a ``conanfile`` as argument, typically ``self``
- ``aggregated_components()``: return a new ``CppInfo`` object resulting from the aggregation of all the components
- ``merge(other_cppinfo: CppInfo)``: modifies the current ``CppInfo`` object, updating it with the information of the parameter ``other_cppinfo``, allowing to aggregate information from multiple dependencies.

.. _conan_tools_default_config_options:

conan.tools.default_config_options
==================================

.. include:: ../../common/experimental_warning.inc

.. note::

    This tool is automatically called **only** whenever a recipe does not declare a ``config_options()`` method explicitly.

Manage options in `config_options()` method automatically. This tool manages the following options:

- ``fPIC`` (True, False): Option set as a convention to designate "Position Independent Code" flag.
  This option is not intended for Windows, so the tool automatically deletes it if the option is defined in the recipe.

Implementation:

.. code-block:: python

    def default_configure(conanfile):
        if conanfile.options.get_safe("header_only"):
            conanfile.options.rm_safe("fPIC")
            conanfile.options.rm_safe("shared")
        elif conanfile.options.get_safe("shared"):
            conanfile.options.rm_safe("fPIC")

Usage:

.. code-block:: python

    from conan.tools import default_config_options

    def config_options(self):
        default_config_options(self)

.. _conan_tools_default_configure:

conan.tools.default_configure
=============================

.. include:: ../../common/experimental_warning.inc

.. note::

    This tool is automatically called **only** whenever a recipe does not declare a ``configure()`` method explicitly.

Manage options in `configure()` method automatically. This tool manages the following options:

- ``fPIC`` (True, False): Option set as a convention to designate "Position Independent Code" flag.
  This option is removed when there is a ``header_only=True`` option or when ``shared=True``.
- ``shared`` (True, False): Option set as a convention to designate a dynamic library.
  This option is removed when there is a ``header_only=True`` option.

Implementation:

.. code-block:: python

    def default_configure(conanfile):
        if conanfile.options.get_safe("header_only"):
            conanfile.options.rm_safe("fPIC")
            conanfile.options.rm_safe("shared")
        elif conanfile.options.get_safe("shared"):
            conanfile.options.rm_safe("fPIC")

Usage:

.. code-block:: python

    from conan.tools import default_configure

    def configure(self):
        default_configure(self)

.. _conan_tools_default_package_id:

conan.tools.default_package_id
==============================

.. include:: ../../common/experimental_warning.inc

.. note::

    This tool is automatically called **only** whenever a recipe does not declare a ``package_id()`` method explicitly.

Manages settings and options in `package_id()` method automatically.
This tool clears the defined settings and options from the package ID
when the recipe declares an option ``header_only=True`` or when ``package_type`` is ``"header-library"``.

Implementation:

.. code-block:: python

    def default_package_id(conanfile):
        if conanfile.options.get_safe("header_only") or conanfile.package_type is "header-library":
            conanfile.info.clear()

Usage:

.. code-block:: python

    from conan.tools import default_configure

    def package_id(self):
        default_package_id(self)
