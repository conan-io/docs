Revisions
=========

This sections introduces how doing modifications to a given recipe or source code without explicitly
creating new versions, will still internally track those changes with a mechanism called revisions.


Let's define a simple recipe that could be useful as a header-only library:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.files import copy

    class pkgRecipe(ConanFile):
        name = "revisions"
        version = "1.0"
        package_type = "header-library"

        exports_sources = "include/*"
        def package(self):
            ...


.. code-block:: bash

    # Lets remove all previous "pkg" packages from previous versions
    $ conan remove pkg/* -c
    $ conan create .