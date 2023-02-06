.. _reference_conanfile_methods_validate_build:


validate_build()
================

The ``validate_build()`` method is used to verify if a configuration is valid for building a package. It is different
from the ``validate()`` method that checks if the binary package is "impossible" or invalid for a given configuration.

The ``validate()`` method should do the checks of the settings and options using the ``self.info.settings``
and ``self.info.options``.

The ``validate_build()`` method has to use always the ``self.settings`` and ``self.options``:

.. code-block:: python

    from conan import ConanFile
    from conan.errors import ConanInvalidConfiguration
    class myConan(ConanFile):
        name = "foo"
        version = "1.0"
        settings = "os", "arch", "compiler"
        def package_id(self):
            # For this package, it doesn't matter the compiler used for the binary package
            del self.info.settings.compiler
        def validate_build(self):
            # But we know this cannot be build with "gcc"
            if self.settings.compiler == "gcc":
                raise ConanInvalidConfiguration("This doesn't build in GCC")
        def validate(self):
            # We shouldn't check here the self.info.settings.compiler because it has been removed in the package_id()
            # so it doesn't make sense to check if the binary is compatible with gcc because the compiler doesn't matter
            pass
