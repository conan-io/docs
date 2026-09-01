<a id="reference-config-files-global-conf"></a>

# global.conf

The **global.conf** file is located in the Conan user home directory, e.g.,  *[CONAN_HOME]/global.conf*. If it does not
already exist, a default one is automatically created.

## Introduction to configuration

*global.conf* is aimed to save some core/tools/user configuration variables that will be used by Conan. For instance:

* Package ID modes.
* General HTTP(python-requests) configuration.
* Number of retries when downloading/uploading recipes.
* Related tools configurations (used by toolchains, helpers, etc.)
* [Policies](https://docs.conan.io/2//reference/policies.html.md#reference-policies), which are a set of rules to enforce certain behaviors from Conan.
* Others (required Conan version, CLI non-interactive, etc.)

Let’s briefly explain the three types of existing configurations:

* `core.*`: aimed to configure values of Conan core behavior (download retries, package ID modes, etc.).
  Only definable in *global.conf* file.
* `tools.*`: aimed to configure values of Conan tools (toolchains, build helpers, etc.) used in your recipes.
  Definable in both *global.conf* and [profiles](https://docs.conan.io/2//reference/config_files/profiles.html.md#reference-config-files-profiles).
* `user.*`: aimed to define personal user configurations. They can define whatever user wants.
  Definable in both *global.conf* and [profiles](https://docs.conan.io/2//reference/config_files/profiles.html.md#reference-config-files-profiles).

To list all the possible configurations available, run **conan config list**:

```text
$ conan config list
core.cache:storage_path: Absolute path where the packages and database are stored
core.download:download_cache: Define path to a file download cache
core.download:parallel: Number of concurrent threads to download packages
core.download:retry:  (int, default: 2) Number of retries in case of failure when downloading from Conan server
core.download:retry_wait: (int, default: 1s) Seconds to wait between download attempts from Conan server
core.graph:compatibility_mode: (Experimental) Set this to 'optimized' to enable the improved compatibility behaviour when querying multiple compatible binaries in remotes
core.gzip:compresslevel: The Gzip compression level for Conan artifacts (default=9)
core.net.http:cacert_path: Path containing a custom Cacert file
core.net.http:clean_system_proxy: If defined, the proxies system env-vars will be discarded
core.net.http:client_cert: Path or tuple of files containing a client cert (and key)
core.net.http:max_retries: Maximum number of connection retries (requests library)
core.net.http:no_proxy_match: List of urls to skip from proxies configuration
core.net.http:proxies: Dictionary containing the proxy configuration
core.net.http:timeout: Number of seconds without response to timeout (requests library)
core.package_id:config_mode: How the 'config_version' affects binaries. By default 'None'
core.package_id:default_build_mode: By default, 'None'
core.package_id:default_embed_mode: By default, 'full_mode'
core.package_id:default_non_embed_mode: By default, 'minor_mode'
core.package_id:default_python_mode: By default, 'minor_mode'
core.package_id:default_unknown_mode: By default, 'semver_mode'
core.scm:excluded: List of excluded patterns for builtin git dirty checks
core.scm:local_url: By default allows to store local folders as remote url, but not upload them. Use 'allow' for allowing upload and 'block' to completely forbid it
core.sources.patch:extra_path: Extra path to search for patch files for conan create
core.sources:download_cache: Folder to store the sources backup
core.sources:download_urls: List of URLs to download backup sources from
core.sources:exclude_urls: URLs which will not be backed up
core.sources:upload_url: Remote URL to upload backup sources to
core.upload:compression_format: The compression format used when uploading Conan packages. Possible values: 'zst', 'xz', 'gz' (default=gz)
core.upload:parallel: Number of concurrent threads to upload packages
core.upload:retry: (int, default: 1) Number of retries in case of failure when uploading to Conan server
core.upload:retry_wait: (int, default: 5s) Seconds to wait between upload attempts to Conan server
core.version_ranges:resolve_prereleases: Whether version ranges can resolve to pre-releases or not
core:allow_uppercase_pkg_names: Temporarily (will be removed in 2.X) allow uppercase names
core:compresslevel: The compression level for Conan artifacts (default zstd=3, gz=9)
core:default_build_profile: Defines the default build profile ('default' by default)
core:default_profile: Defines the default host profile ('default' by default)
core:non_interactive: Disable interactive user input, raises error if input necessary
core:policies: A list of opt-in behaviors that can be defined in the configuration to control specific aspects of Conan's behavior,
such as keeping deprecated behaviours:
   - deprecated_build_order_args: Allow deprecated skipping of --order-by argument in conan graph build-order - To be removed in Conan 2.32
   - deprecated_empty_version_range: Allow using deprecated empty version range expressions - To be removed in Conan 2.32
If the policy 'required_conan_version>=version' is defined, different behaviors can be enabled:
   - If required_conan_version>=2.28, bugfix https://github.com/conan-io/conan/pull/19705 for transitive static libraries package_id
   - If required_conan_version>=2.28, bugfix https://github.com/conan-io/conan/pull/19849 for VirtualBuildEnv bindir path propagation based on requirement run trait
   - If required_conan_version>=2.28, https://github.com/conan-io/conan/pull/19286 defaults the new 'consistent' trait to True for the host context, even when 'visible=False'
core:required_conan_version: Raise if current version does not match the defined range.
core:skip_warnings: Do not show warnings matching any of the patterns in this list. Current warning tags are 'network', 'deprecated', 'experimental'
core:update_policy: (Legacy). If equal 'legacy' when multiple remotes, update based on order of remotes, only the timestamp of the first occurrence of each revision counts.
core:warnings_as_errors: Treat warnings matching any of the patterns in this list as errors and then raise an exception. Current warning tags are 'network', 'deprecated'
tools.android:cmake_legacy_toolchain: Define to explicitly pass ANDROID_USE_LEGACY_TOOLCHAIN_FILE in CMake toolchain
tools.android:ndk_path: Argument for the CMAKE_ANDROID_NDK
tools.apple:enable_arc: (boolean) Enable/Disable ARC Apple Clang flags
tools.apple:enable_bitcode: (boolean) Enable/Disable Bitcode Apple Clang flags
tools.apple:enable_visibility: (boolean) Enable/Disable Visibility Apple Clang flags
tools.apple:sdk_path: Path to the SDK to be used
tools.build.cross_building:can_run: (boolean) Indicates whether is possible to run a non-native app on the same architecture. It's used by 'can_run' tool
tools.build.cross_building:cross_build: (boolean) Decides whether cross-building or not regardless of arch/OS settings. Used by 'cross_building' tool
tools.build:add_rpath_link: Add -Wl,-rpath-link flags pointing to all lib directories for host dependencies (CMake and Meson toolchains)
tools.build:cflags: List of extra C flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
tools.build:compiler_executables: Defines a Python dict-like with the compilers path to be used. Allowed keys {'c', 'cpp', 'cuda', 'objc', 'objcxx', 'rc', 'fortran', 'asm', 'hip', 'ispc'}
tools.build:cxxflags: List of extra CXX flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
tools.build:defines: List of extra definition flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
tools.build:download_source: Force download of sources for every package
tools.build:exelinkflags: List of extra flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
tools.build:install_strip: (boolean or list) True/False to strip on install for every CMake, Meson and Autotools integration, or a list of 'cmake', 'meson', 'autotools' to strip only for those.
tools.build:jobs: Default compile jobs number -jX Ninja, Make, /MP VS (default: max CPUs)
tools.build:linker_scripts: List of linker script files to pass to the linker used by different toolchains like CMakeToolchain, AutotoolsToolchain, and MesonToolchain
tools.build:rcflags: List of extra RC (resource compiler) flags used by different toolchains like CMakeToolchain, MSBuildToolchain and MesonToolchain
tools.build:sharedlinkflags: List of extra flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain
tools.build:skip_test: Do not execute CMake.test() and Meson.test() when enabled
tools.build:sysroot: Pass the --sysroot=<tools.build:sysroot> flag if available. (None by default)
tools.build:verbosity: Verbosity of build systems if set. Possible values are 'quiet' and 'verbose'
tools.cmake.cmake_layout:build_folder: (Experimental) Allow configuring the base folder of the build for local builds
tools.cmake.cmake_layout:build_folder_vars: Settings and Options that will produce a different build folder and different CMake presets names
tools.cmake.cmake_layout:test_folder: (Experimental) Allow configuring the base folder of the build for test_package
tools.cmake.cmakedeps:new: Use the new CMakeDeps generator
tools.cmake.cmaketoolchain:enabled_blocks: Select the specific blocks to use in the conan_toolchain.cmake
tools.cmake.cmaketoolchain:extra_variables: Dictionary with variables to be injected in CMakeToolchain (potential override of CMakeToolchain defined variables)
tools.cmake.cmaketoolchain:find_package_prefer_config: Argument for the CMAKE_FIND_PACKAGE_PREFER_CONFIG
tools.cmake.cmaketoolchain:generator: User defined CMake generator to use instead of default
tools.cmake.cmaketoolchain:presets_environment: String to define wether to add or not the environment section to the CMake presets. Empty by default, will generate the environment section in CMakePresets. Can take values: 'disabled'.
tools.cmake.cmaketoolchain:system_name: Define CMAKE_SYSTEM_NAME in CMakeToolchain
tools.cmake.cmaketoolchain:system_processor: Define CMAKE_SYSTEM_PROCESSOR in CMakeToolchain
tools.cmake.cmaketoolchain:system_version: Define CMAKE_SYSTEM_VERSION in CMakeToolchain
tools.cmake.cmaketoolchain:toolchain_file: Use other existing file rather than conan_toolchain.cmake one
tools.cmake.cmaketoolchain:toolset_arch: Toolset architecture to be used as part of CMAKE_GENERATOR_TOOLSET in CMakeToolchain
tools.cmake.cmaketoolchain:toolset_cuda: (Experimental) Path to a CUDA toolset to use, or version if installed at the system level
tools.cmake.cmaketoolchain:user_presets: (Experimental) Select a different name instead of CMakeUserPresets.json, empty to disable
tools.cmake.cmaketoolchain:user_toolchain: Inject existing user toolchains at the beginning of conan_toolchain.cmake
tools.cmake:cmake_program: Path to CMake executable
tools.cmake:configure_args: Add extra arguments to CMake.configure() command line
tools.cmake:ctest_args: Add extra arguments to CMake.ctest() runner command line
tools.cmake:install_strip: (Deprecated) Add --strip to cmake.install(). Use tools.build:install_strip instead
tools.compilation:verbosity: Verbosity of compilation tools if set. Possible values are 'quiet' and 'verbose'
tools.deployer:symlinks: Set to False to disable deployers copying symlinks
tools.env.virtualenv:powershell: If specified, it generates PowerShell launchers (.ps1). Use this configuration setting the PowerShell executable you want to use (e.g., 'powershell.exe' or 'pwsh')
tools.env:deactivation_mode: (Experimental) If 'function', generate a deactivate function instead of a script to unset the environment variables
tools.env:dotenv: (Experimental) Generate dotenv environment files
tools.files.download:retry: (int, default: 2) Number of retries in case of failure when downloading
tools.files.download:retry_wait: (int, default: 5s) Seconds to wait between download attempts
tools.files.download:verify: If set, overrides recipes on whether to perform SSL verification for their downloaded files. Only recommended to be set while testing
tools.files.unzip:filter: Define tar extraction filter: 'fully_trusted', 'tar', 'data'
tools.gnu:build_triplet: Custom build triplet to pass to Autotools scripts
tools.gnu:define_libcxx11_abi: Force definition of GLIBCXX_USE_CXX11_ABI=1 for libstdc++11
tools.gnu:disable_flags: Disable the automatic addition of flags to some build systems. List of possible values: ['arch', 'arch_link', 'libcxx', 'build_type', 'build_type_link', 'threads','cppstd', 'cstd']
tools.gnu:extra_configure_args: List of extra arguments to pass to configure when using AutotoolsToolchain and GnuToolchain
tools.gnu:host_triplet: Custom host triplet to pass to Autotools scripts
tools.gnu:make_program: Indicate path to make program
tools.gnu:pkg_config: Path to pkg-config executable used by PkgConfig build helper
tools.google.bazel:bazelrc_path: List of paths to bazelrc files to be used as 'bazel --bazelrc=rcpath1 ... build'
tools.google.bazel:configs: List of Bazel configurations to be used as 'bazel build --config=config1 ...'
tools.graph:skip_binaries: Allow the graph to skip binaries not needed in the current configuration (True by default)
tools.graph:skip_build: (Experimental) Do not expand build/tool_requires
tools.graph:skip_test: (Experimental) Do not expand test_requires. If building it might need 'tools.build:skip_test=True'
tools.graph:vendor: (Experimental) If 'build', enables the computation of dependencies of vendoring packages to build them
tools.info.package_id:confs: List of existing configuration to be part of the package ID
tools.intel:installation_path: Defines the Intel oneAPI installation root path
tools.intel:setvars_args: Custom arguments to be passed onto the setvars.sh|bat script from Intel oneAPI
tools.meson.mesontoolchain:backend: Any Meson backend: ninja, vs, vs2010, vs2012, vs2013, vs2015, vs2017, vs2019, xcode
tools.meson.mesontoolchain:extra_machine_files: List of paths for any additional native/cross file references to be appended to the existing Conan ones
tools.microsoft.bash:active: Set True only when Conan runs in a POSIX Bash (MSYS2/Cygwin) where Python's subprocess (shell=True) uses a POSIX-compatible shell (e.g., /bin/sh). Do not set when using Conan from cmd/PowerShell or with native Windows Python ('win32').
tools.microsoft.bash:path: The path to the shell to run when conanfile.win_bash==True
tools.microsoft.bash:subsystem: The subsystem to be used when conanfile.win_bash==True. Possible values: msys2, msys, cygwin, wsl, sfu
tools.microsoft.msbuild:installation_path: VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community. Use empty string to disable
tools.microsoft.msbuild:max_cpu_count: Argument for the /m when running msvc to build parallel projects
tools.microsoft.msbuild:vs_version: Defines the IDE version (15, 16, 17) when using the msvc compiler. Necessary if compiler.version specifies a toolset that is not the IDE default
tools.microsoft.msbuilddeps:exclude_code_analysis: Suppress MSBuild code analysis for patterns
tools.microsoft.msbuildtoolchain:compile_options: Dictionary with MSBuild compiler options
tools.microsoft:msvc_update: Force the specific update irrespective of compiler.update (CMakeToolchain and VCVars)
tools.microsoft:winsdk_version: Use this winsdk_version in vcvars
tools.system.package_manager:mode: Mode for package_manager tools: 'check', 'report', 'report-installed' or 'install'
tools.system.package_manager:sudo: Use 'sudo' when invoking the package manager tools in Linux (False by default)
tools.system.package_manager:sudo_askpass: Use the '-A' argument if using sudo in Linux to invoke the system package manager (False by default)
tools.system.package_manager:tool: Default package manager tool: 'apk', 'apt-get', 'yum', 'dnf', 'brew', 'pacman', 'choco', 'zypper', 'pkg' or 'pkgutil'
tools.system.pipenv:python_interpreter: (Deprecated) Use 'tools.system.pyenv:python_interpreter' instead. Path to the Python interpreter to be used to create the virtualenv
tools.system.pyenv:python_interpreter: (Experimental) Path to the Python interpreter to be used to create the virtualenv

```

## User/Tools configurations

Tools and user configurations can be defined in both the *global.conf* file and
[Conan profiles](https://docs.conan.io/2//reference/config_files/profiles.html.md#reference-config-files-profiles-conf). They look like:

```text
tools.build:verbosity=verbose
tools.microsoft.msbuild:max_cpu_count=2
tools.microsoft.msbuild:vs_version = 16
tools.build:jobs=10
# User conf variable
user.confvar:something=False
```

#### IMPORTANT
Profiles values will have priority over globally defined ones in global.conf.

These are some hints about configuration items scope and naming:

- `core.xxx` and `tools.yyy` are Conan built-ins, users cannot define their own ones in these scopes.
- `core.xxx` can be defined in `global.conf` or via the `--core-conf` CLI argument only, but not in profiles.
- `tools.yyy` can be defined in `global.conf`, in profiles `[conf]` section and as CLI `-c` arguments
- `user.zzz` can be defined everywhere, and they are totally at the user discretion, no established naming convention. However this would be more or less expected:
  : - For open source libraries, specially those in conancenter, `user.packagename:conf` might be expected, like the `boost` recipe defining `user.boost:conf` conf
    - For private usage, the recommendation could be to use something like `user.orgname:conf` for global org configuration across all projects, `user.orgname.project:conf` for project or package configuration, though `user.project:conf` might be also good if the project name is unique enough.
    - They \_must_ have one `:` separator, like `user.myorg:conf`, but not `user.myorg.conf` or `user.myorg`. This is to disambiguate from patterns, which are discussed below.

## Configuration file template

It is possible to use **jinja2** template engine for *global.conf*. When Conan loads this file, it immediately parses
and renders the template, which must result in a standard tools-configuration text.

> ```jinja
> # Using all the cores automatically
> tools.build:jobs={{os.cpu_count()}}
> # Using the current OS
> user.myconf.system:name = {{platform.system()}}
> ```

Conan also injects `detect_api` (non-stable, read the reference) to the jinja rendering context. You can use it like this:

> ```jinja
> user.myteam:myconf1={{detect_api.detect_os()}}
> user.myteam:myconf2={{detect_api.detect_arch()}}
> ```

For more information on how to use it, please check [the detect_api section](https://docs.conan.io/2//reference/config_files/profiles.html.md#reference-config-files-profiles-detect-api) in the profiles reference.

The Python packages passed to render the template are `os`, `platform` and `hashlib` for all platforms and `distro` in Linux platforms.
Additionally, the variables `conan_version` and `conan_home_folder` are also available.

The `os`, `platform` and `distro` can be useful to perform different system checks, while the `hashlib` library can be convenient
to compute unique hashes based on the `conan_home_folder` to define unique strings, for example for unique shorter paths in Windows in
CI systems when sometimes the path length can be an issue, for example:

```python
# compute a unique hash based on the current home folder
{% set h = hashlib.new("sha256", conan_home_folder.encode(),
                       usedforsecurity=False).hexdigest() %}
# and use the first 6 characters to compose a short path for package storage
core.cache:storage_path=C:/conan_{{h[:6]}}
```

## Configuration data types

All the values will be interpreted by Conan as the result of the python built-in eval() function:

```text
# String
tools.build:verbosity=verbose
# Boolean
tools.system.package_manager:sudo=True
# Integer
tools.microsoft.msbuild:max_cpu_count=2
# List of values
user.myconf.build:ldflags=["--flag1", "--flag2"]
# Dictionary
tools.microsoft.msbuildtoolchain:compile_options={"ExceptionHandling": "Async"}
```

<a id="configuration-data-operators"></a>

## Configuration data operators

It’s also possible to use some extra operators when you’re composing tool configurations in your *global.conf* or
any of your profiles:

* `+=` == `append`: appends values at the end of the existing value (only for lists).
* `=+` == `prepend`: puts values at the beginning of the existing value (only for lists).
* `*=` == `update`: updates the specified keys only, leaving the rest unmodified (only for dictionaries)
* `=!` == `unset`: gets rid of any configuration value.

```text
# Define the value => ["-f1"]
user.myconf.build:flags=["-f1"]

# Append the value ["-f2"] => ["-f1", "-f2"]
user.myconf.build:flags+=["-f2"]

# Prepend the value ["-f0"] => ["-f0", "-f1", "-f2"]
user.myconf.build:flags=+["-f0"]

# Unset the value
user.myconf.build:flags=!

# Define the value => {"a": 1, "b": 2}
user.myconf.build:other={"a": 1, "b": 2}

# Update b = 4 => {"a": 1, "b": 4}
user.myconf.build:other*={"b": 4}
```

<a id="reference-config-files-global-conf-patterns"></a>

## Configuration patterns

You can use package patterns to apply the configuration in those dependencies which are matching:

```text
*:tools.cmake.cmaketoolchain:generator=Ninja
zlib/*:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019
```

This example shows you how to specify a general `generator` for all your packages except for `zlib` which is defining
`Visual Studio 16 2019` as its generator.

Besides that, it’s quite relevant to say that **the order matters**. So, if we change the order of the
configuration lines above:

```text
zlib/*:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019
*:tools.cmake.cmaketoolchain:generator=Ninja
```

The result is that you’re specifying a general `generator` for all your packages, and that’s it. The `zlib` line has no
effect because it’s the first one evaluated, and after that, Conan is overriding that specific pattern with the most
general one, so it deserves to pay special attention to the order.

# Configuration precedence

There are different places where a configuration such as `tools.build:verbosity` can be defined:

- Globally, in the `global.conf` file
- In a `tool_requires` recipe that defines a `self.conf_info` in their `package_info()` method.
  (Recall that only **direct** `tool_requires` propagate `conf_info` to their consumers).
- In a profile file `[conf]` section
- In the command line `-c tools.build:verbosity=<value>`

In general, the rule is that the “closest to the user” has higher precedence.

That means that:

- The command line arguments like `-c tools.build:verbosity=<value>` will have higher precedence and overwrite
  possible values already defined in `tool_requires`, in `global.conf` or profiles `[conf]` section. The idea is that the user
  explicitly requested that typing it in the command line, so they want that value to prevail.
- Then, the profile `[conf]` section will have precedence over the `tool_requires` and `global.conf` definitions, as the profiles
  are also inputs by the user.
- Then, the `global.conf` will have precedence over `tool_requires` defined `conf_info`. The idea is that the user can define the
  behavior they want without having to modify or rewrite recipes.
- Finally, the one with less precedence is the `tool_requires` configuration defined in `package_info()` method with `self.conf_info`.

The core configurations such as `core:skip_warnings` can be defined in:

- Globally, in the `global.conf`, with less precedence
- In the command line, with `-cc/--core-conf core:skip_warnings=<value>` with higher precedence over the `global.conf`.

Note that `core` configurations cannot be defined in profiles or in recipes.

## Important configurations with `!` specifier

There are some scenarios when it is desired that a recipe defined configuration in `package_info()` via the `conf_info`
has higher precedence over a value defined downstream by the user in profiles or command line.

The “important configuration” definition allows this, specifying with the `!` qualifier over the configuration name that
such value should have relatively higher priority.
Imagine we are writing a `tool_requires` for the Msys2 subsystem, and we would like that recipe to define the `tools.microsoft.bash:path`
value so it points to itself.
But for some reason we also have `tools.microsoft.bash:path` in our profiles, pointing to a Msys2 that still some
packages that do not use the new `msys2/1.0` still need. We could define a recipe like:

```python
from conan import ConanFile

class Pkg(ConanFile):
    name = "msys2"
    version = "1.0"

    def package_info(self):
      bash = os.path.join(self.package_folder, "bash.exe")
      # Note the ! after the name of the configuration
      # That makes this definition "important", and have higher
      # precedence than in profiles
      self.conf_info.define("tools.microsoft.bash:path!", bash)
      # You can apply the same ! specifier in other "conf_info"
      # operations, for paths, append/prepend, etc
```

with some consumers that requires it:

```python
from conan import ConanFile

class Pkg(ConanFile):
    name = "mylib"
    version = "1.0"

    def build_requirements(self):
      if self.settings_build.os == "Windows":
        self.tool_requires("msys2/1.0")
```

And then have a profile like

```ini
[conf]
tools.microsoft.bash:path=<point/to/system/msys2/installation>
```

Then, the `mylib/1.0` will get the `tools.microsoft.bash:path` pointing to the `msys2` path,
while other recipes that do not `tool_requires` the `msys2` will still get the system one.

If for some reason a profile or command line would still want to force an override also the
important configurations from packages upstream, they can do it using the same syntax:

```ini
[conf]
# This will force all packages to use the system msys2, even if they
# are tool-requiring the ``msys2/1.0`` package
# Note the ! after the configuration name
tools.microsoft.bash:path!=<point/to/system/msys2/installation>
```

#### IMPORTANT
**Best practices**

The usage of important `!` configuration should be exceptional, and reduced to limited cases when
there are no other alternatives. Modifying the default precedence, in which users expects their inputs
from command line or profiles to be always applied can be confusing for them. Please use this feature
sparingly and being aware of these implications.

# Information about built-in confs

This section provides extra information about specific confs.

## Policies

The `core:policies` conf allows to define policies that will be applied globally to modify the
behaviour of Conan in certain aspects. Check [the policies section](https://docs.conan.io/2//reference/policies.html.md#reference-policies)
for more information.

## Networking confs

<a id="reference-config-files-global-conf-ssl-certificates"></a>

### Configuration of client certificates

Conan supports client TLS certificates. You can configure the path to your existing *Cacert* file and/or your client
certificate (and the key) using the following configuration variables:

* `core.net.http:cacert_path`: Path containing a custom Cacert file.
  When multiple certificates are necessary for different remotes, it is possible to aggregate them, for example adding
  your own `my-ca.crt` certificate:
  ```text
  sudo cp my-ca.crt /usr/local/share/ca-certificates/my-ca.crt
  sudo update-ca-certificates
  ```

  Then, the certificate storage can be defined with `core.net.http:cacert_path=/etc/ssl/certs/ca-certificates.crt`.
  The `cacert_path` Conan configuration is forwarded to the `python-requests` `verify` argument, see
  [Python-requests SSL certificates](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification).
  That means that if the `REQUESTS_CA_BUNDLE` environment variable is defined, it might be taken into account too.
* `core.net.http:client_cert`: Path or tuple of files containing a client certificate (and the key). See more details in
  [Python requests and Client Side Certificates](https://requests.readthedocs.io/en/latest/user/advanced/#client-side-certificates)

  For instance:
  ```text
  core.net.http:client_cert=('/path/client.cert', '/path/client.key')
  ```
* `tools.files.download:verify`: Setting `tools.files.download:verify=False` constitutes a security risk if enabled,
  as it disables certificate validation. Do not use it unless you understand the implications
  (And even then, properly scoping the conf to only the required recipes is a good idea)
  or if you are using it for development purposes

#### SEE ALSO
If you need to use both a corporate remote (with a private CA) and a public remote like
ConanCenter, see [Using Conan with both corporate and public remotes (SSL certificates)](https://docs.conan.io/2//knowledge/faq.html.md#faq-ssl-corporate-certificates) for step-by-step instructions on
creating a combined CA bundle.

### Proxies

There are 3 `confs` that can define proxies information:

```bash
$ conan config list proxies
core.net.http:clean_system_proxy: If defined, the proxies system env-vars will be discarded
core.net.http:no_proxy_match: List of urls to skip from proxies configuration
core.net.http:proxies: Dictionary containing the proxy configuration
```

The `core.net.http:proxies` dictionary is passed to the underlying `python-requests` library, to the “proxies” argument
as described in the [python-requests documentation](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)

The `core.net:no_proxy_match` is a list of URL patterns, like:

```ini
core.net.http:no_proxy_match = ["http://someurl.com/*"]
```

for URLs to be excluded from the `proxies` configuration. That means that all URLs that are referenced that matches any
of those patterns will not receive the `proxies` definition. Note the `*` in the pattern is necessary for the match.

If `core.net.http:clean_system_proxy` is `True`, then the environment variables `"http_proxy", "https_proxy", "ftp_proxy", "all_proxy", "no_proxy"`,
will be temporary removed from the environment, so they are not taken into account when resolving proxies.

## Storage configurations

### core.cache:storage_path

Absolute path to a folder where the Conan packages and the database of the packages will be stored.
This folder will be the heaviest Conan storage folder, as it stores the binary packages downloaded or created.

```text
core.cache:storage_path = C:\Users\danielm\my_conan_storage_folder
```

**Default value:** `<CONAN_HOME>/p`

### core.download:download_cache

Absolute path to a folder where the Conan packages will be stored *compressed*.
This is useful to avoid recurrent downloads of the same packages, especially in CI.

```text
core.download:download_cache = C:\Users\danielm\my_download_cache
```

**Default value:** Not defined.

## UX confs

<a id="reference-config-files-global-conf-skip-warnings"></a>

### Skip warnings

There are several warnings that Conan outputs in certain cases which can be omitted via the `core:skip_warnings` conf,
by adding the warning tag to its value.

Those warnings are:

> - `deprecated`: Messages for deprecated features such as legacy generators
> - `network`: Messages related to network issues, such as retries

### Parallel download

By default the download and unzip of pre-compiled package binaries from remote servers will happen in parallel,
defaulting to the number of cpu-cores. The configuration `core.download:parallel=<int-number>` can change this
behavior. If `core.download:parallel=0`, then the behavior will be to not use parallelism and do a sequential
download and unzip of precompiled package binaries.
This `core.download:parallel` configuration also affects the `conan download` command, but for that command
the default at the moment is not to use parallelism, but sequential download.

### Environment deactivation functions

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

When setting the configuration `tools.env:deactivation_mode` to `function` in your profile or in
`global.conf`, the deactivation scripts will no longer be generated.

Instead, an *in-memory* deactivation function will be available in the
current shell session as soon as you activate the conan environment.

Moving from the classical Conan workflow:

Bash

PowerShell

Batchfile

```bash
$ source conanbuild.sh
$ ...
$ source deactivate_conanbuild.sh
```

```powershell
$ .\conanbuild.ps1
$ ...
$ .\deactivate_conanbuild.ps1
```

```batch
$ .\conanbuild.bat
$ ...
$ .\deactivate_conanbuild.bat
```

To the new workflow,

Bash

PowerShell

Batchfile

```bash
$ source conanbuild.sh
$ ...
$ deactivate_conanbuild # from anywhere in the shell
```

```powershell
$ .\conanbuild.ps1
$ ...
$ deactivate_conanbuild # from anywhere in the shell
```

```batch
$ .\conanbuild.bat
$ ...
$ deactivate_conanbuild # from anywhere in the shell
```

By executing this function, the environment will be restored and the function will no longer be
available in the current shell session. This behavior emulates the well known `virtualenv` Python tool.

```text
tools.env:deactivation_mode=function
```

**Default value:** None.
