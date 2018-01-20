Using conan
............

How to package header-only libraries?
--------------------------------------
Packaging header-only libraries is similar to other packages, make sure to first read and understand the :ref:`packaging getting started guide<packaging_getting_started>`. The main difference is that the package recipe is typically much simpler. There are different approaches depending if you want conan to run the library unit tests while creating the package or not. Full details :ref:`in this how-to<header_only>`

When to use settings or options?
--------------------------------------
While creating a package you might want to add different configurations and variants of the package.
There are 2 main inputs that define packages: settings and options.
Read about them in :ref:`this section<settings_vs_options>`
