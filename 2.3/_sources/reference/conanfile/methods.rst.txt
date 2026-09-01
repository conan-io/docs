.. _reference_conanfile_methods:

Methods
=======

What follows is a list of methods that you can define in your recipes to customize the package creation & consumption processes:

.. toctree::
   :maxdepth: 1
   :hidden:
   
   methods/build
   methods/build_id
   methods/build_requirements
   methods/compatibility
   methods/configure
   methods/config_options
   methods/deploy
   methods/export
   methods/export_sources
   methods/generate
   methods/init
   methods/layout
   methods/package
   methods/package_id
   methods/package_info
   methods/requirements
   methods/set_name
   methods/set_version
   methods/source
   methods/system_requirements
   methods/test
   methods/validate
   methods/validate_build


- :doc:`build() <methods/build>`: Contains the build instructions to build a package from source
- :doc:`build_id() <methods/build_id>`: Allows reusing the same build to create different package binaries
- :doc:`build_requirements() <methods/build_requirements>`: Defines ``tool_requires`` and ``test_requires``
- :doc:`compatibility() <methods/compatibility>`: Defines binary compatibility at the recipe level
- :doc:`configure() <methods/configure>`: Allows configuring settings and options while computing dependencies
- :doc:`config_options() <methods/config_options>`: Configure options while computing dependency graph
- :doc:`deploy() <methods/deploy>`: Deploys (copy from package to user folder) the desired artifacts
- :doc:`export() <methods/export>`: Copies files that are part of the recipe
- :doc:`export_sources() <methods/export_sources>`: Copies files that are part of the recipe sources
- :doc:`generate() <methods/generate>`: Generates the files that are necessary for building the package
- :doc:`init() <methods/init>`: Special initialization of recipe when extending from ``python_requires``
- :doc:`layout() <methods/layout>`: Defines the relative project layout, source folders, build folders, etc.
- :doc:`package() <methods/package>`: Copies files from build folder to the package folder.
- :doc:`package_id() <methods/package_id>`: Defines special logic for computing the binary ``package_id`` identifier
- :doc:`package_info() <methods/package_info>`: Provide information for consumers of this package about libraries, folders, etc.
- :doc:`requirements() <methods/requirements>`: Define the dependencies of the package
- :doc:`set_name() <methods/set_name>`: Dynamically define the name of a package
- :doc:`set_version() <methods/set_version>`: Dynamically define the version of a package.
- :doc:`source() <methods/source>`: Contains the commands to obtain the source code used to build
- :doc:`system_requirements() <methods/system_requirements>`: Call system package managers like Apt to install system packages
- :doc:`test() <methods/test>`: Run some simple package test (exclusive of ``test_package``)
- :doc:`validate() <methods/validate>`: Define if the current package is invalid (cannot work) with the current configuration.
- :doc:`validate_build() <methods/validate_build>`: Define if the current package cannot be created with the current configuration.
