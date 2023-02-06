.. _reference_conanfile_methods_validate_build:


validate_build()
================

The ``validate_build()`` method is used to verify if a configuration is valid for building a package. It is different
from the ``validate()`` method which checks if the binary package is "impossible" or invalid for a given configuration.


The ``validate_build()`` method has to always use the ``self.settings`` and ``self.options`` attributes:

.. code-block:: python

    from conan import ConanFile
    from conan.errors import ConanInvalidConfiguration

    class Pkg(ConanFile):
        name = "foo"
        version = "1.0"
        settings = "os", "arch", "compiler", "build_type"

        def package_id(self):
            # For this package, it doesn't matter the compiler used for the binary package
            del self.info.settings.compiler

        def validate_build(self):
            # But we know this cannot be build with "gcc"
            if self.settings.compiler == "gcc":
                raise ConanInvalidConfiguration("This doesn't build in GCC")
