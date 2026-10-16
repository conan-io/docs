.. _reference_conanfile_methods_validate_build:


validate_build()
================

The ``validate_build()`` method is used to verify if a package binary can be **built** with the current configuration. It is different than the ``validate()`` method which raises when the package cannot be **used** with the current configuration.


The ``validate_build()`` method can check the ``self.settings`` and ``self.options`` values to raise ``ConanInvalidConfiguration`` if necessary.

.. code-block:: python

    from conan import ConanFile
    from conan.errors import ConanInvalidConfiguration

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0"
        settings = "os", "arch", "compiler", "build_type"

        def package_id(self):
            # For this package, it doesn't matter the compiler used for the binary package
            del self.info.settings.compiler

        def validate_build(self):
            # But we know this cannot be build with "gcc"
            if self.settings.compiler == "gcc":
                raise ConanInvalidConfiguration("This doesn't build in GCC")

This package cannot be created with the ``gcc`` compiler, but it can be created with other:

.. code-block:: text

    $ conan create . -s compiler=gcc
    ...
    ERROR: There are invalid packages:
    pkg/1.0: Cannot build for this configuration: This doesn't build in GCC

    $ conan create . -s compiler=clang  # WORKS!

Once the package has been built, it can be consumed with that compiler:

.. code-block:: bash

    $ conan install --requires=pkg/1.0 -s compiler=gcc # WORKS!
