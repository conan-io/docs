.. _examples_tools_system_consuming_system_packages:

Consuming system requirements only when building a package
==========================================================

In some cases, you may want to consume system requirements only when building a package, but not when installing it.
It can be useful when you want to build a package in a CI/CD pipeline, but you don't want to run the system package
manager when installing the Conan package in a different environment.
For those cases, there are few approaches that can be used to achieve this goal.


Consume a Conan package wrapper for a system package as build requirement
-------------------------------------------------------------------------

In this approach, you can use a Conan package for a :ref:`wrapped system package<examples_tools_system_package_manager>`.
Then, the package can be consumed regularly by the method
:ref:`build_requirements()<reference_conanfile_methods_build_requirements>`.

.. code-block:: python

    from conan import ConanFile

    class MyPackage(ConanFile):
        name = "mypackage"
        settings = "os", "compiler", "build_type", "arch"

        def build_requirements(self):
            self.tool_requires("ncurses/system")

        ...

This ensures that downstream consumers of the package *mypackage* will not directly invoke the system
package manager (e.g., apt-get). Only the direct package consumer of the system wrap package for ``ncurses``
will execute the system package manager when building the package.

Centralizing and wrapping ``ncurses`` in a separated recipe makes it reusable across multiple cases and is
good practice to avoid code duplication.


Consume the system package directly in the build() method
---------------------------------------------------------

In case wanting to run the system package manager only when building the package, but not having a Conan package to
wrap the system library information, it's possible to run the system package manager in the **build()** method:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.system import package_manager

    class MyPackage(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        ...

        def build(self):
            if self.settings.os == "Linux":
                apt = package_manager.Apt(self)
                apt.install(["libncurses-dev"], update=True, check=True)

This way, the system package manager will be called only when building the package, not when installing it.
There is the advantage of not needed to create a separated Conan package to wrap the system library information,
this is a much simpler case, when only a single recipe need to install the system package.

Still, this approach may lead to code duplication if multiple recipes consume the same system package.
It is recommended to use this method sparingly and only for well-contained cases.
