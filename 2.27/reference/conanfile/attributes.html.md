<a id="conan-conanfile-attributes"></a>

# Attributes

> * [Package reference](#package-reference)
>   * [name](#name)
>   * [version](#version)
>   * [user](#user)
>   * [channel](#channel)
> * [Metadata](#metadata)
>   * [description](#description)
>   * [license](#license)
>   * [author](#author)
>   * [topics](#topics)
>   * [homepage](#homepage)
>   * [url](#url)
> * [Requirements](#requirements)
>   * [requires](#requires)
>   * [tool_requires](#tool-requires)
>   * [build_requires](#build-requires)
>   * [test_requires](#test-requires)
>   * [python_requires](#python-requires)
>   * [python_requires_extend](#python-requires-extend)
> * [Sources](#sources)
>   * [exports](#exports)
>   * [exports_sources](#exports-sources)
>   * [conan_data](#conan-data)
>   * [source_buildenv](#source-buildenv)
> * [Binary model](#binary-model)
>   * [package_type](#package-type)
>   * [settings](#settings)
>   * [options](#options)
>   * [default_options](#default-options)
>   * [default_build_options](#default-build-options)
>   * [options_description](#options-description)
>   * [languages](#languages)
>   * [info](#info)
>   * [package_id_{embed,non_embed,python,unknown}_mode, build_mode](#package-id-embed-non-embed-python-unknown-mode-build-mode)
>   * [package_id_abi_options](#package-id-abi-options)
>   * [context](#context)
> * [Build](#build)
>   * [generators](#generators)
>   * [build_policy](#build-policy)
>   * [win_bash](#win-bash)
>   * [win_bash_run](#win-bash-run)
> * [Folders and layout](#folders-and-layout)
>   * [source_folder](#source-folder)
>   * [export_sources_folder](#export-sources-folder)
>   * [build_folder](#build-folder)
>   * [generators_folder](#generators-folder)
>   * [package_folder](#package-folder)
>   * [recipe_folder](#recipe-folder)
>   * [recipe_metadata_folder](#recipe-metadata-folder)
>   * [package_metadata_folder](#package-metadata-folder)
>   * [no_copy_source](#no-copy-source)
>   * [test_package_folder](#test-package-folder)
> * [Layout](#layout)
>   * [folders](#folders)
>   * [cpp](#cpp)
>   * [layouts](#layouts)
> * [Package information for consumers](#package-information-for-consumers)
>   * [cpp_info](#cpp-info)
>   * [buildenv_info](#buildenv-info)
>   * [runenv_info](#runenv-info)
>   * [conf_info](#conf-info)
>   * [generator_info](#generator-info)
>   * [deprecated](#deprecated)
>   * [provides](#provides)
> * [Other](#other)
>   * [dependencies](#dependencies)
>   * [subgraph](#subgraph)
>   * [conf](#conf)
>   * [Output](#output)
>   * [Output contents](#output-contents)
>   * [revision_mode](#revision-mode)
>   * [upload_policy](#upload-policy)
>   * [required_conan_version](#required-conan-version)
>   * [implements](#implements)
>   * [alias](#alias)
>   * [extension_properties](#extension-properties)

## Package reference

Recipe attributes that can define the main `pkg/version@user/channel` package reference.

### name

The name of the package. A valid name is all lowercase and has:

- A minimum of 2 and a maximum of 101 characters (though shorter names are recommended).
- Matches the following regex `^[a-z0-9_][a-z0-9_+.-]{1,100}$`: so starts with alphanumeric or `_`,
  : then from 1 to 100 characters between alphanumeric, `_`, `+`, `.` or `-`.

The name is only necessary for `export`-ing the recipe into the local cache (`export`, `export-pkg`
: and `create` commands), if they are not defined in the command line with `--name=<pkgname>`.

### version

The version of the package. A valid version follows the same rules than the `name` attribute.
In case the version follows semantic versioning in the form `X.Y.Z-pre1+build2`, that value might be used for requiring
this package through version ranges instead of exact versions.

The version is only strictly necessary for `export`-ing the recipe into the local cache (`export`, `export-pkg`
and `create` commands), if they are not defined in the command line with `--version=<pkgversion>`

The `version` can be dynamically defined in the command line, and also programmatically in the recipe with the
[set_version() method](https://docs.conan.io/2//reference/conanfile/methods/set_version.html.md#reference-conanfile-methods-set-version).

### user

A valid string for the `user` field follows the same rules than the `name` attribute.
This is an optional attribute. It can be used to identify your own packages with `pkg/version@user/channel`,
where `user` could be the name of your team, org or company. ConanCenter recipes don’t have `user/channel`,
so they are in the form of `pkg/version` only. You can also name your packages without user and channel, or using
only the user as `pkg/version@user`.

The user can be specified in the command line with `--user=<myuser>`

### channel

A valid string for the `channel` field follows the same rules than the `name` attribute.
This is an optional attribute. It is sometimes used to identify a maturity of the package (“stable”, “testing”…),
but in general this is not necessary, and the maturity of packages is better managed by putting them in different
server repositories.

The channel can be specified in the command line with `--channel=<mychannel>`. If a channel is specified,
a user must also be specified, so the package reference is always complete as `pkg/version@user/channel`.

## Metadata

Optional metadata, like license, description, author, etc. Not necessary for most cases, but can be useful to have.

### description

This is an optional, but recommended text field, containing the description of the package,
and any information that might be useful for the consumers. The first line might be used as a
short description of the package.

```python
class HelloConan(ConanFile):
    name = "hello"
    version = "0.1"
    description = """This is a Hello World library.
                    A fully featured, portable, C++ library to say Hello World in the stdout,
                    with incredible iostreams performance"""
```

### license

License of the **target** source code and binaries, i.e. the code
that is being packaged, not the `conanfile.py` itself.
Can contain several, comma separated licenses. It is a text string, so it can
contain any text, but it is strongly recommended that recipes of Open Source projects use
[SPDX](https://spdx.dev) identifiers from the [SPDX license list](https://spdx.org/licenses/)

This will help people wanting to automate license compatibility checks, like consumers of your
package, or you if your package has Open-Source dependencies.

```python
class Pkg(ConanFile):
    license = "MIT"
```

### author

Main maintainer/responsible for the package, any format. This is an optional attribute.

```python
class HelloConan(ConanFile):
    author = "John J. Smith (john.smith@company.com)"
```

### topics

Tags to group related packages together and describe what the code is about.
Used as a search filter in ConanCenter. Optional attribute. It should be a tuple of strings.

```python
class ProtocInstallerConan(ConanFile):
    name = "protoc_installer"
    version = "0.1"
    topics = ("protocol-buffers", "protocol-compiler", "serialization", "rpc")
```

### homepage

The home web page of the library being packaged.

Used to link the recipe to further explanations of the library itself like an overview of its features, documentation, FAQ
as well as other related information.

```python
class EigenConan(ConanFile):
    name = "eigen"
    version = "3.3.4"
    homepage = "http://eigen.tuxfamily.org"
```

### url

URL of the package repository, i.e. not necessarily of the original source code.
Recommended, but not mandatory attribute.

```python
class HelloConan(ConanFile):
    name = "hello"
    version = "0.1"
    url = "https://github.com/conan-io/libhello.git"
```

## Requirements

Attribute form of the dependencies simple declarations, like `requires`, `tool_requires`.
For more advanced way to define requirements, use the `requirements()`, `build_requirements()` methods instead.

### requires

List or tuple of strings for regular dependencies in the host context, like a library.

```python
class MyLibConan(ConanFile):
    requires = "hello/1.0", "otherlib/2.1@otheruser/testing"
```

You can specify version ranges, the syntax is using brackets:

<a id="version-ranges-reference"></a>
```python
class HelloConan(ConanFile):
    requires = "pkg/[>1.0 <1.8]"
```

Accepted expressions would be:

| Expression   | Versions in range        | Versions outside of range   |
|--------------|--------------------------|-----------------------------|
| [>=1.0 <2]   | 1.0.0, 1.0.1, 1.1, 1.2.3 | 0.2, 2.0, 2.1, 3.0          |
| [<3.2.1]     | 0.1, 1.2, 2.4, 3.1.1     | 3.2.2                       |
| [>2.0]       | 2.1, 2.2, 3.1, 14.2      | 1.1, 1.2, 2.0               |

The caret `^` and tilde `~` operators are basically compact representations of lower and upper bounds:

- The `[~2.5.1]` range could be written as `[>=2.5.1 <2.6.0]`
- The `[^1.2.3]` range could be written as `[>=1.2.3 <2.0.0]`

In general, it is recommended to use the full expression `[>=lower <upper]` instead of the caret or tilde shortcuts,
as it is more explicit and evident for all readers what the valid versions are in that range.

If pre-releases are activated, like defining configuration `core.version_ranges:resolve_prereleases=True`:

| Expression   | Versions in range                             | Versions outside of range      |
|--------------|-----------------------------------------------|--------------------------------|
| [>=1.0 <2]   | 1.0.0-pre.1, 1.0.0, 1.0.1, 1.1, 1.2.3         | 0.2, 2.0-pre.1, 2.0, 2.1, 3.0  |
| [<3.2.1]     | 0.1, 1.2, 1.8-beta.1, 2.0-alpha.2, 2.4, 3.1.1 | 3.2.1-pre.1, 3.2.1, 3.2.2, 3.3 |
| [>2.0]       | 2.1-pre.1, 2.1, 2.2, 3.1, 14.2                | 1.1, 1.2, 2.0-pre.1, 2.0       |

#### SEE ALSO
- Check [Range expressions](https://docs.conan.io/2//tutorial/versioning/version_ranges.html.md#tutorial-version-ranges-expressions) version_ranges tutorial section
- Check [requirements()](https://docs.conan.io/2//reference/conanfile/methods/requirements.html.md#reference-conanfile-methods-requirements) method docs

### tool_requires

List or tuple of strings for dependencies. Represents a build tool like “cmake”. If there is
an existing pre-compiled binary for the current package, the binaries for the tool_require
won’t be retrieved. They cannot conflict.

```python
class MyPkg(ConanFile):
    tool_requires = "tool_a/0.2", "tool_b/0.2@user/testing"
```

This is the declarative way to add `tool_requires`. Check the [tool_requires()](https://docs.conan.io/2//reference/conanfile/methods/build_requirements.html.md#reference-conanfile-methods-build-requirements-tool-requires)
conanfile.py method to learn a more flexible way to add them.

<a id="reference-conanfile-attributes-build-requires"></a>

### build_requires

build_requires are used in Conan 2 to provide compatibility with the Conan 1.X syntax,
but their use is discouraged in Conan 2 and will be deprecated in future 2.X releases.
Please use tool_requires instead of build_requires in your Conan 2 recipes.

### test_requires

List or tuple of strings for dependencies in the host context only. Represents a test tool
like “gtest”. Used when the current package is built from sources.
They don’t propagate information to the downstream consumers. If there is
an existing pre-compiled binary for the current package, the binaries for the test_require
won’t be retrieved. They cannot conflict.

```python
class MyPkg(ConanFile):
    test_requires = "gtest/1.17.0", "other_test_tool/0.2@user/testing"
```

This is the declarative way to add `test_requires`.
Check the [test_requires() method](https://docs.conan.io/2//reference/conanfile/methods/build_requirements.html.md#reference-conanfile-methods-build-requirements-test-requires)
to learn a more flexible way to add them.

### python_requires

This class attribute allows to define a dependency to another Conan recipe and reuse its code.
Its basic syntax is:

```python
from conan import ConanFile

class Pkg(ConanFile):
    python_requires = "pyreq/0.1@user/channel"  # recipe to reuse code from

    def build(self):
        self.python_requires["pyreq"].module # access to the whole conanfile.py module
        self.python_requires["pyreq"].module.myvar  # access to a variable
        self.python_requires["pyreq"].module.myfunct()  # access to a global function
        self.python_requires["pyreq"].path # access to the folder where the reused file is
```

Read more about this attribute in [Python requires](https://docs.conan.io/2//reference/extensions/python_requires.html.md#reference-extensions-python-requires)

### python_requires_extend

This class attribute defines one or more classes that will be injected in runtime as base classes of
the recipe class. Syntax for each of these classes should be a string like `pyreq.MyConanfileBase`
where the `pyreq` is the name of a `python_requires` and `MyConanfileBase` is the name of the class
to use.

```python
from conan import ConanFile

class Pkg(ConanFile):
    python_requires = "pyreq/0.1@user/channel", "utils/0.1@user/channel"
    python_requires_extend = "pyreq.MyConanfileBase", "utils.UtilsBase"  # class/es to inject
```

## Sources

<a id="exports-attribute"></a>

### exports

List or tuple of strings with file names or
[fnmatch](https://docs.python.org/3/library/fnmatch.html) patterns that should be exported
and stored side by side with the *conanfile.py* file to make the recipe work:
other python files that the recipe will import, some text file with data to read,…

For example, if we have some python code that we want the recipe to use in a `helpers.py` file,
and have some text file *info.txt* we want to read and display during the recipe evaluation
we would do something like:

```python
exports = "helpers.py", "info.txt"
```

Exclude patterns are also possible, with the `!` prefix:

```python
exports = "*.py", "!*tmp.py"
```

#### SEE ALSO
- [Check the export() conanfile.py method](https://docs.conan.io/2//reference/conanfile/methods/export.html.md#reference-conanfile-methods-export).

<a id="exports-sources-attribute"></a>

### exports_sources

List or tuple of strings with file names or
[fnmatch](https://docs.python.org/3/library/fnmatch.html) patterns that should be exported
and will be available to generate the package. Unlike the `exports` attribute, these files
shouldn’t be used by the `conanfile.py` Python code, but to compile the library or generate
the final package. And, due to its purpose, these files will only be retrieved if requested
binaries are not available or the user forces Conan to compile from sources.

This is an alternative to getting the sources with the `source()` method. Used when we are not packaging a third party
library and we have together the recipe and the C/C++ project:

```python
exports_sources = "include*", "src*"
```

Exclude patterns are also possible, with the `!` prefix:

```python
exports_sources = "include*", "src*", "!src/build/*"
```

Note, if the recipe defines the `layout()` method and specifies a `self.folders.source = "src"` it won’t affect
where the files (from the `exports_sources`) are copied. They will be copied to the base source folder. So, if you
want to replace some file that got into the `source()` method, you need to explicitly copy it from the parent folder
or even better, from `self.export_sources_folder`.

```python
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
        shutil.copy(os.path.join(self.export_sources_folder, "CMakeLists.txt"), ".")
```

#### SEE ALSO
- [Check the export_sources() conanfile.py method](https://docs.conan.io/2//reference/conanfile/methods/export_sources.html.md#reference-conanfile-methods-export-sources).

<a id="conan-conanfile-properties-conandata"></a>

### conan_data

Read only attribute with a dictionary with the keys and values provided in a
[conandata.yml](https://docs.conan.io/2//tutorial/creating_packages/handle_sources_in_packages.html.md#creating-packages-handle-sources-in-packages-conandata) file format placed
next to the *conanfile.py*. This YAML file is automatically exported with the recipe and automatically loaded with it too.

You can declare information in the *conandata.yml* file and then access it inside any of the methods of the recipe.
For example, a *conandata.yml* with information about sources that looks like this:

```YAML
sources:
  "1.1.0":
    url: "https://www.url.org/source/mylib-1.0.0.tar.gz"
    sha256: "8c48baf3babe0d505d16cfc0cf272589c66d3624264098213db0fb00034728e9"
  "1.1.1":
    url: "https://www.url.org/source/mylib-1.0.1.tar.gz"
    sha256: "15b6393c20030aab02c8e2fe0243cb1d1d18062f6c095d67bca91871dc7f324a"
```

```python
def source(self):
    get(self, **self.conan_data["sources"][self.version])
```

### source_buildenv

Boolean attribute to opt-in injecting the [VirtualBuildEnv](https://docs.conan.io/2//reference/tools/env/virtualbuildenv.html.md#conan-tools-env-virtualbuildenv) generated environment while running the source() method.

Setting this attribute to True (default value False) will inject the `VirtualBuildEnv` generated environment from tool requires
when executing the source() method.

```python
 class MyConan:
    name = "mylib"
    version = "1.0.0"
    source_buildenv = True
    tool_requires = "7zip/1.2.0"

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        self.run("7z x *.zip -o*")  ## Can run 7z in the source method
```

## Binary model

Important attributes that define the package binaries model, which settings, options, package type, etc.
affect the final packaged binaries.

<a id="reference-conanfile-attributes-package-type"></a>

### package_type

Optional, but very strongly recommended.
Declaring the `package_type` will help Conan:

- To choose better the default `package_id_mode` for each dependency, that is, how a change
  in a dependency should affect the `package_id` to the current package.
- Which information from the dependencies should be propagated to the consumers, like
  headers, libraries, runtime information. See [here](https://docs.conan.io/2//reference/conanfile/methods/requirements.html.md#reference-conanfile-package-type-trait-inferring)
  to see what traits are propagated based on the `package_type` information.

The valid values are:

- **application**: The package is an application.
- **library**: The package is a generic library. It will try to determine
  the type of library (from `shared-library`, `static-library`, `header-library`)
  reading the `self.options.shared` (if declared) and the `self.options.header_only`
- **shared-library**: The package is a shared library.
- **static-library**: The package is a static library.
- **header-library**: The package is a header only library.
- **build-scripts**: The package only contains build scripts.
- **python-require**: The package is a python require.
- **unknown**: The type of the package is unknown.

Note that relationships between packages might not always be defined and can lead to errors, for example,
`build-scripts` cannot have regular `requires` dependencies to compiled libraries, and it is not
known how these should be propagated through something that is intended to be used as a `tool_requires`.
If some package want to use both some build scripts and link with a given library should define a
`tool_requires()` to the `build-scripts` package and a regular `requires()` to the compiled library.

#### IMPORTANT
The `package_type` defines how different information of C and C++ packages is propagated
down the dependency graph: visibility of headers, linkage requirements, etc. It is very
recommended to define it, and it should be defined in most cases.

<a id="conan-conanfile-properties-settings"></a>

### settings

List of strings with the first level settings (from [settings.yml](https://docs.conan.io/2//reference/config_files/settings.html.md#reference-config-files-settings-yml)) that the recipe
needs, because:
- They are read for building (e.g: if self.settings.compiler == “gcc”)
- They affect the `package_id`. If a value of the declared setting changes, the `package_id` has to be different.

The most common is to declare:

```python
settings = "os", "compiler", "build_type", "arch"
```

Once the recipe is loaded by Conan, the `settings` are processed and they can be read in the recipe, also
the sub-settings:

```python
settings = "os", "arch"

def build(self):
    if self.settings.compiler == "gcc":
        if self.settings.compiler.cppstd == "gnu20":
            # do some special build commands
```

If you try to access some setting that doesn’t exist, like `self.settings.compiler.libcxx`
for the `msvc` setting, Conan will fail telling that `libcxx` does not exist for that compiler.

If you want to do a safe check of settings values, you could use the `get_safe()` method:

```python
def build(self):
    # Will be None if doesn't exist (not declared)
    arch = self.settings.get_safe("arch")
    # Will be None if doesn't exist (doesn't exist for the current compiler)
    compiler_version = self.settings.get_safe("compiler.version")
    # Will be the default version if the return is None
    build_type = self.settings.get_safe("build_type", default="Release")
```

The `get_safe()` method returns `None` if that setting or sub-setting doesn’t
exist and there is no default value assigned.

It’s also feasible to check the possible values defined in [settings.yml](https://docs.conan.io/2//reference/config_files/settings.html.md#reference-config-files-settings-yml) using the
`possible_values()` method:

```python
def generate(self):
    # Print if Android exists as OS in the whole settings.yml
    is_android = "Android" in self.settings.possible_values()["os"]
    self.output.info(f"Android in settings.yml: {is_android}")
    # Print the available versions for the compiler used by the HOST profile
    compiler_versions = self.settings.compiler.version.possible_values()
    self.output.info(f"[HOST] Versions for {str(self.settings.compiler)}:  {', '.join(compiler_versions)}")
    # Print the available versions for the compiler used by the BUILD profile
    compiler_versions = self.settings_build.compiler.version.possible_values()
    self.output.info(f"[BUILD] Versions for {str(self.settings_build.compiler)}:  {', '.join(compiler_versions)}")
```

As you can see above, doing `self.settings.possible_values()` returns the
whole [settings.yml](https://docs.conan.io/2//reference/config_files/settings.html.md#reference-config-files-settings-yml) as a Python dict-like object, and doing
`self.settings.compiler.version.possible_values()` for instance returns the available versions for the compiler
used by the consumer.

If you want to do a safe deletion of settings, you could use the `rm_safe()` method.
For example, in the `configure()` method a typical pattern for a C library would be:

```python
def configure(self):
    self.settings.rm_safe("compiler.libcxx")
    self.settings.rm_safe("compiler.cppstd")
```

#### SEE ALSO
- [settings.yml](https://docs.conan.io/2//reference/config_files/settings.html.md#reference-config-files-settings-yml).
- [Removing settings in the package_id() method](https://docs.conan.io/2//reference/conanfile/methods/package_id.html.md#reference-conanfile-methods-package-id-clear).
- [Creating universal binaries using CMakeToolchain](https://docs.conan.io/2//reference/tools/cmake/cmaketoolchain.html.md#conan-tools-cmaketoolchain-universal-binaries).

<a id="conan-conanfile-properties-options"></a>

### options

Dictionary with traits that affects only the current recipe, where the key is the option
name and the value is a list of different values that the option can take. By default any
value change in an option, changes the `package_id`. Check the `default_options` and
`default_build_options` fields to define default values for the options.

Values for each option can be typed or plain strings (`"value"`, `True`, `42`,…).

There are two special values:

- `None`: Allow the option to have a `None` value (not specified) without erroring.
- `"ANY"`:  For options that can take any value, not restricted to a set.

```python
class MyPkg(ConanFile):
    ...
    options = {
        "shared": [True, False],
        "option1": ["value1", "value2"],
        "option2": ["ANY"],
        "option3": [None, "value1", "value2"],
        "option4": [True, False, "value"],
}
```

Once the recipe is loaded by Conan, the `options` are processed and they can be read in the recipe. You can also
use the method `.get_safe()` (see [settings attribute](#conan-conanfile-properties-settings)) to avoid Conan raising an Exception if the option
doesn’t exist:

```python
class MyPkg(ConanFile):
    options = {"shared": [True, False]}

    def build(self):
        if self.options.shared:
            # build the shared library
        if self.options.get_safe("foo", True):
            pass
```

In boolean expressions, like `if self.options.shared`:

- equals `True` for the values `True`, `"True"` and `"true"`, and any other value that
  would be evaluated the same way in Python code.
- equals `False` for the values `False`, `"False"` and `"false"`, also for the empty
  string and for `0` and `"0"` as expected.

Notice that a comparison using `is` is always `False` because the types would be different as it is encapsulated
inside a Python class.

If you want to do a safe deletion of options, you could use the `rm_safe()` method.
For example, in the `config_options()` method a typical pattern for Windows library
would be:

```python
def config_options(self):
    if self.settings.os == "Windows":
        self.options.rm_safe("fPIC")
```

#### SEE ALSO
- Read the [Getting started, creating packages](https://docs.conan.io/2//tutorial/creating_packages/create_your_first_package.html.md#creating-packages-create-your-first-conan-package) to know how to declare and how to
  define a value to an option.
- [Removing options in the package_id() method](https://docs.conan.io/2//reference/conanfile/methods/package_id.html.md#reference-conanfile-methods-package-id-clear).
- Read [how the package_type attribute behaves when a shared option is declared](#reference-conanfile-attributes-package-type).

<a id="conan-conanfile-properties-default-options"></a>

### default_options

The attribute `default_options` defines the default values for the options, both for the
current recipe and for any requirement.
This attribute should be defined as a python dictionary.

```python
class MyPkg(ConanFile):
    ...
    requires = "zlib/1.2.8", "zwave/2.0"
    options = {"build_tests": [True, False],
                "option2": "ANY"}
    default_options = {"build_tests": True,
                        "option1": 42,
                        "z*:shared": True}
```

You can also assign default values for options of your requirements using “<reference_pattern>: option_name”, being
a valid `reference_pattern` a `name/version` or any pattern with `*` like the example above.

#### WARNING
Defining options values in recipes does not have strong guarantees, please check
[this FAQ about options values for dependencies](https://docs.conan.io/2//knowledge/faq.html.md#faq-different-options-values). The recommended way
to define options values is in profile files.

You can also set the options conditionally to a final value with `configure()` instead of using `default_options`:

```python
class OtherPkg(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    options = {"some_option": [True, False]}
    # Do NOT declare 'default_options', use 'config_options()'

    def configure(self):
        if self.options.some_option == None:
            if self.settings.os == 'Android':
                self.options.some_option = True
            else:
                self.options.some_option = False
```

Take into account that if a value is assigned in the `configure()` method it cannot be overridden.

#### SEE ALSO
- [config_options() method](https://docs.conan.io/2//reference/conanfile/methods/config_options.html.md#reference-conanfile-methods-config-options).

There are 2 different ways that a recipe can try to define options values for its dependencies.
Using `default_options = {"mypkg/*:myoption", 123}` the current recipe can define the `123` value
to the dependency `mypkg` `myoption`. This way of defining options for dependencies has
some limitations:

- Any other downstream user of the current recipe that defines the same option for `mypkg`
  will have precedence, overwriting the current recipe `123` value. Also any definition
  in the profile or command line will also have precedence. The recipe `default_options`
  have the least precedence.
  If a recipe will not work at all with some dependencies options, then recipes can check
  and raise `ConanInvalidConfiguration` errors accordingly.
- Any *sibling* package that depends on `mypkg` will also define its options and it will
  be the only one being taken into account. In other words, the first time `mypkg` is required
  by any other package will “freeze” its currently assigned options values. Any other package
  that depends later on `mypkg`, closing the diamond structures in the dependency graph will
  not have any influence on the `mypkg` options. Only the first one requiring it will.

The second way to define the options values is defining them as `important!`.

#### WARNING
The `important!` syntax is experimental and can be changed or removed at any time.

A recipe can define its dependencies options as `important!` with the syntax
`default_options = {"mypkg/*:myoption!", 123}`. That means that the `mypkg` `myoption`
will not be overriden by other downstream packages, profile or command line doing regular
definition of options (like `-o *:myoption=234`).

But there are 2 cases in which this will still not define the final value of the dependency:

- If any downstream recipe, command line or profile also uses the `myoption!` syntax, that
  will also have precedence and override the value upstream
- If there is any other package that requires first `mypkg`, the values defined at that moment
  will still have precedence.

In general the recommendation for defining options values is to do it in `profile` files,
not in recipes, as in-recipe definition can be more complicated specially for complex
dependency graphs.

### default_build_options

The attribute `default_build_options` defines the default values for the options in the
build context and is typically used for defining options for `tool_requires`.

```python
from conan import ConanFile
class Consumer(ConanFile):
    default_options = {"protobuf/*:shared": True}
    default_build_options = {"protobuf/*:shared": False}
    def requirements(self):
        self.requires("protobuf/1.0")
    def build_requirements(self):
        self.tool_requires("protobuf/1.0")
```

### options_description

The `options_description` attribute is an optional attribute that can be defined in the
form of a dictionary where the key is the option name and the value is a description of
the option in text format. This attribute is useful for providing additional information
about the functionality and purpose of each option, particularly when the option is not
self-explanatory or has complex or special behavior.

The format for each dictionary entry should be:

- Key: Option name. Must be a string and must match one of the keys in the `options` dictionary.
- Value: Description of the option. Must be a string and can be as long as necessary.

For example:

```python
class MyPkg(ConanFile):
    ...
    options = {"option1": [True, False],
               "option2": "ANY"}

    options_description = {
        "option1": "Describe the purpose and functionality of 'option1'. ",
        "option2": "Describe the purpose and functionality of 'option2'. ",
    }
```

### languages

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

From Conan 2.4, the `conanfile.py` recipe attribute `languages` can be used to define the programming languages
involved in this package. At the moment the `C` and `C++` languages are the possible values. For example a
pure C package would define something as:

```python
class ZLib(ConanFile):
    languages = "C"
```

It is possible to define more than one language, for example `languages = "C", "C++"` is the correct definition when
a package is built from both C and C++ sources.

Regarding `languages` definition, the following will happen:

- If no `languages` is defined or `C` is not a declared language, `compiler.cstd` subsetting will be automatically removed
  at package `configure()` time (to achieve backward compatibility).
- If `languages` is defined, but it doesn’t contain `C++`, `compiler.cppstd` and `compiler.libcxx` subsettings will be
  automatically removed at package `configure()` time.

### info

Object used exclusively in `package_id()` method:

- The :ref:package_id method<reference_conanfile_methods_package_id> to control the unique ID for a package:
  > ```python
  > def package_id(self):
  >     self.info.clear()
  > ```

The `self.info.clear()` method removes all the settings, options, requirements (`requires`, `tool_requires`, `python_requires`)
and configuration (`conf`) from the `package_id` computation, so the `package_id` will always result in the same binary, irrespective
of all those things. This would be the typical case of a header-only library, in which the packaged artifacts (files) are always identical.

<a id="reference-conanfile-attributes-package-id-modes"></a>

### package_id_{embed,non_embed,python,unknown}_mode, build_mode

The `package_id_embed_mode, package_id_non_embed_mode, package_id_python_mode, package_id_unknown_mode` are class attributes that can be defined in recipes to define the effect they have on their consumers’ `package_id`, when they are consumed as `requires`.

The `build_mode` (experimental) is a class attribute that affects the package consumers when these consumers use it as `tool_requires`. Can be declared as:

```python
from conan import ConanFile

class Pkg(ConanFile):
    name = "pkg"
    version = "1.0.0"
    # They are not mandatory, and it is not necessary to define all
    package_id_embed_mode = "full_mode"
    package_id_non_embed_mode = "patch_mode"
    package_id_unknown_mode = "minor_mode"
    package_id_python_mode = "major_mode"
    build_mode = "patch_mode"  # (experimental) when used as tool_requires
```

In general, the Conan defaults are good ones, and allow providing users good control over when the consumers need to be re-built from source or not. Also, the Conan defaults can be changed globally in the `global.conf` file (they should be changed globally for all users, CI, etc.) via the `core.package_id:xxxx` configurations. The in-recipe attribute definition is useful to define behavior that deviates from the defaults.

Possible values are (following the semver definition of MAJOR.MINOR.PATCH):

- `patch_mode`: New patches, minors, and major releases of the package will require a new binary (new `package_id`) of the consumers. New recipe revisions will not require new binaries of the consumers. For example if we create a new `pkg/1.0.1` version and some consumer has `requires = "pkg/[>=1.0 <2.0]"`, such a consumer will build a new binary against this specific new `1.0.1` version. But if we just change the recipe, producing a new `recipe_revision`, the consumers will not require building a new binary.
- `minor_mode`: New minor and major releases of this package will require a new binary of the consumers. New patches and new revisions will not require new binaries of the consumers. This is the default for the “non-embed-mode”, as it allows fine control by the users to decide when to rebuild things or not.
- `major_mode`: Only new major releases will require new binaries. Any other modifications and new versions will not require new binaries from the consumers.
- `full_mode`: The full identifier of this package, including `pkgname/version@user/channel#recipe_revision:package_id` will be used in the consumers `package_id`, then requiring to build a new binary of the consumer for every change of this package (as any change either in source or configuration will produce a different `recipe_revision` or `package_id` respectively). This is the default for the “embed-mode”.
- `unrelated_mode`: No change in this package will ever produce a new binary in the consumer.
- `revision_mode`: Uses the `pkgname/version@user/channel#recipe_revision` in the consumers’ `package_id`, that is the full reference except the `package_id` of the dependency.
- `semver_mode`: Equivalent to `major_mode` if the version is `>=1.0`, or equivalent to `patch_mode` (or the full version if it has more than 3 digits) if the version is `<1.0`.

The 4 different attributes are:

- `package_id_embed_mode`: Define the mode for “embedding” cases, that is, a shared library linking a static library, an application linking a static library, an application or a library linking a header-only library. The default for this mode is `full_mode`
- `package_id_non_embed_mode`. Define the mode for “non-embedding” cases, that is, a shared library linking another shared library, a static library linking another static library, an application executable linking a shared library. The default for this mode is `minor_mode`.
- `package_id_unknown_mode`: Define the mode when the relationship between packages is unknown. If it is not possible to deduce the package type, because there are no `shared` or `header_only` options defined, or because `package_type` is not defined, then, this mode will be used. The default for this mode is `semver_mode` (similar to Conan 1.X behavior).
- `package_id_python_mode`: Define the mode for consumers of `python_requires`. By default it will be `minor_mode`, and it is strongly recommended to use this default, and not define the `package_id_python_mode`. This attribute is provided for completeness and exceptional cases like temporary migrations.
- `build_mode`: (Experimental) Define the mode for consumers using this dependency as `tool_requires`. By default is `None`, which means that the `tool_requires` does not affect directly the `package_id` of their consumers. Enabling this `build_mode` introduces a harder dependency to the `tool_requires` that will be needed to resolve the `package_id` of the consumers in more cases.

#### SEE ALSO
Read the [binary model reference](https://docs.conan.io/2//reference/binary_model.html.md#reference-binary-model) for a full view of the Conan binary model.

<a id="reference-conanfile-attributes-package-id-abi-options"></a>

### package_id_abi_options

There are some scenarios when it might be desired to make the value of a given option to influence the
`package_id` of the binaries consuming this package.

This is generally not necessary in most of the cases, as the default binary model is good for the majority of
scenarios. For example, in all `embed` modes, the full dependency reference, including its `package_id`,
that already encodes the dependency options, are already factored in into the consumer `package_id`.
So for that case, the dependency’s options already have this effect on the consumer `package_id`.

But there might be some cases for `non_embed`, like a static library that could be linking a dependency
sometimes as a static library and sometimes as a shared library. In platforms such as Linux or Mac, the
linkage doesn’t really change the consumer. But this case for Windows `msvc` compiler, when the dependency
is conditionally defining `dllimport` in their headers, the calling convention changes, and the binary
of the consumer is different.

For shared libraries in Windows, it is common to find this idiom:

```cpp
#ifdef WIN32
    #define HELLO_EXPORT __declspec(dllexport)
#else
    #define HELLO_EXPORT
#endif

HELLO_EXPORT void hello();
```

To export the `hello()` symbol into the shared library, as in Windows MSVC the symbols are not exported
by default.
This is not an issue, as the consumer packages and callers of `hello()` will not change its linkage.

But in some cases, some libraries might decide to define something like:

```cpp
#ifdef WIN32
    #ifdef libhello_EXPORTS
        /* We are building this library */
        #define HELLO_EXPORT __declspec(dllexport)
    #else
        /* We are using this library */
        #define HELLO_EXPORT __declspec(dllimport)
    #endif
#else
    #define HELLO_EXPORT
#endif

HELLO_EXPORT void hello();
```

And control via `libhello_EXPORTS` if the package is being built or consumed. In this case, the consumer
will have a different linkage when linking this shared library with the `dllimport`, than when linking
this library as a static library.

For those case, the package recipe can define which of its own options affect the consumers `package_id`,
irrespective of the `non_embed` mode, so they can still generate different binaries for the different
linkages, without necessarily resorting to a full `embed` mode that will require unnecessary rebuilds of
binaries from source.

This can be defined with:

```python
from conan import ConanFile

class Pkg(ConanFile):
    name = "pkg"
    version = "1.0.0"
    options = {"shared": [False, True]}

    package_id_abi_options = ["shared"]
```

And that will make all the consumers of `pkg/1.0.0` to automatically factor the `pkg/*:shared=True/False` value
in their own `package_id`.

### context

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The `conanfile.py` recipe attribute `context` will contain either the “build” or “host” value to represent the context where
the current package instance is being evaluated. Recall that it is possible that some recipes might exist both in the “build” and “host”
contexts, depending on the usage.

This attribute shouldn’t be necessary for the vast majority of cases, so it is recommended to avoid using it.
One potential exception for this recommendation would be to break otherwise infinite dependency cycles, defining
some conditional dependency as:

```python
def requirements(self):
    if self.context == "host":
        self.tool_requires("mytool/1.0")
```

## Build

### generators

List or tuple of strings with names of generators.

```python
class MyLibConan(ConanFile):
    generators = "CMakeDeps", "CMakeToolchain"
```

The generators can also be instantiated explicitly in the [generate() method](https://docs.conan.io/2//reference/conanfile/methods/generate.html.md#reference-conanfile-methods-generate).

```python
from conan.tools.cmake import CMakeToolchain

class MyLibConan(ConanFile):
    ...

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
```

### build_policy

Controls when the current package is built during a `conan install`.
The allowed values are:

- `"missing"`: Conan builds it from source if there is no binary available.
- `"never"`: This package cannot be built from sources, it is always created with
  `conan export-pkg`
- `None` (default value): This package won’t be built unless the policy is specified
  in the command line (e.g `--build=foo*`)
  > ```python
  >  class PocoTimerConan(ConanFile):
  >      build_policy = "missing"
  > ```

### win_bash

When `True` it enables the new run in a subsystem bash in Windows mechanism.

```python
from conan import ConanFile

class FooRecipe(ConanFile):
    ...
    win_bash = True
```

It can also be declared as a `property` based on any condition:

```python
from conan import ConanFile

class FooRecipe(ConanFile):
    ...


    @property
    def win_bash(self):
        return self.settings.arch == "armv8"
```

### win_bash_run

When `True` it enables running commands in the `"run"` scope, to run them inside a bash shell.

```python
from conan import ConanFile

class FooRecipe(ConanFile):

    ...

    win_bash_run = True
    def build(self):
        self.run(cmd, scope="run")  # will run <cmd> inside bash
```

## Folders and layout

<a id="conan-conanfile-properties-folders"></a>

<a id="conan-conanfile-properties-source-folder"></a>

### source_folder

The folder in which the source code lives. The path is built joining the base directory
(a cache directory when running in the cache or the `output folder` when running locally)
with the value of `folders.source` if declared in the `layout()` method.

Note that the base directory for the `source_folder` when running in the cache will point to the base folder of the
build unless [no_copy_source](#conan-conanfile-properties-no-copy-source) is set to `True`. But anyway it will
always point to the correct folder where the source code is.

### export_sources_folder

The value depends on the method you access it:

- At `source(self)`: Points to the base source folder (that means self.source_folder but
  without taking into account the `folders.source` declared in the `layout()` method).
  The declared exports_sources are copied to that base source folder always.
- At `exports_sources(self)`: Points to the folder in the cache where the export sources
  have to be copied.

#### SEE ALSO
- [Read about the export_sources() method](https://docs.conan.io/2//reference/conanfile/methods/export_sources.html.md#reference-conanfile-methods-export-sources).
- [Read about the source() method](https://docs.conan.io/2//reference/conanfile/methods/source.html.md#reference-conanfile-methods-source).

<a id="attribute-build-folder"></a>

### build_folder

The folder used to build the source code. The path is built joining the base directory (a cache
directory when running in the cache or the `output folder` when running locally) with
the value of `folders.build` if declared in the `layout()` method.

<a id="attribute-generators-folder"></a>

### generators_folder

The folder where the files in the `generate()` method should be generated. The path is built
from the layout’s `self.folders.generators` attribute.

<a id="conan-conanfile-properties-package-folder"></a>

### package_folder

The folder to copy the final artifacts for the binary package. In the local cache a package
folder is created for every different package ID.

The most common usage of `self.package_folder` is to `copy` the files
at the [package() method](https://docs.conan.io/2//reference/conanfile/methods/package.html.md#reference-conanfile-methods-package):

```python
import os
from conan import ConanFile
from conan.tools.files import copy

class MyRecipe(ConanFile):
    ...

    def package(self):
        copy(self, "*.so", self.build_folder, os.path.join(self.package_folder, "lib"))
        ...
```

### recipe_folder

The folder where the recipe *conanfile.py* is stored, either in the local folder or in
the cache. This is useful in order to access files that are exported along with the recipe,
or the origin folder when exporting files in `export(self)` and `export_sources(self)`
methods.

The most common usage of `self.recipe_folder` is in the `export(self)` and `export_sources(self)` methods,
as the folder from where we copy the files:

```python
from conan import ConanFile
from conan.tools.files import copy

class MethodConan(ConanFile):
    exports = "file.txt"
    def export(self):
        copy(self, "LICENSE.md", self.recipe_folder, self.export_folder)
```

### recipe_metadata_folder

The `self.recipe_metadata_folder` (**experimental**) can be used in the `export()` and `export_sources()` and `source()` methods
to save or copy **recipe** metadata files. See [metadata section](https://docs.conan.io/2//devops/metadata.html.md#devops-metadata) for more information.

### package_metadata_folder

The `self.package_metadata_folder` (**experimental**)  can be used in the `generate()`, `build()` and `package()` methods
to save or copy **package** metadata files. See [metadata section](https://docs.conan.io/2//devops/metadata.html.md#devops-metadata) for more information.

<a id="conan-conanfile-properties-no-copy-source"></a>

### no_copy_source

The attribute `no_copy_source` tells the recipe that the source code will not be copied from
the `source_folder` to the `build_folder`. This is mostly an optimization for packages
with large source codebases or header-only, to avoid extra copies.

If you activate `no_copy_source=True`, it is **mandatory** that the source code must not be modified at all by
the configure or build scripts, as the source code will be shared among all builds.

The recipes should always use `self.source_folder` attribute, which will point to the `build`
folder when `no_copy_source=False` and will point to the `source` folder when `no_copy_source=True`.

#### SEE ALSO
Read  [header-only packages section](https://docs.conan.io/2//tutorial/creating_packages/other_types_of_packages/header_only_packages.html.md#creating-packages-other-header-only) for an
example using `no_copy_source` attribute.

<a id="conan-conanfile-attributes-test-package-folder"></a>

### test_package_folder

The `test_package_folder` class attribute allows defining in recipe a different default
`test_package` folder for `conan create` commands.
When a `conan create` runs, after the package is created in the cache, it will look for
a `test_package` folder, or for the folder specified in the `--test-folder=xxx` argument,
and launch the package test.

This attribute allows to change that default name:

```python
import os
from conan import ConanFile

class Pkg(ConanFile):
    test_package_folder = "my/test/folder"
```

It allows to define any folder, always relative to the location of the `conanfile.py`.

## Layout

<a id="conan-conanfile-attributes-folders"></a>

### folders

The `folders` attribute has to be set only in the `layout()` method. Please check the
[layout() method documentation](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md#layout-folders-reference) to learn more about this
attribute.

<a id="conan-conanfile-attributes-cpp"></a>

### cpp

Object storing all the information needed by the consumers
of a package: include directories, library names, library paths… Both for editable
and regular packages in the cache. It is only available at the `layout()` method.

- `self.cpp.package`: For a regular package being used from the Conan cache. Same as
  declaring `self.cpp_info` at the `package_info()` method.
- `self.cpp.source`: For “editable” packages, to describe the artifacts under
  `self.source_folder`
- `self.cpp.build`: For “editable” packages, to describe the artifacts under
  `self.build_folder`.

The `cpp` attribute has to be set only in the `layout()` method. Please check the
[layout() method documentation](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md#layout-cpp-reference) to learn more about this
attribute.

### layouts

The `layouts` attribute has to be set only in the `layout()` method. Please check the
[layout() method documentation](https://docs.conan.io/2//reference/conanfile/methods/layout.html.md#layout-cpp-reference) to learn more about this
attribute.

The `layouts` attribute contains information about environment variables and `conf` that
would be path-dependent, and as a result it would contain a different value when the package
is in editable mode, or when the package is in the cache. The `layouts` sub-attributes are:

- `self.layouts.build`: information related to the relative `self.folders.build`
- `self.layouts.source`: information related to the relative `self.folders.source`
- `self.layouts.package`: information related to the final `package_folder`

Each one of those will contain:

- `buildenv_info`: environment variables build information for consumers (equivalent to `self.buildenv_info` in `package_info()`)
- `runenv_info`: environment variables run information for consumers (equivalent to `self.runenv_info` in `package_info()`)
- `conf_info`: configuration information for consumers (equivalent to `self.conf_info` in `package_info()`). Note this is
  only automatically propagated to `self.conf` of consumers when this package is a direct `tool_require`.

For example, if we had an `androidndk` recipe that contains the AndroidNDK, and we want to have that recipe in “editable” mode,
it is necessary where the androidndk will be locally, before being in the created package:

```python
import os
from conan import ConanFile
from conan.tools.files import copy

class AndroidNDK(ConanFile):

    def layout(self):
        # When developing in user space it is in a "mybuild" folder (relative to current dir)
        self.layouts.build.conf_info.define_path("tools.android:ndk_path", "mybuild")
        # but when packaged it will be in a "mypkg" folder (inside the cache package folder)
        self.layouts.package.conf_info.define_path("tools.android:ndk_path", "mypkg")

    def package(self):
        copy(self, "*", src=os.path.join(self.build_folder, "mybuild"),
             dst=os.path.join(self.package_folder, "mypkg"))
```

## Package information for consumers

### cpp_info

Same as using `self.cpp.package` in the `layout()` method. Use it if you need to read
the `package_folder` to locate the already located artifacts.

#### SEE ALSO
- [CppInfo](https://docs.conan.io/2//reference/conanfile/methods/package_info.html.md#conan-conanfile-model-cppinfo) model.

#### IMPORTANT
This attribute is only defined inside `package_info()` method being None elsewhere.

<a id="conan-conanfile-attributes-buildenv-info"></a>

### buildenv_info

For the dependant recipes, the declared environment variables will be present during the
build process. Should be only filled in the `package_info()` method.

#### IMPORTANT
This attribute is only defined inside `package_info()` method being None elsewhere.

```python
def package_info(self):
    self.buildenv_info.append_path("PATH", self.package_folder)
```

#### SEE ALSO
Check the reference of the [Environment](https://docs.conan.io/2//reference/tools/env/environment.html.md#conan-tools-env-environment-model) object to know how to fill
the `self.buildenv_info`.

<a id="conan-conanfile-attributes-runenv-info"></a>

### runenv_info

For the dependant recipes, the declared environment variables will be present at runtime.
Should be only filled in the `package_info()` method.

#### IMPORTANT
This attribute is only defined inside `package_info()` method being None elsewhere.

```python
def package_info(self):
    self.runenv_info.define_path("RUNTIME_VAR", "c:/path/to/exe")
```

#### SEE ALSO
Check the reference of the [Environment](https://docs.conan.io/2//reference/tools/env/environment.html.md#conan-tools-env-environment-model) object to know how to fill
the `self.runenv_info`.

<a id="conan-conanfile-attributes-conf-info"></a>

### conf_info

Configuration variables to be passed to the dependant recipes.
Should be only filled in the `package_info()` method.

```python
class Pkg(ConanFile):
    name = "pkg"

    def package_info(self):
        self.conf_info.define("tools.build:verbosity", "debug")
        self.conf_info.get("tools.build:verbosity")  # == "debug"
        self.conf_info.append("user.myconf.build:ldflags", "--flag3")  # == ["--flag1", "--flag2", "--flag3"]
        self.conf_info.update("tools.microsoft.msbuildtoolchain:compile_options", {"ExpandAttributedSource": "false"})
        self.conf_info.unset("tools.microsoft.msbuildtoolchain:compile_options")
        self.conf_info.remove("user.myconf.build:ldflags", "--flag1")  # == ["--flag0", "--flag2", "--flag3"]
        self.conf_info.pop("tools.system.package_manager:sudo")
```

#### SEE ALSO
Read here [the complete reference of self.conf_info](https://docs.conan.io/2//reference/conanfile/methods/package_info.html.md#conan-conanfile-model-conf-info).

### generator_info

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

Generators to be passed to the dependant recipes.
Should be only filled in the `package_info()` method, `None` by default.

#### SEE ALSO
See [an example usage here](https://docs.conan.io/2//reference/extensions/custom_generators.html.md#reference-commands-custom-generators-tool-requires)
and [the complete reference of self.generator_info](https://docs.conan.io/2//reference/conanfile/methods/package_info.html.md#conan-conanfile-model-generator-info).

### deprecated

This attribute declares that the recipe is deprecated, causing a user-friendly warning
message to be emitted whenever it is used

For example, the following code:

```python
from conan import ConanFile

class Pkg(ConanFile):
    name = "cpp-taskflow"
    version = "1.0"
    deprecated = True
```

may emit a `risk` warning like:

```bash
Deprecated
    cpp-taskflow/1.0

WARN: risk: There are deprecated packages in the graph
```

Optionally, the attribute may specify the name of the suggested replacement:

```python
from conan import ConanFile

class Pkg(ConanFile):
    name = "cpp-taskflow"
    version = "1.0"
    deprecated = "Not secure, use better taskflow>1.2.3"
```

This will emit a `risk` warning like:

```bash
Deprecated
    cpp-taskflow/1.0: Not secure, use better taskflow>1.2.3

WARN: risk: There are deprecated packages in the graph
```

If the value of the attribute evaluates to `False`, no warning is printed.

### provides

This attribute declares that the recipe provides the same functionality as other recipe(s).
The attribute is usually needed if two or more libraries implement the same API to prevent
link-time and run-time conflicts (ODR violations). One typical situation is forked libraries.
Some examples are:

- [LibreSSL](https://www.libressl.org/), [BoringSSL](https://boringssl.googlesource.com/boringssl/) and [OpenSSL](https://www.openssl.org/)
- [libav](https://en.wikipedia.org/wiki/Libav) and [ffmpeg](https://ffmpeg.org/)
- [MariaDB client](https://downloads.mariadb.org/client-native) and [MySQL client](https://dev.mysql.com/downloads/c-api/)

If Conan encounters two or more libraries providing the same functionality within a single graph, it raises an error:

```bash
At least two recipes provides the same functionality:
- 'libjpeg' provided by 'libjpeg/9d', 'libjpeg-turbo/2.0.5'
```

The attribute value should be a string with a recipe name or a tuple of such recipe names.

For example, to declare that `libjpeg-turbo` recipe offers the same functionality as `libjpeg` recipe, the following code could be used:

```python
from conan import ConanFile

class LibJpegTurbo(ConanFile):
    name = "libjpeg-turbo"
    version = "1.0"
    provides = "libjpeg"
```

To declare that a recipe provides the functionality of several different recipes at the same time, the following code could be used:

```python
from conan import ConanFile

class OpenBLAS(ConanFile):
    name = "openblas"
    version = "1.0"
    provides = "cblas", "lapack"
```

If the attribute is omitted, the value of the attribute is assumed to be equal to the current package name. Thus, it’s redundant for
`libjpeg` recipe to declare that it provides `libjpeg`, it’s already implicitly assumed by Conan.

## Other

### dependencies

Conan recipes provide access to their dependencies via the `self.dependencies` attribute.

```python
class Pkg(ConanFile):
    requires = "openssl/0.1"

    def generate(self):
        openssl = self.dependencies["openssl"]
        # access to members
        openssl.ref.version
        openssl.ref.revision # recipe revision
        openssl.options
        openssl.settings
```

#### SEE ALSO
Read here [the complete reference of self.dependencies](https://docs.conan.io/2//reference/conanfile/methods/generate.html.md#conan-conanfile-model-dependencies).

<a id="conan-conanfile-attribute-other-subgraph"></a>

### subgraph

(Experimental) A read-only dependency graph of the recipe. The `dependencies` attribute should be used to access the dependencies of the recipe,
as this attribute is intended to be passed to other Conan APIs and exposed for advanced usages like [SBOM generation](https://docs.conan.io/2//reference/tools/sbom.html.md#conan-tools-sbom).

### conf

In the `self.conf` attribute we can find all the conf entries declared in the [[conf]](https://docs.conan.io/2//reference/config_files/profiles.html.md#reference-config-files-profiles-conf)  section of the profiles.
in addition of the declared [self.conf_info](https://docs.conan.io/2//reference/conanfile/methods/package_info.html.md#conan-conanfile-model-conf-info) entries from the first level tool requirements.
The profile entries have priority.

```python
from conan import ConanFile

class MyConsumer(ConanFile):

  tool_requires = "my_android_ndk/1.0"

  def generate(self):
      # This is declared in the tool_requires
      self.output.info("NDK host: %s" % self.conf.get("tools.android:ndk_path"))
      # This is declared in the profile at [conf] section
      self.output.info("Custom var1: %s" % self.conf.get("user.custom.var1"))
```

#### NOTE
The `conf` attribute is a **read-only** attribute. It can only be defined in profiles and command lines, but it should never be set by recipes.
Recipes can only read its value via `self.conf.get()` method.

### Output

<a id="conanfile-output-attribute"></a>

### Output contents

Use the `self.output` attribute to print contents to the output.

```python
self.output.success("This is good, should be green")
self.output.info("This is neutral, should be white")
self.output.warning("This is a warning, should be yellow")
self.output.error("Error, should be red")
```

Additional output methods are available and you can produce different outputs with different colors.
See [the output documentation](https://docs.conan.io/2//reference/conanfile/running_and_output.html.md#reference-conanfile-output) for the list of available output methods.

<a id="revision-mode-attribute"></a>

### revision_mode

This attribute allow each recipe to declare how the revision for the recipe itself should
be computed. It can take three different values:

- `"hash"` (by default): Conan will use the checksum hash of the recipe manifest to
  compute the revision for the recipe.
- `"scm"`: if the project is inside a Git repository the commit ID will be used as the
  recipe revision. If there is no repository it will raise an error.
- `"scm_folder"`: This configuration applies when you have a mono-repository project, but
  still want to use *scm* revisions. In this scenario, the revision of the exported
  conanfile.py will correspond to the commit ID of the folder where it’s located. This
  approach allows multiple conanfile.py files to exist within the same Git repository,
  with each file exported under its distinct revision.

When `scm` or `scm_folder` is selected, the Git commit will be used, but by default
the repository must be clean, otherwise it would be very likely that there are uncommitted
changes and the build wouldn’t be reproducible. So if there are dirty files, Conan will raise
an error.

If there are files that can be dirty in the repo, but do not belong at all to the
recipe or the package, then it is possible to exclude them from the check with the
`revision_mode_excluded` recipe attribute or the `core.scm:excluded`
configuration, which is a list of patterns (fnmatch) to exclude.

```python
from conan import ConanFile

class MyConsumer(ConanFile):

  revision_mode = "scm"
  # the .tmp files are excluded from revision and dirty check
  revision_mode_excluded = ["*.tmp"]
```

### upload_policy

Controls when the current package built binaries are uploaded or not

- `"skip"`: The precompiled binaries are not uploaded. This is useful for “installer”
  packages that just download and unzip something heavy (e.g. android-ndk), and is useful
  together with the `build_policy = "missing"`
  > ```python
  > class Pkg(ConanFile):
  >     upload_policy = "skip"
  > ```

### required_conan_version

Recipes can define a module level `required_conan_version` that defines a valid version range of
Conan versions that can load and understand the current `conanfile.py`. The syntax is:

```python
from conan import ConanFile

required_conan_version = ">=2.0"

class Pkg(ConanFile):
    pass
```

Version ranges as in `requires` are allowed.
Also there is a `global.conf` file `core:required_conan_version` configuration that can
define a global minimum, maximum or exact Conan version to run, which can be very convenient
to maintain teams of developers and CI machines to use the desired range of versions.

<a id="conan-conanfile-attributes-implements"></a>

### implements

A list is used to define a series of option configurations that Conan will handle
automatically. This is especially handy for avoiding boilerplate code that tends to repeat
in most of the recipes. The syntax is as follows:

```python
from conan import ConanFile

class Pkg(ConanFile):
    implements = ["auto_shared_fpic", "auto_header_only", ...]
```

Currently these are the automatic implementations provided by Conan:

- `"auto_shared_fpic"`: automatically manages `fPIC` and `shared` options. Adding this
  implementation will have both effect in the
  [configure](https://docs.conan.io/2//reference/conanfile/methods/configure.html.md#reference-conanfile-methods-configure-implementations) and
  [config_options](https://docs.conan.io/2//reference/conanfile/methods/config_options.html.md#reference-conanfile-methods-config-options-implementations) steps
  when those methods are not explicitly defined in the recipe.
- `"auto_header_only"`: automatically manages the package ID clearing settings. Adding this
  implementation will have effect in the
  [package_id](https://docs.conan.io/2//reference/conanfile/methods/package_id.html.md#reference-conanfile-methods-package-id-implementations) step
  when the method is not explicitly defined in the recipe.

#### WARNING
This is a 2.0-only feature, and it will not work in 1.X

### alias

#### WARNING
While aliases can technically still be used in Conan 2, their usage is not recommended
and they may be fully removed in future releases. Users are encouraged to adapt to the
[newer versioning features](https://docs.conan.io/2//devops/versioning/versioning.html.md#devops-versioning) for a more standardized and efficient
package management experience.

In Conan 2, the `alias` attribute remains a part of the recipe, allowing users to define
an alias for a package version. Normally, you would create one using the `conan new`
command with the `alias` template and the exporting the recipe with conan export:

```shell
$ conan new alias -d name=mypkg -d version=latest -d target=1.0
$ conan export .
```

Note that when requiring the alias, you must place the version in parentheses `()` to
explicitly declare the use of an alias as a requirement:

```python
class Consumer(ConanFile):

    ...
    requires = "mypkg/(latest)"
    ...
```

<a id="conan-conanfile-attributes-extension-properties"></a>

### extension_properties

The `extensions_properties` attribute is a dictionary intended to define and pass information from the
recipes to the Conan extensions.

At the moment, the only defined properties are `compatibility_cppstd` and `compatibility_cstd`, that allows disabling the behavior
of [the default compatibility.py extension](https://docs.conan.io/2//reference/extensions/binary_compatibility.html.md#reference-extensions-binary-compatibility), that considers
binaries built with different `compiler.cppstd` and `compiler.cstd` values ABI-compatible among them.
To disable this behavior for the current package, it is possible to do it with:

```python
class Pkg(ConanFile):
    extension_properties = {"compatibility_cppstd": False}
```

If it is necessary to do it conditionally, it is also possible to define its value inside recipe `compatibility()`
method:

```python
class Pkg(ConanFile):

    def compatibility(self):
        self.extension_properties = {"compatibility_cppstd": False}
```

#### NOTE
The value of `extension_properties` is not transitive from the dependencies to the consumers by default, but can be
propagated manually by iterating the `self.dependencies` and checking the desired values of their `extension_properties`.
