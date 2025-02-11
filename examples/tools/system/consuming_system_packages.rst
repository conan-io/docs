.. _examples_tools_system_consuming_system_packages:

Consuming system requirements only when building a package
==========================================================

In some cases, you may want to consume system requirements only when building a package, but not when installing it.
It can be useful when you want to build a package in a CI/CD pipeline, but you don't want to run the system package
manager when installing the Conan package in a different environment.
For those cases, there are few approaches that can be used to achieve this goal.


Consume a Conan package wrapper for a system package using hidden visibility
----------------------------------------------------------------------------

In this approach, you can use a Conan recipe to :ref:`wrap the system package<examples_tools_system_package_manager>`
via the :ref:`system_requirements()<reference_conanfile_methods_system_requirements>` method,
making it available as a Conan package. Then, the package can be consumed regularly by the method
:ref:`requirements()<reference_conanfile_methods_requirements>`, but with the parameter ``visible=False``.

.. code-block:: python

    from conan import ConanFile

    class MyPackage(ConanFile):
        name = "mypackage"
        settings = "os", "compiler", "build_type", "arch"

        def requirements(self):
            self.requires("ncurses/system", visible=False)

        ...

This ensures that downstream consumers of the package *mypackage* will not directly invoke the system package manager (e.g., apt-get).
Only the direct package consumer of the system wrap package for ``ncurses`` will execute the system package manager.

Centralizing and wrapping ``ncurses`` in a single recipe, as mentioned in this example, makes it reusable across multiple
cases and is good practice to avoid code duplication.


Package the system requirement as a header-library or consume only the headers
------------------------------------------------------------------------------

This solution is similar to the previous one, but for those cases when only needing to consume the headers of a system
package, for instance, when needed to use a define or macro available only in the system package headers.

When wrapping a system package as a Conan package, it is possible to define the
:ref:`package_type <reference_conanfile_package_type_trait_inferring>` as ``header-library``.

.. code-block:: python

    from conan import ConanFile

    class NCursesWrapPackage(ConanFile):
        name = "ncurses"
        version = "system"
        settings = "os", "compiler", "build_type", "arch"
        package_type = "header-library"

        def system_requirements(self):
            apt = package_manager.Apt(self)
            apt.install(["libncurses-dev"], update=True, check=True)

        ...

Then, the direct package consumer can require the wrapped package as a header-library:

.. code-block:: python

    from conan import ConanFile

    class MyPackage(ConanFile):
        name = "mypackage"
        settings = "os", "compiler", "build_type", "arch"

        def requirements(self):
            self.requires("ncurses/system", libs=False)

        ...

The direct consumer package *mypackage* will only see the header files provided by the system ``ncurses``.
The Conan package *mypackage*  will forward the Conan wrap package for *ncurses* as a dependency but will not
invoke the system package manager due to the ``header-library`` package type, nor propagating libraries linkage due to
its **trait interfering**.


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
There is the advantage of not needed to create a Conan package to wrap the system library information,
this is a much simpler case, when only a single recipe need to install the system package.

Still, this approach may lead to code duplication if multiple recipes consume the same system package.
It is recommended to use this method sparingly and only for well-contained cases.
