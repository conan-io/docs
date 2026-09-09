# conan.tools.files basic operations

<a id="conan-tools-files-copy"></a>

## conan.tools.files.copy()

### copy(conanfile, pattern, src, dst, keep_path=True, excludes=None, ignore_case=True, overwrite_equal=False)

Copy the files matching the pattern (fnmatch) at the src folder to a dst folder.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **pattern** – (Required) An fnmatch file pattern of the files that should be copied.
    It must not start with `..` relative path or an exception will be raised.
  * **src** – (Required) Source folder in which those files will be searched. This folder
    will be stripped from the dst parameter. E.g., lib/Debug/x86.
  * **dst** – (Required) Destination local folder. It must be different from src value or an
    exception will be raised.
  * **keep_path** – (Optional, defaulted to `True`) Means if you want to keep the relative
    path when you copy the files from the src folder to the dst one.
  * **excludes** – (Optional, defaulted to `None`) A tuple/list of fnmatch patterns or even a
    single one to be excluded from the copy.
  * **ignore_case** – (Optional, defaulted to `True`) If enabled, it will do a
    case-insensitive pattern matching. will do a case-insensitive pattern matching when
    `True`
  * **overwrite_equal** – (Optional, default `False`). If the file to be copied already exists
    in the destination folder, only really copy it if it seems different (different size,
    different modification time)
* **Returns:**
  list of copied files

Usage:

```python
def package(self):
    copy(self, "*.h", self.source_folder, os.path.join(self.package_folder, "include"))
    copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))
```

#### NOTE
The files that are **symlinks to files** or **symlinks to folders** with be treated like any other file, so they will only
be copied if the specified pattern matches with the file.

At the destination folder, the symlinks will be created pointing to the exact same file or folder, absolute or relative,
being the responsibility of the user to manipulate the symlink to, for example, transform the symlink into a relative path
before copying it so it points to the destination folder.

