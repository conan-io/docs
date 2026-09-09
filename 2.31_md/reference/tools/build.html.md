<a id="conan-tools-build"></a>

# conan.tools.build

## Building

### conan.tools.build.build_jobs()

### build_jobs(conanfile)

Returns the number of CPUs available for parallel builds.
It returns the configuration value for `tools.build:jobs` if exists, otherwise,
it defaults to the helper function `_cpu_count()`.
`_cpu_count()` reads cgroup to detect the configured number of CPUs.
Currently, there are two versions of cgroup available.

In the case of cgroup v1, if the data in cgroup is invalid, processor detection comes into play.
Whenever processor detection is not enabled, `build_jobs()` will safely return 1.

In the case of cgroup v2, if no limit is set, processor detection is used. When the limit is set,
the behavior is as described in cgroup v1.

* **Parameters:**
  **conanfile** – The current recipe object. Always use `self`.
* **Returns:**
  `int` with the number of jobs

<a id="conan-tools-build-cross-building"></a>

### conan.tools.build.cross_building()

### cross_building(conanfile=None, skip_x64_x86=False)

Check if we are cross building comparing the *build* and *host* settings. Returns `True`
in the case that we are cross-building.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **skip_x64_x86** – Do not consider cross building when building to 32 bits from 64 bits:
    x86_64 to x86, sparcv9 to sparc or ppc64 to ppc32
* **Returns:**
  `bool` value from `tools.build.cross_building:cross_build` if exists, otherwise,
  it returns `True` if we are cross-building, else, `False`.

<a id="conan-tools-build-can-run"></a>

### conan.tools.build.can_run()

### can_run(conanfile)

Validates whether is possible to run a non-native app on the same architecture.
It’s a useful feature for the case your architecture can run more than one target.
For instance, Mac M1 machines can run both armv8 and x86_64.

* **Parameters:**
  **conanfile** – The current recipe object. Always use `self`.
* **Returns:**
  `bool` value from `tools.build.cross_building:can_run` if exists, otherwise,
  it returns `False` if we are cross-building, else, `True`.

## Cppstd

<a id="conan-tools-build-check-min-cppstd"></a>

### conan.tools.build.check_min_cppstd()

### check_min_cppstd(conanfile, cppstd, gnu_extensions=False)

Check if current cppstd fits the minimal version required.

> In case the current cppstd doesn’t fit the minimal version required
> by cppstd, a ConanInvalidConfiguration exception will be raised.

> settings.compiler.cppstd must be defined, otherwise ConanInvalidConfiguration is raised
* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cppstd** – Minimal cppstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17)

<a id="conan-tools-build-check-max-cppstd"></a>

### conan.tools.build.check_max_cppstd()

### check_max_cppstd(conanfile, cppstd, gnu_extensions=False)

Check if current cppstd fits the maximum version required.

> In case the current cppstd doesn’t fit the maximum version required
> by cppstd, a ConanInvalidConfiguration exception will be raised.

> settings.compiler.cppstd must be defined, otherwise ConanInvalidConfiguration is raised
* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cppstd** – Maximum cppstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17)

### conan.tools.build.valid_min_cppstd()

### valid_min_cppstd(conanfile, cppstd, gnu_extensions=False)

Validate if current cppstd fits the minimal version required.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cppstd** – Minimal cppstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17). This option ONLY works on Linux.
* **Returns:**
  True, if current cppstd matches the required cppstd version. Otherwise, False.

### conan.tools.build.valid_max_cppstd()

### valid_max_cppstd(conanfile, cppstd, gnu_extensions=False)

Validate if current cppstd fits the maximum version required.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cppstd** – Maximum cppstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17). This option ONLY works on Linux.
* **Returns:**
  True, if current cppstd matches the required cppstd version. Otherwise, False.

### conan.tools.build.default_cppstd()

### default_cppstd(conanfile, compiler=None, compiler_version=None)

Get the default `compiler.cppstd` for the “conanfile.settings.compiler” and “conanfile
settings.compiler_version” or for the parameters “compiler” and “compiler_version” if specified.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **compiler** – Name of the compiler e.g. gcc
  * **compiler_version** – Version of the compiler e.g. 12
* **Returns:**
  The default `compiler.cppstd` for the specified compiler

### conan.tools.build.supported_cppstd()

### supported_cppstd(conanfile, compiler=None, compiler_version=None)

Get a list of supported `compiler.cppstd` for the “conanfile.settings.compiler” and
“conanfile.settings.compiler_version” or for the parameters “compiler” and “compiler_version”
if specified.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **compiler** – Name of the compiler e.g: gcc
  * **compiler_version** – Version of the compiler e.g: 12
* **Returns:**
  a list of supported `cppstd` values.

### conan.tools.build.cppstd_flag()

### cppstd_flag(conanfile) → str

