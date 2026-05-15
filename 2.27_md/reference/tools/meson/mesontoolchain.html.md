<a id="conan-tools-meson-mesontoolchain"></a>

# MesonToolchain

<a id="id1"></a>

#### IMPORTANT
This class will generate files that are only compatible with Meson versions >= 0.55.0

The `MesonToolchain` is the toolchain generator for Meson and it can be used in the `generate()` method
as follows:

```python
from conan import ConanFile
from conan.tools.meson import MesonToolchain

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    requires = "hello/0.1"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    def generate(self):
        tc = MesonToolchain(self)
        tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
        tc.generate()
```

#### IMPORTANT
When your recipe has dependencies `MesonToolchain` only works with the `PkgConfigDeps` generator.
Please, do not use other generators, as they can have overlapping definitions that can conflict.

## Generated files

The `MesonToolchain` generates the following files after a **conan install** (or when building the package
in the cache) with the information provided in the `generate()` method as well as information
translated from the current `settings`, `conf`, etc.:

- *conan_meson_native.ini*: if doing a native build.
- *conan_meson_cross.ini*: if doing a cross-build ([conan.tools.build](https://docs.conan.io/2//reference/tools/build.html.md#conan-tools-build)).

### conan_meson_native.ini

This file contains the definitions of all the Meson properties related to the Conan options
and settings for the current package, platform, etc. This includes but is not limited to the following:

* Detection of `default_library` from Conan settings.
  > * Based on existence/value of an option named `shared`.
* Detection of `buildtype` from Conan settings.
* Definition of the C++ standard as necessary.
* The Visual Studio runtime (`b_vscrt`), obtained from Conan input settings.

### conan_meson_cross.ini

This file contains the same information as the previous *conan_meson_native.ini*,
but with additional information to describe host, target, and build machines (such as the processor architecture).

Check out the meson documentation for more details on native and cross files:

* [Machine files](https://mesonbuild.com/Machine-files.html)
* [Native environments](https://mesonbuild.com/Native-environments.html)
* [Cross compilation](https://mesonbuild.com/Cross-compilation.html)

### Default directories

`MesonToolchain` manages some of the directories used by Meson. These are variables declared under
the `[project options]` section of the files conan_meson_native.ini and conan_meson_cross.ini
(see more information about [Meson directories](https://mesonbuild.com/Builtin-options.html#directories)):

`bindir`: value coming from `self.cpp.package.bindirs`. Defaulted to None.
`sbindir`: value coming from `self.cpp.package.bindirs`. Defaulted to None.
`libexecdir`: value coming from `self.cpp.package.bindirs`. Defaulted to None.
`datadir`: value coming from `self.cpp.package.resdirs`. Defaulted to None.
`localedir`: value coming from `self.cpp.package.resdirs`. Defaulted to None.
`mandir`: value coming from `self.cpp.package.resdirs`. Defaulted to None.
`infodir`: value coming from `self.cpp.package.resdirs`. Defaulted to None.
`includedir`: value coming from `self.cpp.package.includedirs`. Defaulted to None.
`libdir`: value coming from `self.cpp.package.libdirs`. Defaulted to None.

Notice that it needs a `layout` to be able to initialize those `self.cpp.package.xxxxx` variables. For instance:

```python
from conan import ConanFile
from conan.tools.meson import MesonToolchain
class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    def layout(self):
        self.folders.build = "build"
        self.cpp.package.resdirs = ["res"]
    def generate(self):
        tc = MesonToolchain(self)
        self.output.info(tc.project_options["datadir"])  # Will print '["res"]'
        tc.generate()
```

#### NOTE
All of them are saved only if they have any value. If the values are\`\`None\`\`, they won’t be mentioned
in `[project options]` section.

## Customization

### Attributes

#### project_options

This attribute allows defining Meson project options:

```python
def generate(self):
    tc = MesonToolchain(self)
    tc.project_options["MYVAR"] = "MyValue"
    tc.generate()
```

This is translated to:

- One project options definition for `MYVAR` in `conan_meson_native.ini` or `conan_meson_cross.ini` file.

The `wrap_mode: nofallback` is defined by default as a project option, to make sure that dependencies are found in Conan packages. It is possible to change or remove it with:

```python
def generate(self):
    tc = MesonToolchain(self)
    tc.project_options.pop("wrap_mode")
    tc.generate()
```

Note that in this case, Meson might be able to find dependencies in “wraps”, it is the responsibility of the user to check the behavior and make sure about the dependencies origin.

#### subproject_options

This attribute allows defining Meson subproject options:

```python
def generate(self):
    tc = MesonToolchain(self)
    tc.subproject_options["SUBPROJECT"] = [{'MYVAR': 'MyValue'}]
    tc.generate()
```

This is translated to:

- One subproject `SUBPROJECT` and option definition for `MYVAR` in the `conan_meson_native.ini` or `conan_meson_cross.ini` file.

Note that in contrast to `project_options`, `subproject_options` is a dictionary of lists of dictionaries. This is because Meson allows multiple subprojects, and each subproject can have multiple options.

#### preprocessor_definitions

This attribute allows defining compiler preprocessor definitions, for multiple configurations (Debug, Release, etc).

```python
def generate(self):
    tc = MesonToolchain(self)
    tc.preprocessor_definitions["MYDEF"] = "MyValue"
    tc.generate()
```

This is translated to:

- One preprocessor definition for `MYDEF` in `conan_meson_native.ini` or `conan_meson_cross.ini` file.

### conf

`MesonToolchain` is affected by these `[conf]` variables:

- `tools.meson.mesontoolchain:backend`. the meson [backend](https://mesonbuild.com/Configuring-a-build-directory.html) to use. Possible values:
  `ninja`, `vs`, `vs2010`, `vs2015`, `vs2017`, `vs2019`, `xcode`.
- `tools.apple:sdk_path` argument for SDK path in case of Apple cross-compilation. It is used as value
  of the flag `-isysroot`.
- `tools.android:ndk_path` argument for NDK path in case of Android cross-compilation. It is used to get
  some binaries like `c`, `cpp` and `ar` used in `[binaries]` section from *conan_meson_cross.ini*.
- `tools.build:cxxflags` list of extra C++ flags that is used by `cpp_args`.
- `tools.build:cflags` list of extra of pure C flags that is used by `c_args`.
- `tools.build:sharedlinkflags` list of extra linker flags that is used by `c_link_args` and `cpp_link_args`.
- `tools.build:exelinkflags` list of extra linker flags that is used by `c_link_args` and `cpp_link_args`.
- `tools.build:linker_scripts` list of linker scripts, each of which will be prefixed with `-T` and passed
  to `c_link_args` and `cpp_link_args`. Only use this flag with linkers that supports specifying
  linker scripts with the `-T` flag, such as `ld`, `gold`, and `lld`.
- `tools.build:tools.build:add_rpath_link`: add `-Wl,-rpath-link,` linker flag. Set this to `True` to pass this flag pointing
  to all library directories of all host dependencies.
- `tools.build:defines` list of preprocessor definitions, each of which will be prefixed with `-D` and passed to `cpp_args` and `c_args`.
- `tools.build:compiler_executables` dict-like Python object which specifies the compiler as key
  and the compiler executable path as value. Those keys will be mapped as follows:
- `tools.build:sysroot` which accepts a path to the system root directory and sets the `--sysroot` flag that is used by `c_args`, `cpp_args`, `c_link_args` and `cpp_link_args`.
  * `c`: will set `c` in `[binaries]` section from *conan_meson_xxxx.ini*.
  * `cpp`: will set `cpp` in `[binaries]` section from *conan_meson_xxxx.ini*.
  * `objc`: will set `objc` in `[binaries]` section from *conan_meson_xxxx.ini*.
  * `objcpp`: will set `objcpp` in `[binaries]` section from *conan_meson_xxxx.ini*.

## Using Proper Data Types for Conan Options in Meson

Always transform Conan options into valid Python data types before assigning them as Meson
values:

```python
options = {{"shared": [True, False], "fPIC": [True, False], "with_msg": ["ANY"]}}
default_options = {{"shared": False, "fPIC": True, "with_msg": "Hi everyone!"}}

def generate(self):
    tc = MesonToolchain(self)
    tc.project_options["DYNAMIC"] = bool(self.options.shared)  # shared is bool
    tc.project_options["GREETINGS"] = str(self.options.with_msg)  # with_msg is str
    tc.subproject_options["SUBPROJECT"] = [{'MYVAR': str(self.options.with_msg)}]  # with_msg is str
    tc.subproject_options["SUBPROJECT"].append({'MYVAR': bool(self.options.shared)})  # shared is bool
    tc.generate()
```

In contrast, directly assigning a Conan option as a Meson value is strongly discouraged:

```python
options = {{"shared": [True, False], "fPIC": [True, False], "with_msg": ["ANY"]}}
default_options = {{"shared": False, "fPIC": True, "with_msg": "Hi everyone!"}}
# ...
def generate(self):
    tc = MesonToolchain(self)
    tc.project_options["DYNAMIC"] = self.options.shared  # == <PackageOption object>
    tc.project_options["GREETINGS"] = self.options.with_msg  # == <PackageOption object>
    tc.subproject_options["SUBPROJECT"] = [{'MYVAR': self.options.with_msg}]  # == <PackageOption object>
    tc.subproject_options["SUBPROJECT"].append({'MYVAR': self.options.shared})  # == <PackageOption object>
    tc.generate()
```

These are not boolean or string values but an internal Conan class representing such
option values. If you assign these values directly, upon executing the generate()
function, you should receive a warning in your console stating, `WARN: deprecated:
Please, do not use a Conan option value directly.` This method is considered bad practice
as it can result in unexpected errors during your project’s build process.

## Cross-building for Apple and Android

The `MesonToolchain` generator adds all the flags required to cross-compile for Apple (MacOS M1, iOS, etc.) and Android.

**Apple**

It adds link flags `-arch XXX`, `-isysroot [SDK_PATH]` and the minimum deployment target flag, e.g., `-mios-version-min=8.0`
to the `MesonToolchain` `c_args`, `c_link_args`, `cpp_args`, and `cpp_link_args` attributes, given the
Conan settings for any Apple OS (iOS, watchOS, etc.) and the `tools.apple:sdk_path` configuration value like it’s shown
in this example of host profile:

```text
[settings]
os = iOS
os.version = 10.0
os.sdk = iphoneos
arch = armv8
compiler = apple-clang
compiler.version = 12.0
compiler.libcxx = libc++

[conf]
tools.apple:sdk_path=/my/path/to/iPhoneOS.sdk
```

**Android**

It initializes the `MesonToolchain` `c`, `cpp`, and `ar` attributes, which are needed to cross-compile for Android, given the
Conan settings for Android and the `tools.android:ndk_path` configuration value like it’s shown
in this example of host profile:

```text
[settings]
os = Android
os.api_level = 21
arch = armv8

[conf]
tools.android:ndk_path=/my/path/to/NDK
```

## Cross-building and native=true

New since [Conan 2.3.0](https://github.com/conan-io/conan/releases/tag/2.3.0)

When you are cross-building, sometimes you need to build a tool which is used to generate source files.
For this you would want to build some targets with the system’s native compiler. Then, you need Conan to create both
context files:

```python
def generate(self):
    tc = MesonToolchain(self)
    tc.generate()
    # Forcing to create the native context too
    if cross_building(self):
        tc = MesonToolchain(self, native=True)
        tc.generate()
```

See also [this reference](https://mesonbuild.com/Cross-compilation.html#mixing-host-and-build-targets)
from the Meson documentation for more information.

### Objective-C arguments

In Apple OS’s there are also specific Objective-C/Objective-C++ arguments: `objc`,
`objcpp`, `objc_args`, `objc_link_args`, `objcpp_args`, and `objcpp_link_args`,
as public attributes of the `MesonToolchain` class, where the variables `objc` and
`objcpp` are initialized as `clang` and `clang++` respectively by default.

#### SEE ALSO
- [Getting started with Meson](https://docs.conan.io/2//examples/tools/meson/build_simple_meson_project.html.md#examples-tools-meson-toolchain-build-simple-meson-project)

<a id="mesontoolchain-reference"></a>

## Reference

### *class* MesonToolchain(conanfile, backend=None, native=False)

MesonToolchain generator

* **Parameters:**
  * **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.
  * **backend** – (**DEPRECATED**, use `self.backend` instead) `str` `backend` Meson variable
    value. By default, `ninja`.
  * **native** – `bool` Indicates whether you want Conan to create the
    `conan_meson_native.ini` in a cross-building context. Notice that it only
    makes sense if your project’s `meson.build` uses the `native=true`
    (see also [https://mesonbuild.com/Cross-compilation.html#mixing-host-and-build-targets](https://mesonbuild.com/Cross-compilation.html#mixing-host-and-build-targets)).

#### backend

Backend to use. Defined by the conf `tools.meson.mesontoolchain:backend`. By default, `ninja`.

#### buildtype

Build type to use.

#### b_ndebug

Disable asserts.

#### b_staticpic

Build static libraries as position independent. By default, `self.options.get_safe("fPIC")`

#### default_library

Default library type, e.g., “shared.

#### cpp_std

C++ language standard to use. Defined by `to_cppstd_flag()` by default.

#### c_std

C language standard to use. Defined by `to_cstd_flag()` by default.

#### b_vscrt

VS runtime library to use. Defined by `msvc_runtime_flag()` by default.

#### extra_cxxflags

List of extra `CXX` flags. Added to `cpp_args`

#### extra_cflags

List of extra `C` flags. Added to `c_args`

#### extra_ldflags

List of extra linker flags. Added to `c_link_args` and `cpp_link_args`

#### extra_defines

List of extra preprocessor definitions. Added to `c_args` and `cpp_args` with the
format `-D[FLAG_N]`.

#### arch_flag

Architecture flag deduced by Conan and added to `c_args`, `cpp_args`, `c_link_args` and `cpp_link_args`

#### arch_link_flag

Architecture link flag deduced by Conan and added to `c_link_args` and `cpp_link_args`

#### threads_flags

Threads flags deduced by Conan and added to `c_args`, `cpp_args`, `c_link_args` and `cpp_link_args`

#### properties

Dict-like object that defines Meson `properties` with `key=value` format

#### project_options

Dict-like object that defines Meson `project options` with `key=value` format

#### preprocessor_definitions

Dict-like object that defines Meson `preprocessor definitions`

#### subproject_options

Dict-like object that defines Meson `subproject options`.

#### pkg_config_path

Defines the Meson `pkg_config_path` variable

#### cross_build

Dict-like object with the build, host, and target as the Meson machine context

#### c

Sets the Meson `c` variable, defaulting to the `CC` build environment value.
If provided as a blank-separated string, it will be transformed into a list.
Otherwise, it remains a single string.

#### cpp

Sets the Meson `cpp` variable, defaulting to the `CXX` build environment value.
If provided as a blank-separated string, it will be transformed into a list.
Otherwise, it remains a single string.

#### ld

Sets the Meson `ld` variable, defaulting to the `LD` build environment value.
If provided as a blank-separated string, it will be transformed into a list.
Otherwise, it remains a single string.

#### c_ld

Defines the Meson `c_ld` variable. Defaulted to `CC_LD`
environment value

#### cpp_ld

Defines the Meson `cpp_ld` variable. Defaulted to `CXX_LD`
environment value

#### ar

Defines the Meson `ar` variable. Defaulted to `AR` build environment value

#### strip

Defines the Meson `strip` variable. Defaulted to `STRIP` build environment value

#### as_

Defines the Meson `as` variable. Defaulted to `AS` build environment value

#### windres

Defines the Meson `windres` variable. Defaulted to `WINDRES` build environment value

#### pkgconfig

Defines the Meson `pkgconfig` variable. Defaulted to `PKG_CONFIG`
build environment value

#### c_args

Defines the Meson `c_args` variable. Defaulted to `CFLAGS` build environment value

#### c_link_args

Defines the Meson `c_link_args` variable. Defaulted to `LDFLAGS` build
environment value

#### cpp_args

Defines the Meson `cpp_args` variable. Defaulted to `CXXFLAGS` build environment value

#### cpp_link_args

Defines the Meson `cpp_link_args` variable. Defaulted to `LDFLAGS` build
environment value

#### apple_arch_flag

Apple arch flag as a list, e.g., `["-arch", "i386"]`

#### apple_isysroot_flag

Apple sysroot flag as a list, e.g., `["-isysroot", "./Platforms/MacOSX.platform"]`

#### apple_min_version_flag

Apple minimum binary version flag as a list, e.g., `["-mios-version-min", "10.8"]`

#### apple_extra_flags

Apple bitcode, visibility and arc flags

#### objc

Defines the Meson `objc` variable. Defaulted to `None`, if if any Apple OS `clang`

#### objcpp

Defines the Meson `objcpp` variable. Defaulted to `None`, if if any Apple OS `clang++`

#### objc_args

Defines the Meson `objc_args` variable. Defaulted to `OBJCFLAGS` build environment value

#### objc_link_args

Defines the Meson `objc_link_args` variable. Defaulted to `LDFLAGS` build environment value

#### objcpp_args

Defines the Meson `objcpp_args` variable. Defaulted to `OBJCXXFLAGS` build environment value

#### objcpp_link_args

Defines the Meson `objcpp_link_args` variable. Defaulted to `LDFLAGS` build environment value

#### generate()

Creates a `conan_meson_native.ini` (if native builds) or a
`conan_meson_cross.ini` (if cross builds) with the proper content.
If Windows OS, it will be created a `conanvcvars.bat` as well.
