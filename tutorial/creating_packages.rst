.. _tutorial_creating_packages:

Creating packages
=================

This section shows how to create Conan packages using a Conan recipe. We begin by creating
a basic Conan recipe to package a simple C++ library that you can scaffold using the
:command:`conan new` command. Then, we will explain the different methods that you can
define inside a Conan recipe and the things you can do inside them:

* Using the ``source()`` method to retrieve sources from external repositories and apply
  patches to those sources.

* Add requirements to your Conan packages inside the ``requirements()`` method. 

* Use the ``generate()`` method to prepare the package build, and customize the toolchain.

* Configure settings and options in the ``configure()`` and ``config_options()``
  methods and how they affect the packages' binary compatibility.

* Use the ``build()`` method to customize the build process and launch the tests for the
  library you are packaging. 

* Select which files will be included in the Conan package using the ``package()`` method.

* Define the package information in the ``package_info()`` method so that consumers
  of this package can use it.

* Use a *test_package* to test that the Conan package can be consumed correctly.

After this walkthrough around some Conan recipe methods, we will explain some
peculiarities of different types of Conan packages like, for example, header-only
libraries, packages for pre-built binaries, packaging tools for building other packages or
packaging your own applications.

.. toctree::
   :maxdepth: 2
   :caption: Table of contents
   
   creating_packages/create_your_first_package
   creating_packages/handle_sources_in_packages
   creating_packages/add_dependencies_to_packages
   creating_packages/preparing_the_build
   creating_packages/configure_options_settings
   creating_packages/build_packages
   creating_packages/package_method
   creating_packages/define_package_information
   creating_packages/test_conan_packages
   creating_packages/other_types_of_packages
