<a id="conan-tools-apple-fix-apple-shared-install-name"></a>

# conan.tools.apple.fix_apple_shared_install_name()

### fix_apple_shared_install_name(conanfile)

Search for all the *dylib* files in the conanfile’s *package_folder* and fix
both the `LC_ID_DYLIB` and `LC_LOAD_DYLIB` fields on those files using the
*install_name_tool* utility available in macOS to set `@rpath`.

This tool will search for all the *dylib* files in the conanfile’s *package_folder* and fix
the library *install names* (the `LC_ID_DYLIB` header). Libraries and executables
inside the package folder will also have the `LC_LOAD_DYLIB` fields updated to reflect
the patched install names. Executables inside the package will also get an `LC_RPATH`
entry pointing to the relative location of the libraries inside the package folder.
This is done using the *install_name_tool* utility available in macOS, as outlined below:

* For `LC_ID_DYLIB` which is the field containing the install name of the library, it
  will change the install name to one that uses the `@rpath`. For example, if the
  install name is `/path/to/lib/libname.dylib`, the new install name will be
  `@rpath/libname.dylib`. This is done by internally executing something like:

```bash
install_name_tool /path/to/lib/libname.dylib -id @rpath/libname.dylib
```

* For `LC_LOAD_DYLIB` which is the field containing the path to the library
  dependencies, it will change the path of the dependencies to one that uses the
  `@rpath`. For example, if a binary has a dependency on `/path/to/lib/dependency.dylib`,
  this will be updated to be `@rpath/dependency.dylib`. This is done for both libraries
  and executables inside the package folder, invoking install_name_tool as below:

```bash
install_name_tool /path/to/lib/libname.dylib -change /path/to/lib/dependency.dylib @rpath/dependency.dylib
```

* For `LC_RPATH`, in those cases in which the packages also contain binary executables
  that depend on libraries within the same package, entries will be added to reflect
  the location of the libraries relative to the executable. If a package has executables
  in the bin subfolder and libraries in the lib subfolder, this can be performed
  with an invocation like this:

```bash
install_name_tool /path/to/bin/my_executable -add_rpath @executable_path/../lib
```

This tool is typically needed by recipes that use Autotools as the build system and in the
case that the correct install names are not fixed in the library being packaged. Use this
tool, if needed, in the conanfile’s `package()` method like:

```python
from conan.tools.apple import fix_apple_shared_install_name

class HelloConan(ConanFile):

  ...

  def package(self):
      autotools = Autotools(self)
      autotools.install()
      fix_apple_shared_install_name(self)
```

<a id="conan-tools-apple-is-apple-os"></a>

# conan.tools.apple.is_apple_os()

### is_apple_os(conanfile, build_context=False)

returns True if OS is Apple one (Macos, iOS, watchOS, tvOS or visionOS)

<a id="conan-tools-apple-to-apple-arch"></a>

# conan.tools.apple.to_apple_arch()

### to_apple_arch(conanfile, default=None)

converts conan-style architecture into Apple-style arch

<a id="conan-tools-apple-xcrun"></a>

# conan.tools.apple.XCRun()

### *class* XCRun(conanfile, sdk=None, use_settings_target=False)

XCRun is a wrapper for the Apple **xcrun** tool used to get information for building.

* **Parameters:**
  * **conanfile** – Conanfile instance.
  * **sdk** – Will skip the flag when `False` is passed and will try to adjust the
    sdk it automatically if `None` is passed.
  * **use_settings_target** – Try to use `settings_target` in case they exist
    (`False` by default)

#### find(tool)

find SDK tools (e.g. clang, ar, ranlib, lipo, codesign, etc.)

#### *property* sdk_path

obtain sdk path (aka apple sysroot or -isysroot

#### *property* sdk_version

obtain sdk version

#### *property* sdk_platform_path

obtain sdk platform path

#### *property* sdk_platform_version

obtain sdk platform version

#### *property* cc

path to C compiler (CC)

#### *property* cxx

path to C++ compiler (CXX)

#### *property* ar

path to archiver (AR)

#### *property* ranlib

path to archive indexer (RANLIB)

#### *property* strip

path to symbol removal utility (STRIP)

#### *property* libtool

path to libtool

#### *property* otool

path to otool

#### *property* install_name_tool

path to install_name_tool
