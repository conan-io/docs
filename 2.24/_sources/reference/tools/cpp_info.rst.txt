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
- ``get_sorted_components()``: Get the ordered components of a package, prioritizing those
  with fewer dependencies within the same package. Returns an ``OrderedDict`` of sorted
  components in the format ``{component_name: component}``.
- ``merge(other_cppinfo: CppInfo)``: modifies the current ``CppInfo`` object, updating it with the information of the parameter ``other_cppinfo``, allowing to aggregate information from multiple dependencies.
