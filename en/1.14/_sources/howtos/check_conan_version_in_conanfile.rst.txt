
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
comparison in the if clause.

You can find a real example of this in the
`mingw_installer <https://github.com/conan-community/conan-mingw-installer>`_. Here you have the
interesting part of the recipe:

.. code-block:: python
   :caption: conanfile.py

    from conans import ConanFile, tools, __version__ as conan_version
    from conans.model.version import Version


    class MingwInstallerConan(ConanFile):
        name = "mingw_installer"
        version = "1.0"
        license = "http://www.mingw.org/license"
        url = "http://github.com/conan-community/conan-mingw-installer"

        if conan_version < Version("0.99"):
            os_name = "os"
            arch_name = "arch"
        else:
            os_name = "os_build"
            arch_name = "arch_build"

        settings = {os_name: ["Windows"],
                    arch_name: ["x86", "x86_64"],
                    "compiler": {"gcc": {"version": None,
                                        "libcxx": ["libstdc++", "libstdc++11"],
                                        "threads": ["posix", "win32"],
                                        "exception": ["dwarf2", "sjlj", "seh"]}}}
        ...

You can see here the ``mingw_installer`` recipe uses new settings ``os_build`` and ``arch_build``
since Conan 1.0 as those are the right ones for
:ref:`installer packages <create_installer_packages>`. However, it also keeps the old settings so as
not to break the recipe for old version, using normal ``os`` and ``arch``.

As said before, this is useful to maintain recipe compatibility with older Conan versions but
remember that since Conan 1.0 there should not be :ref:`any breaking changes<stability>`.
