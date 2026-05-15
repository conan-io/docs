# conan.tools.files.symlinks

<a id="id1"></a>

## conan.tools.files.symlinks.absolute_to_relative_symlinks()

### absolute_to_relative_symlinks(conanfile, base_folder)

Convert the symlinks with absolute paths into relative ones if they are pointing to a file or
directory inside the `base_folder`. Any absolute symlink pointing outside the `base_folder`    will be ignored.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **base_folder** – Folder to be scanned.

## conan.tools.files.symlinks.remove_external_symlinks()

### remove_external_symlinks(conanfile, base_folder)

Remove the symlinks to files that point outside the `base_folder`, no matter if relative or absolute.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **base_folder** – Folder to be scanned.

## conan.tools.files.symlinks.remove_broken_symlinks()

### remove_broken_symlinks(conanfile, base_folder=None)

Remove the broken symlinks, no matter if relative or absolute.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **base_folder** – Folder to be scanned.