Returns flags specific to the C++ standard based on the `conanfile.settings.compiler`,
`conanfile.settings.compiler.version` and `conanfile.settings.compiler.cppstd`.

It also considers when using GNU extension in `settings.compiler.cppstd`, reflecting it in the
compiler flag. Currently, it supports GCC, Clang, AppleClang, MSVC, Intel, MCST-LCC.

In case there is no `settings.compiler` or `settings.cppstd` in the profile, the result will
be an **empty string**.

* **Parameters:**
  **conanfile** – The current recipe object. Always use `self`.
* **Returns:**
  `str` with the standard C++ flag used by the compiler. e.g. “-std=c++11”, “/std:c++latest”

## cstd

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

<a id="conan-tools-build-check-min-cstd"></a>

### conan.tools.build.check_min_cstd()

### check_min_cstd(conanfile, cstd, gnu_extensions=False)

Check if current cstd fits the minimal version required.

> In case the current cstd doesn’t fit the minimal version required
> by cstd, a ConanInvalidConfiguration exception will be raised.

> 1. If settings.compiler.cstd, the tool will use settings.compiler.cstd to compare
> 2. It not settings.compiler.cstd, the tool will use compiler to compare (reading the
>    default from cstd_default)
> 3. If not settings.compiler is present (not declared in settings) will raise because it
>    cannot compare.
> 4. If can not detect the default cstd for settings.compiler, a exception will be raised.
* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cstd** – Minimal cstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17)

<a id="conan-tools-build-check-max-cstd"></a>

### conan.tools.build.check_max_cstd()

### check_max_cstd(conanfile, cstd, gnu_extensions=False)

Check if current cstd fits the maximum version required.

> In case the current cstd doesn’t fit the maximum version required
> by cstd, a ConanInvalidConfiguration exception will be raised.

> 1. If settings.compiler.cstd, the tool will use settings.compiler.cstd to compare
> 2. It not settings.compiler.cstd, the tool will use compiler to compare (reading the
>    default from cstd_default)
> 3. If not settings.compiler is present (not declared in settings) will raise because it
>    cannot compare.
> 4. If can not detect the default cstd for settings.compiler, a exception will be raised.
* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cstd** – Maximum cstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17)

### conan.tools.build.valid_min_cstd()

### valid_min_cstd(conanfile, cstd, gnu_extensions=False)

Validate if current cstd fits the minimal version required.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cstd** – Minimal cstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17). This option ONLY works on Linux.
* **Returns:**
  True, if current cstd matches the required cstd version. Otherwise, False.

### conan.tools.build.valid_max_cstd()

### valid_max_cstd(conanfile, cstd, gnu_extensions=False)

Validate if current cstd fits the maximum version required.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **cstd** – Maximum cstd version required
  * **gnu_extensions** – GNU extension is required (e.g gnu17). This option ONLY works on Linux.
* **Returns:**
  True, if current cstd matches the required cstd version. Otherwise, False.

### conan.tools.build.default_cstd()

### default_cstd(conanfile, compiler=None, compiler_version=None)

Get the default `compiler.cstd` for the “conanfile.settings.compiler” and “conanfile
settings.compiler_version” or for the parameters “compiler” and “compiler_version” if specified.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **compiler** – Name of the compiler e.g. gcc
  * **compiler_version** – Version of the compiler e.g. 12
* **Returns:**
  The default `compiler.cstd` for the specified compiler

### conan.tools.build.supported_cstd()

### supported_cstd(conanfile, compiler=None, compiler_version=None)

Get a list of supported `compiler.cstd` for the “conanfile.settings.compiler” and
“conanfile.settings.compiler_version” or for the parameters “compiler” and “compiler_version”
if specified.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **compiler** – Name of the compiler e.g: gcc
  * **compiler_version** – Version of the compiler e.g: 12
* **Returns:**
  a list of supported `cstd` values.

## Compiler

### conan.tools.build.check_min_compiler_version()

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

### check_min_compiler_version(conanfile, compiler_restrictions)

(Experimental) Checks if the current compiler and its version meet the minimum requirements.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **compiler_restrictions** – 

    A list of tuples, where each tuple contains:
    - **compiler** (*str*): The name of the compiler (e.g., “gcc”, “msvc”).
    - **min_version** (*str*): The minimum required version as a string (e.g., “14”, “19.0”).
    - **reason** (*str*): A string explaining the reason for the version requirement.
* **Raises:**
  * **ConanException** – If the ‘compiler’ or ‘compiler.version’ settings are not defined.
  * **ConanInvalidConfiguration** – If the found compiler version is less than the specified minimum version for that compiler.
* **Example:**
  ```python
  def validate(self):
      compiler_restrictions = [
          ("clang", "14", "requires C++20 coroutines support"),
          ("gcc", "12", "requires C++20 modules support")
      ]
      check_min_compiler_version(self, compiler_restrictions)
  ```
