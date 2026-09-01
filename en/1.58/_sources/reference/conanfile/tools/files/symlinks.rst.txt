.. _conan_tools_files_symlinks:

conan.tools.files.symlinks
==========================


conan.tools.files.symlinks.absolute_to_relative_symlinks()
----------------------------------------------------------

Available since: `1.44.0 <https://github.com/conan-io/conan/releases/tag/1.44.0>`_

.. code-block:: python

    def absolute_to_relative_symlinks(conanfile, base_folder):


Convert the symlinks with absolute paths into relative ones if they are pointing to a file or directory inside the
'base_folder'. Any absolute symlink pointing outside the 'base_folder' will be ignored.

Parameters:

- **base_folder**: Folder to be scanned.



conan.tools.files.symlinks.remove_external_symlinks()
----------------------------------------------------------

Available since: `1.44.0 <https://github.com/conan-io/conan/releases/tag/1.44.0>`_

.. code-block:: python

    def remove_external_symlinks(conanfile, base_folder):


Remove the symlinks to files that point outside the 'base_folder', no matter if relative or absolute.

Parameters:

- **base_folder**: Folder to be scanned.


conan.tools.files.symlinks.remove_broken_symlinks()
----------------------------------------------------------

Available since: `1.44.0 <https://github.com/conan-io/conan/releases/tag/1.44.0>`_

.. code-block:: python

    def remove_broken_symlinks(conanfile, base_folder):


Remove the broken symlinks, no matter if relative or absolute.

Parameters:

- **base_folder**: Folder to be scanned.