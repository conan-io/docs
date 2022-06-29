conan.tools.files basic operations
==================================


.. warning::

    These tools are **experimental** and subject to breaking changes.

.. _conan_tools_files_copy:

conan.tools.files.copy()
------------------------

.. code-block:: python

    def copy(conanfile, pattern, src, dst, keep_path=True, excludes=None, ignore_case=True)


Copy the files matching the ``pattern`` (fnmatch) at the ``src`` folder to a ``dst`` folder.

Parameters:
    - **conanfile**: Conanfile object.
    - **pattern**: An fnmatch file pattern of the files that should be copied. It must not start with ``..`` relative path or an exception will be raised.
    - **src**: Source folder in which those files will be searched. This folder will be stripped from the
      dst parameter. E.g., `lib/Debug/x86`.
    - **dst**: Destination local folder. It must be different from ``src`` value or an exception will be raised.
    - **keep_path**: Means if you want to keep the relative path when you copy the files from the **src**
      folder to the **dst** one.
    - **excludes**: A tuple/list of fnmatch patterns or even a single one to be excluded from the copy.
    - **ignore_case**: If enabled, it will do a case-insensitive pattern matching.

.. note::

    The files that are **symlinks to files** or **symlinks to folders** with be treated like any other file, so they will only
    be copied if the specified pattern matches with the file.

    At the destination folder, the symlinks will be created pointing to the exact same file or folder, absolute or relative,
    being the responsibility of the user to manipulate the symlink to, for example, transform the symlink into a relative path
    before copying it so it points to the destination folder.

    Check :ref:`here<conan_tools_files_symlinks>` the reference of tools to manage symlinks.


conan.tools.files.load()
------------------------

.. code-block:: python

    def load(conanfile, path, encoding="utf-8")

Utility function to load files in one line. It will manage the open and close of the file, and load binary encodings. Returns the content of
the file.

.. code-block:: python

    from conan.tools.files import load

    content = load(self, "myfile.txt")

Parameters:
    - **conanfile**: Conanfile object.
    - **path**: Path to the file.
    - **encoding**: Specifies the input file text encoding.


conan.tools.files.save()
------------------------

.. code-block:: python

    def save(conanfile, path, content, append=False, encoding="utf-8"):


Utility function to save files in one line. It will manage the open and close of the file and creating directories if necessary.

.. code-block:: python

    from conan.tools.files import save

    save(self, "path/to/otherfile.txt", "contents of the file")


Parameters:
    - **conanfile**: Conanfile object.
    - **path**: Path to the file.
    - **content**: Content that should be saved into the file.
    - **append**: If ``True``, it will append the content.
    - **encoding**: Specifies the output file text encoding.



conan.tools.files.rename()
--------------------------

.. code-block:: python

    def rename(conanfile, src, dst)

Utility function to rename a file or folder *src* to *dst*. On Windows, it is very common that ``os.rename()`` raises an "Access is denied" exception, so this tool uses:command:`robocopy` if available. If that is not the case, or the rename is done in a non-Windows machine, it falls back to the ``os.rename()`` implementation.

.. code-block:: python

    from conan.tools.files import rename

    def source(self):
        rename(self, "lib-sources-abe2h9fe", "sources")  # renaming a folder

Parameters:
    - **conanfile**: Conanfile object.
    - **src**: Path to be renamed.
    - **dst**: Path to be renamed to.


conan.tools.files.replace_in_file()
-----------------------------------

.. code-block:: python

    def replace_in_file(conanfile, file_path, search, replace, strict=True, encoding="utf-8")


Replace a string ``search`` in the contents of the file ``file_path`` with the string ``replace``.

.. code-block:: python

    from conan.tools.files import replace_in_file

    replace_in_file(self, os.path.join(self.source_folder, "folder", "file.txt"), "foo", "bar")


Parameters:
    - **conanfile**: Conanfile object.
    - **file_path**: File path of the file to perform the replace in.
    - **search**: String you want to be replaced.
    - **replace**: String to replace the searched string.
    - **strict**: If ``True``, it raises an error if the searched string is not found, so nothing is
      actually replaced.
    - **encoding**: Specifies the input and output files text encoding.


conan.tools.files.rm()
----------------------

.. code-block:: python

    def rm(conanfile, pattern, folder, recursive=False)


Remove the files following the ``pattern`` (fnmatch) from the specified ``folder``.

.. code-block:: python

    from conan.tools.files import rm

    rm(self, "*.tmp", self.build_folder, recursive=True)