Check [here](https://docs.conan.io/2//reference/tools/files/symlinks.html.md#id1) the reference of tools to manage symlinks.

## conan.tools.files.load()

### load(conanfile, path, encoding='utf-8')

Utility function to load files in one line. It will manage the open and close of the file,
and load binary encodings. Returns the content of the file.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **path** – Path to the file to read
  * **encoding** – (Optional, Defaulted to `utf-8`): Specifies the input file text encoding.
* **Returns:**
  The contents of the file

Usage:

```python
from conan.tools.files import load

content = load(self, "myfile.txt")
```

## conan.tools.files.save()

### save(conanfile, path, content, append=False, encoding='utf-8')

Utility function to save files in one line. It will manage the open and close of the file
and creating directories if necessary.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **path** – Path of the file to be created.
  * **content** – Content (str or bytes) to be write to the file.
  * **append** – (Optional, Defaulted to False): If `True` the contents will be appended to the
    existing one.
  * **encoding** – (Optional, Defaulted to utf-8): Specifies the output file text encoding.

Usage:

```python
from conan.tools.files import save

save(self, "path/to/otherfile.txt", "contents of the file")
```

## conan.tools.files.rename()

### rename(conanfile, src, dst)

Utility functions to rename a file or folder src to dst with retrying. `os.rename()`
frequently raises “Access is denied” exception on Windows.
This function renames file or folder using robocopy to avoid the exception on Windows.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **src** – Path to be renamed.
  * **dst** – Path to be renamed to.

Usage:

```python
from conan.tools.files import rename

def source(self):
    rename(self, "lib-sources-abe2h9fe", "sources")  # renaming a folder
```

<a id="conan-tools-files-replace-in-file"></a>

## conan.tools.files.replace_in_file()

### replace_in_file(conanfile, file_path, search, replace, strict=True, encoding='utf-8')

Replace a string `search` in the contents of the file `file_path` with the string replace.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **file_path** – File path of the file to perform the replacing.
  * **search** – String you want to be replaced.
  * **replace** – String to replace the searched string.
  * **strict** – (Optional, Defaulted to `True`) If `True`, it raises an error if the searched
    string is not found, so nothing is actually replaced.
  * **encoding** – (Optional, Defaulted to utf-8): Specifies the input and output files text
    encoding.
* **Returns:**
  `True` if the pattern was found, `False` otherwise if strict is `False`.

Usage:

```python
from conan.tools.files import replace_in_file

replace_in_file(self, os.path.join(self.source_folder, "folder", "file.txt"), "foo", "bar")
```

## conan.tools.files.chmod()

### chmod(conanfile, path: str, read: bool | None = None, write: bool | None = None, execute: bool | None = None, recursive: bool = False)

Change file or directory permissions cross-platform.

#### Versionadded
New in version 2.15.

This function is a simple wrapper around the chmod Unix command, but it is cross-platform supported.
It is indicated to use it instead of os.stat + os.chmod, as it only changes the permissions of the
directory or file for the owner and avoids issues with the umask.
On Windows is limited to changing write permission only.

### Parameters

conanfile
: The current recipe object. Always use `self`.

path
: Path to the file or directory whose permissions will be changed.

read
: If `True`, the file or directory will be given read permissions for owner user.
  If `False`, the read permission will be removed.
  If `None`, the read permission will be left unchanged.
  Defaults to None.

write
: If `True`, the file or directory will be given write permissions for owner user.
  If `False`, the write permission will be removed.
  If `None`, the file or directory will not be changed.
  Defaults to None.

execute
: If `True`, the file or directory will be given execute permissions for owner user.
  If `False`, the execution permission will be removed.
  If `None`, the file or directory will not be changed.
  Defaults to None.

recursive
: If `True`, the permissions will be applied recursively to all files and directories
  inside the specified directory. If `False`, only the specified file or directory will
  be changed. Defaults to False.

### Returns

None

### Examples

```python
from conan.tools.files import chmod
chmod(self, os.path.join(self.package_folder, "bin", "script.sh"), execute=True)
```

## conan.tools.files.rm()

This function removes files from the filesystem. It can be used to remove a single file or a pattern based on fnmatch.
It’s indicated to use it instead of `os.remove` because it’s cross-platform and may avoid permissions issues.

```python
from conan.tools.files import rm

rm(self, "*.tmp", self.build_folder, recursive=True)
```

```python
from conan.tools.files import rm

rm(self, "*", self.bin_folder, recursive=False, excludes="*.dll")
```

### rm(conanfile, pattern, folder, recursive=False, excludes=None)

Utility functions to remove files matching a `pattern` in a `folder`.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **pattern** – Pattern that the files to be removed have to match (fnmatch).
  * **folder** – Folder to search/remove the files.
  * **recursive** – If `recursive` is specified it will search in the subfolders.
  * **excludes** – (Optional, defaulted to None) A tuple/list of fnmatch patterns or even a
    single one to be excluded from the remove pattern.

## conan.tools.files.mkdir()

### mkdir(conanfile, path)

Utility functions to create a directory. The existence of the specified directory is checked,
so mkdir() will do nothing if the directory already exists.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **path** – Path to the folder to be created.

Usage:

```python
from conan.tools.files import mkdir

mkdir(self, "mydir") # Creates mydir if it does not already exist
mkdir(self, "mydir") # Does nothing
```

## conan.tools.files.rmdir()

### rmdir(conanfile, path)

Usage:

```python
from conan.tools.files import rmdir

rmdir(self, "mydir") # Remove mydir if it exist
rmdir(self, "mydir") # Does nothing
```

## conan.tools.files.chdir()

### chdir(conanfile, newdir)

This is a context manager that allows to temporary change the current directory in your conanfile

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **newdir** – Directory path name to change the current directory.

Usage:

```python
from conan.tools.files import chdir

def build(self):
    with chdir(self, "./subdir"):
        do_something()
```

<a id="conan-tools-files-unzip"></a>

## conan.tools.files.unzip()

This function extract different compressed formats (`.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tbz2`, `.tar.xz`, `.txz`,
and `.zip`) into the given destination folder.

It also accepts gzipped files, with extension `.gz` (not matching any of the above), and it will unzip them into a file with the same name
but without the extension, or to a filename defined by the `destination` argument.

```python
from conan.tools.files import unzip

unzip(self, "myfile.zip")
# or to extract in "myfolder" sub-folder
unzip(self, "myfile.zip", "myfolder")
```

You can keep the permissions of the files using the `keep_permissions=True` parameter.

```python
from conan.tools.files import unzip

unzip(self, "myfile.zip", "myfolder", keep_permissions=True)
```

Use the `pattern` argument if you want to filter specific files and paths to decompress from the archive.

```python
from conan.tools.files import unzip

# Extract only files inside relative folder "small"
unzip(self, "bigfile.zip", pattern="small/*")
# Extract only txt files
unzip(self, "bigfile.zip", pattern="*.txt")
```

#### IMPORTANT
In Conan 2.8 `unzip()` provides a new `extract_filter=None` argument and a new
`tools.files.unzip:filter` configuration was added to prepare for future Python 3.14
breaking changes, in which the `data` filter for extracting tar archives will be made the default.
The recommendation is to start using the `data` filter as soon as possible (the conf can be
defined in `global.conf`, or it can be explicitly added as argument in recipes `unzip()` and `get()`
helpers) as that is the current security recommendation while downloading sources from the internet.

### unzip(conanfile, filename, destination='.', keep_permissions=False, pattern=None, strip_root=False, extract_filter=None, excludes=None)

Extract different compressed formats

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **filename** – Path to the compressed file.
  * **destination** – (Optional, Defaulted to `.`) Destination folder (or file for .gz files)
  * **keep_permissions** – (Optional, Defaulted to `False`) Keep the zip permissions.
    WARNING: Can be dangerous if the zip was not created in a NIX system, the bits could
    produce undefined permission schema. Use this option only if you are sure that the zip
    was created correctly.
  * **pattern** – (Optional, Defaulted to `None`) Extract only paths matching the pattern.
    This should be a Unix shell-style wildcard, see fnmatch documentation for more details.
  * **strip_root** – (Optional, Defaulted to False) If True, and all the unzipped contents are
    in a single folder it will flat the folder moving all the contents to the parent folder.
  * **extract_filter** – (Optional, defaulted to None). When extracting a tar file,
    use the tar extracting filters define by Python in
    [https://docs.python.org/3/library/tarfile.html](https://docs.python.org/3/library/tarfile.html)
  * **excludes** – (Optional, defaulted to None). When extracting a file,
    exclude paths matching any of the patterns. This should be a Unix shell-style wildcard,
    see fnmatch documentation for more details.

## conan.tools.files.update_conandata()

This function reads the `conandata.yml` inside the exported folder in the conan cache, if it exists.
If the `conandata.yml` does not exist, it will create it.
Then, it updates the conandata dictionary with the provided `data` one, which is updated recursively,
prioritizing the `data` values, but keeping other existing ones. Finally the `conandata.yml` is saved
in the same place.

This helper can only be used within the `export()` method, it can raise otherwise. One application is
to capture in the `conandata.yml` the scm coordinates (like Git remote url and commit), to be able to
recover it later in the `source()` method and have reproducible recipes that can build from sources
without actually storing the sources in the recipe.

### update_conandata(conanfile, data)

Tool to modify the `conandata.yml` once it is exported. It can be used, for example:

> - To add additional data like the “commit” and “url” for the scm.
> - To modify the contents cleaning the data that belong to other versions (different
>   from the exported) to avoid changing the recipe revision when the changed data doesn’t
>   belong to the current version.
* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **data** – (Required) A dictionary (can be nested), of values to update

## conan.tools.files.trim_conandata()

### trim_conandata(conanfile, raise_if_missing=True)

Tool to modify the `conandata.yml` once it is exported, to limit it to the current version
only

#### WARNING
The `conan.tools.files.trim_conandata()` function is in **preview**.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

This function modifies the `conandata.yml` inside the exported folder in the conan cache, if it exists,
and keeps only the information related to the currently built version.

This helper can only be used within the `export()` method or `post_export()` [hook](https://docs.conan.io/2//reference/extensions/hooks.html.md#reference-extensions-hooks),
it may raise in the future otherwise. One application is to ensure changes in the `conandata.yml` file
related to some versions do not affect the generated recipe revisions of the rest.

Usage:

```python
from conan import ConanFile
from conan.tools.files import trim_conandata

class Pkg(ConanFile):
    name = "pkg"

    def export(self):
        # any change to other versions in the conandata.yml
        # won't affect the revision of the version that is built
        trim_conandata(self)
```

<a id="conan-tools-files-collect-libs"></a>

## conan.tools.files.collect_libs()

### collect_libs(conanfile, folder=None)

Returns a sorted list of library names from the libraries (files with extensions  *.so*,  *.lib*,
 *.a* and  *.dylib*) located inside the `conanfile.cpp_info.libdirs` (by default) or the
**folder** directory relative to the package folder. Useful to collect not inter-dependent
libraries or with complex names like `libmylib-x86-debug-en.lib`.

For UNIX libraries staring with **lib**, like *libmath.a*, this tool will collect the library
name **math**.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **folder** – (Optional, Defaulted to `None`): String indicating the subfolder name inside
    `conanfile.package_folder` where the library files are.
* **Returns:**
  A list with the library names

#### WARNING
This tool collects the libraries searching directly inside the package folder and returns them in no specific order. If libraries are
inter-dependent, then `package_info()` method should order them to achieve correct linking order.

Usage:

```python
from conan.tools.files import collect_libs

def package_info(self):
    self.cpp_info.libdirs = ["lib", "other_libdir"]  # Default value is 'lib'
    self.cpp_info.libs = collect_libs(self)
```

For UNIX libraries starting with **lib**, like *libmath.a*, this tool will collect the
library name **math**. Regarding symlinks, this tool will keep only the “most generic”
file among the resolved real file and all symlinks pointing to this real file. For example
among files below, this tool will select *libmath.dylib* file and therefore only append
*math* in the returned list:

```shell
-rwxr-xr-x libmath.1.0.0.dylib lrwxr-xr-x libmath.1.dylib -> libmath.1.0.0.dylib
lrwxr-xr-x libmath.dylib -> libmath.1.dylib
```
