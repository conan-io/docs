
How to check the version of the Conan client inside a conanfile
===============================================================

Sometimes it might be useful to check the Conan version that is running in that moment your recipe.
Although we consider conan-center recipes only forward compatible, this kind of check makes sense to
update them so they can maintain compatibility with old versions of Conan.

Let's have a look at a basic example of this:

.. code-block:: python
   :caption: conanfile.py

    from conans import ConanFile, CMake, __version__ as conan_version
    from conans.model.version import Version


    class MyLibraryConan(ConanFile):
        name = "mylibrary"
        version = "1.0"

        def build(self):
            if conan_version < Version("0.29"):
                cmake = CMake(self.settings)
            else:
                cmake = CMake(self)
        ...

Here it checks the Conan version to maintain compatibility of the CMake build helper for versions
lower than Conan 0.29. It also uses the internal ``Version()`` class to perform the semver
comparison in the if-clause.

You can also use it to take advantage of new features when the client is new enough, for 
example:

.. code-block:: python

    from conans import ConanFile, tools, __version__ as conan_version
    from conans.model.version import Version

    class MyPackage(ConanFile):
        name = "package"
        ...

        def package_id(self):
            if conan_version >= Version("1.20"):
                if self.settings.compiler == "gcc" and self.settings.compiler.version == "4.9":
                    compatible_pkg = self.info.clone()
                    compatible_pkg.settings.compiler.version = "4.8"
                    self.compatible_packages.append(compatible_pkg)


It can be useful to introduce new features in your recipes while all the consumers update
their client version. Together with our :ref:`stability commitment for Conan 1.x<stability>`
it should be easy to adopt new Conan versions while evolving your recipes.
