conan.tools.files basic operations
==================================

.. _conan_tools_files_copy:

conan.tools.files.copy()
------------------------

.. currentmodule:: conan.tools.files.copy_pattern

.. autofunction:: copy

Usage:

.. code-block:: python

    def package(self):
        copy(self, "*.h", self.source_folder, os.path.join(self.package_folder, "include"))
        copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))


.. note::

    The files that are **symlinks to files** or **symlinks to folders** with be treated like any other file, so they will only
    be copied if the specified pattern matches with the file.

    At the destination folder, the symlinks will be created pointing to the exact same file or folder, absolute or relative,
    being the responsibility of the user to manipulate the symlink to, for example, transform the symlink into a relative path
    before copying it so it points to the destination folder.

    Check :ref:`here<conan_tools_files_symlinks>` the reference of tools to manage symlinks.


conan.tools.files.load()
------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: load


Usage:

.. code-block:: python

    from conan.tools.files import load

    content = load(self, "myfile.txt")



conan.tools.files.save()
------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: save

Usage:

.. code-block:: python

    from conan.tools.files import save

    save(self, "path/to/otherfile.txt", "contents of the file")




conan.tools.files.rename()
--------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: rename

Usage:

.. code-block:: python

    from conan.tools.files import rename

    def source(self):
        rename(self, "lib-sources-abe2h9fe", "sources")  # renaming a folder


.. _conan_tools_files_replace_in_file:

conan.tools.files.replace_in_file()
-----------------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: replace_in_file


Usage:

.. code-block:: python

    from conan.tools.files import replace_in_file

    replace_in_file(self, os.path.join(self.source_folder, "folder", "file.txt"), "foo", "bar")


conan.tools.files.rm()
----------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: rm


Usage:

.. code-block:: python

    from conan.tools.files import rm

    rm(self, "*.tmp", self.build_folder, recursive=True)



conan.tools.files.mkdir()
-------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: mkdir


Usage:

.. code-block:: python

    from conan.tools.files import mkdir

    mkdir(self, "mydir") # Creates mydir if it does not already exist
    mkdir(self, "mydir") # Does nothing



conan.tools.files.rmdir()
-------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: rmdir


Usage:

.. code-block:: python


    from conan.tools.files import rmdir

    rmdir(self, "mydir") # Remove mydir if it exist
    rmdir(self, "mydir") # Does nothing



conan.tools.files.chdir()
-------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: chdir

Usage:

.. code-block:: python

    from conan.tools.files import chdir

    def build(self):
        with chdir(self, "./subdir"):
            do_something()

.. _conan_tools_files_unzip:

conan.tools.files.unzip()
-------------------------

This function extract different compressed formats (``.tar.gz``, ``.tar``, ``.tzb2``, ``.tar.bz2``, ``.tgz``, ``.txz``,
``tar.xz``, and ``.zip``) into the given destination folder.

It also accepts gzipped files, with extension ``.gz`` (not matching any of the above), and it will unzip them into a file with the same name
but without the extension, or to a filename defined by the ``destination`` argument.

.. code-block:: python

    from conan.tools.files import unzip

    unzip(self, "myfile.zip")
    # or to extract in "myfolder" sub-folder
    unzip(self, "myfile.zip", "myfolder")

You can keep the permissions of the files using the ``keep_permissions=True`` parameter.

.. code-block:: python

    from conan.tools.files import unzip

    unzip(self, "myfile.zip", "myfolder", keep_permissions=True)

Use the ``pattern`` argument if you want to filter specific files and paths to decompress from the archive.

.. code-block:: python

    from conan.tools.files import unzip

    # Extract only files inside relative folder "small"
    unzip(self, "bigfile.zip", pattern="small/*")
    # Extract only txt files
    unzip(self, "bigfile.zip", pattern="*.txt")



.. currentmodule:: conan.tools.files.files

.. autofunction:: unzip


conan.tools.files.update_conandata()
------------------------------------

This function reads the ``conandata.yml`` inside the exported folder in the conan cache, if it exists.
If the ``conandata.yml`` does not exist, it will create it.
Then, it updates the conandata dictionary with the provided ``data`` one, which is updated recursively,
prioritizing the ``data`` values, but keeping other existing ones. Finally the ``conandata.yml`` is saved
in the same place.

This helper can only be used within the ``export()`` method, it can raise otherwise. One application is
to capture in the ``conandata.yml`` the scm coordinates (like Git remote url and commit), to be able to
recover it later in the ``source()`` method and have reproducible recipes that can build from sources
without actually storing the sources in the recipe.

.. currentmodule:: conan.tools.files.conandata

.. autofunction:: update_conandata


conan.tools.files.trim_conandata()
----------------------------------

.. currentmodule:: conan.tools.files.conandata

.. autofunction:: trim_conandata


.. warning::

  The ``conan.tools.files.trim_conandata()`` function is in **preview**.
  See :ref:`the Conan stability<stability>` section for more information.


This function modifies the ``conandata.yml`` inside the exported folder in the conan cache, if it exists,
and keeps only the information related to the currently built version.

This helper can only be used within the ``export()`` method, it can raise otherwise. One application is
to ensure changes in the ``conandata.yml`` file related to some versions do not affect the generated recipe revisions of the rest.

Usage:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import trim_conandata

    class Pkg(ConanFile):
        name = "pkg"

        def export(self):
            # any change to other versions in the conandata.yml
            # won't affect the revision of the version that is built
            trim_conandata(self)


.. _conan_tools_files_collect_libs:

conan.tools.files.collect_libs()
--------------------------------

.. currentmodule:: conan.tools.files

.. autofunction:: collect_libs

.. warning::

    This tool collects the libraries searching directly inside the package folder and returns them in no specific order. If libraries are
    inter-dependent, then ``package_info()`` method should order them to achieve correct linking order.

Usage:

.. code-block:: python

    from conan.tools.files import collect_libs

    def package_info(self):
        self.cpp_info.libdirs = ["lib", "other_libdir"]  # Default value is 'lib'
        self.cpp_info.libs = collect_libs(self)

For UNIX libraries starting with **lib**, like *libmath.a*, this tool will collect the
library name **math**. Regarding symlinks, this tool will keep only the "most generic"
file among the resolved real file and all symlinks pointing to this real file. For example
among files below, this tool will select *libmath.dylib* file and therefore only append
*math* in the returned list: 

.. code-block:: shell

    -rwxr-xr-x libmath.1.0.0.dylib lrwxr-xr-x libmath.1.dylib -> libmath.1.0.0.dylib
    lrwxr-xr-x libmath.dylib -> libmath.1.dylib
