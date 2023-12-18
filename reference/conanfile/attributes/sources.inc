Sources
+++++++

.. _exports_attribute:

exports
-------


List or tuple of strings with `file names` or
`fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ patterns that should be exported
and stored side by side with the *conanfile.py* file to make the recipe work:
other python files that the recipe will import, some text file with data to read,...


For example, if we have some python code that we want the recipe to use in a ``helpers.py`` file,
and have some text file *info.txt* we want to read and display during the recipe evaluation
we would do something like:

.. code-block:: python

    exports = "helpers.py", "info.txt"

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

    exports = "*.py", "!*tmp.py"


.. seealso::

    - :ref:`Check the export() conanfile.py method<reference_conanfile_methods_export>`.


.. _exports_sources_attribute:

exports_sources
---------------

List or tuple of strings with file names or
`fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ patterns that should be exported
and will be available to generate the package. Unlike the ``exports`` attribute, these files
shouldn't be used by the ``conanfile.py`` Python code, but to compile the library or generate
the final package. And, due to its purpose, these files will only be retrieved if requested
binaries are not available or the user forces Conan to compile from sources.

This is an alternative to getting the sources with the ``source()`` method. Used when we are not packaging a third party
library and we have together the recipe and the C/C++ project:

.. code-block:: python

    exports_sources = "include*", "src*"

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

    exports_sources = "include*", "src*", "!src/build/*"


Note, if the recipe defines the ``layout()`` method and specifies a ``self.folders.source = "src"`` it won't affect
where the files (from the ``exports_sources``) are copied. They will be copied to the base source folder. So, if you
want to replace some file that got into the ``source()`` method, you need to explicitly copy it from the parent folder
or even better, from ``self.export_sources_folder``.

.. code-block:: python

    import os, shutil
    from conan import ConanFile
    from conan.tools.files import save, load

    class Pkg(ConanFile):
        ...
        exports_sources = "CMakeLists.txt"

        def layout(self):
            self.folders.source = "src"
            self.folders.build = "build"

        def source(self):
            # emulate a download from web site
            save(self, "CMakeLists.txt", "MISTAKE: Very old CMakeLists to be replaced")
            # Now I fix it with one of the exported files
            shutil.copy("../CMakeLists.txt", ".")
            shutil.copy(os.path.join(self.export_sources_folder, "CMakeLists.txt", "."))


.. _conan_conanfile_properties_conandata:

conan_data
----------

Read only attribute with a dictionary with the keys and values provided in a
:ref:`conandata.yml<creating_packages_handle_sources_in_packages_conandata>` file format placed
next to the *conanfile.py*. This YAML file is automatically exported with the recipe and automatically loaded with it too.

You can declare information in the *conandata.yml* file and then access it inside any of the methods of the recipe.
For example, a *conandata.yml* with information about sources that looks like this:

.. code-block:: YAML

    sources:
      "1.1.0":
        url: "https://www.url.org/source/mylib-1.0.0.tar.gz"
        sha256: "8c48baf3babe0d505d16cfc0cf272589c66d3624264098213db0fb00034728e9"
      "1.1.1":
        url: "https://www.url.org/source/mylib-1.0.1.tar.gz"
        sha256: "15b6393c20030aab02c8e2fe0243cb1d1d18062f6c095d67bca91871dc7f324a"

.. code-block:: python

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])

source_buildenv
---------------

Boolean attribute to opt-out from using tool requires in the `source()` method.

Setting this attribute to `False` (default value `True`) will prevent Conan from inyecting the VirtualBuildEnv generated environment from tool requires
when executing the `source()` method.

.. code-block:: python
   :emphasize-lines: 4,5,8

    class MyConan:
       name = "mylib"
       version = "1.0.0"
       source_buildenv = False
       tool_requires = "7zip/1.2.0"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        self.run("7z x *.zip -o*")  ## Error! tool require not available