Parameters:
    - **conanfile**: Conanfile object.
    - **pattern**: Pattern that the files to be removed have to match (fnmatch).
    - **folder**: Folder to search/remove the files.
    - **recursive**: If ``recursive`` is specified it will search in the subfolders.



conan.tools.files.mkdir()
-------------------------

.. code-block:: python

    def mkdir(path)

Utility functions to create a directory. The existence of the specified directory is checked, so ``mkdir()`` will do nothing if the
directory already exists.

.. code-block:: python

    from conan.tools.files import mkdir

    mkdir(self, "mydir") # Creates mydir if it does not already exist
    mkdir(self, "mydir") # Does nothing


Parameters:
    - **conanfile**: Conanfile object.
    - **path**: Path to the directory.


conan.tools.files.rmdir()
-------------------------

.. code-block:: python

    def rmdir(path)

Utility functions to remove a directory. The existence of the specified directory is checked, so ``rmdir()`` will do nothing if the
directory doesn't exists.

.. code-block:: python

    from conan.tools.files import rmdir

    rmdir(self, "mydir") # Remove mydir if it exist
    rmdir(self, "mydir") # Does nothing


Parameters:
    - **conanfile**: Conanfile object.
    - **path**: Path to the directory.


conan.tools.files.chdir()
-------------------------

.. code-block:: python

    def chdir(conanfile, newdir):

This is a context manager that allows to temporary change the current directory in your conanfile:

.. code-block:: python

    from conan.tools.files import chdir

    def build(self):
        with chdir(self, "./subdir"):
            do_something()

Parameters:
    - **conanfile**: Conanfile object.
    - **newdir**: Directory path name to change the current directory.


conan.tools.files.unzip()
-------------------------

.. code-block:: python

    def unzip(conanfile, filename, destination=".", keep_permissions=False, pattern=None,
              strip_root=False):


This function extract different compressed formats (``.tar.gz``, ``.tar``, ``.tzb2``, ``.tar.bz2``, ``.tgz``, ``.txz``,
``tar.xz``, and ``.zip``) into the given destination folder.

It also accepts gzipped files, with extension ``.gz`` (not matching any of the above), and it will unzip them into a file with the same name
but without the extension, or to a filename defined by the ``destination`` argument.

.. code-block:: python

    from conan.tools.files import unzip

    tools.unzip("myfile.zip")
    # or to extract in "myfolder" sub-folder
    tools.unzip("myfile.zip", "myfolder")

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

Parameters:
    - **conanfile**: Conanfile object.
    - **filename**: File to be unzipped.
    - **destination**: Destination folder for unzipped files.
    - **keep_permissions**: Keep permissions of files. **WARNING:** Can be dangerous if the zip
      was not created in a NIX system, the bits could produce undefined permission schema. Use only this option if you are sure that
      the zip was created correctly.
    - **pattern**: Extract from the archive only paths matching the pattern. This should be a Unix
      shell-style wildcard. See `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ documentation for more details.
    - **strip_root**: When ``True`` and the ZIP file contains one folder containing all the contents,
      it will strip the root folder moving all its contents to the root. E.g: *mylib-1.2.8/main.c* will be extracted as *main.c*. If the compressed
      file contains more than one folder or only a file it will raise a ``ConanException``.


conan.tools.files.update_conandata()
------------------------------------

.. code-block:: python

    def update_conandata(conanfile, data)

Parameters:

- **conanfile**: Conanfile object.
- **data**: A dictionary (can be nested), of values to update


This function reads the ``conandata.yml`` inside the exported folder in the conan cache, if it exists.
If the ``conandata.yml`` does not exist, it will create it.
Then, it updates the conandata dictionary with the provided ``data`` one, which is updated recursively,
prioritizing the ``data`` values, but keeping other existing ones. Finally the ``conandata.yml`` is saved
in the same place.

This helper can only be used within the ``export()`` method, it can raise otherwise. One application is
to capture in the ``conandata.yml`` the scm coordinates (like Git remote url and commit), to be able to
recover it later in the ``source()`` method and have reproducible recipes that can build from sources
without actually storing the sources in the recipe.

Example:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import update_conandata

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"

        def export(self):
            # This is an example, doesn't make sense to have static data, instead you
            # could put the data directly in a conandata.yml file.
            # This would be useful for storing dynamic data, obtained at export() time from elsewhere
            update_conandata(self, {"mydata": {"value": {"nested1": 123, "nested2": "some-string"}}})
    
        def source(self):
            data = self.conan_data["sources"]["mydata"]
