# conan config

Manage the Conan configuration in the Conan home.

## conan config home

```text
$ conan config home -h
usage: conan config home [-h] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF]

Show the Conan home folder.

options:
  -h, --help            show this help message and exit
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True

```

The `conan config home` command returns the path of the Conan home folder.

```text
$ conan config home

/home/user/.conan2
```

<a id="reference-commands-conan-config-install"></a>

## conan config install

```text
$ conan config install -h
usage: conan config install [-h] [--out-file OUT_FILE]
                            [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                            [-cc CORE_CONF] [--verify-ssl [VERIFY_SSL] |
                            --insecure] [-t {git,dir,file,url}] [-a ARGS]
                            [-sf SOURCE_FOLDER] [-tf TARGET_FOLDER]
                            item

Install the configuration (remotes, profiles, conf), from git, http or a
folder, into the Conan home folder.

positional arguments:
  item                  git repository, local file or folder or zip file
                        (local or http) where the configuration is stored

options:
  -h, --help            show this help message and exit
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True
  --verify-ssl [VERIFY_SSL]
                        Verify SSL connection when downloading file
  --insecure            Allow insecure server connections when using SSL.
                        Equivalent to --verify-ssl=False
  -t {git,dir,file,url}, --type {git,dir,file,url}
                        Type of remote config
  -a ARGS, --args ARGS  String with extra arguments for "git clone"
  -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                        Install files only from a source subfolder from the
                        specified origin
  -tf TARGET_FOLDER, --target-folder TARGET_FOLDER
                        Install to that path in the conan cache

```

The `conan config install` command is intended to install in the current home a common shared Conan
configuration, like the definitions of `remotes`, `profiles`, `settings`, `hooks`, `extensions`, etc.

The command can use as source any of the following:

- A URL pointing to a zip archive containing the configuration files
- A git repository containing the files
- A local folder
- Just one file

Files in the current Conan home will be replaced by the ones from the installation source.
All the configuration files can be shared and installed this way:

- `remotes.json` for the definition of remotes
- Any custom profile files inside a `profiles` subfolder
- Custom `settings.yml`
- Custom `global.conf`
- All the extensions, including plugins, hooks.
- Custom user commands.

This command reads a `.conanignore` file which, if present, filters which files and folders
are copied over to the user’s Conan home folder.
This file uses [fnmatch](https://docs.python.org/3/library/fnmatch.html) patterns
to match over the folder contents, excluding those entries that match from the config installation.
See [conan-io/command-extensions’s .conanignore](https://github.com/conan-io/command-extensions/blob/main/.conanignore) for an example of such a file.
You can force certain files to be copied over by using the `!` negation syntax:

```text
# Ignore all files
*
# But copy the file named "settings.yml"
!settings.yml
```

**Examples**:

- Install the configuration from a URL:
  ```text
  $ conan config install http://url/to/some/config.zip
  ```
- Install the configuration from a URL, but only getting the files inside a *origin* folder
  inside the zip file, and putting them inside a *target* folder in the local cache:
  ```text
  $ conan config install http://url/to/some/config.zip -sf=origin -tf=target
  ```
- Install configuration from 2 different zip files from 2 different urls, using different source
  and target folders for each one, then update all:
  ```text
  $ conan config install http://url/to/some/config.zip -sf=origin -tf=target
  $ conan config install http://url/to/some/config.zip -sf=origin2 -tf=target2
  $ conan config install http://other/url/to/other.zip -sf=hooks -tf=hooks
  ```
- Install the configuration from a Git repository with submodules:
  ```text
  $ conan config install http://github.com/user/conan_config/.git --args="--recursive"
  ```

  You can also force the git download by using **--type git** (in case it is not deduced from the URL automatically):
  ```text
  $ conan config install http://github.com/user/conan_config/.git --type git
  ```
- Install the configuration from a specific Git branch:
  ```text
  $ conan config install http://github.com/user/conan_config/.git --args="--branch mybranch"
  ```
- Install from a URL skipping SSL verification:
  ```text
  $ conan config install http://url/to/some/config.zip --verify-ssl=False
  ```

  This will disable the SSL check of the certificate.
- Install a specific file from a local path:
  ```text
  $ conan config install my_settings/settings.yml
  ```
- Install the configuration from a local path:
  ```text
  $ conan config install /path/to/some/config.zip
  ```

<a id="reference-commands-conan-config-install-pkg"></a>

## conan config install-pkg

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

```text
$ conan config install-pkg -h
usage: conan config install-pkg [-h] [--out-file OUT_FILE]
                                [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                                [-cc CORE_CONF] [-l LOCKFILE]
                                [--lockfile-partial]
                                [--lockfile-out LOCKFILE_OUT] [-f]
                                [--insecure] [--url URL] [-pr PROFILE]
                                [-s SETTINGS] [-o OPTIONS]
                                [reference]

(Experimental) Install the configuration (remotes, profiles, conf), from a
Conan package or from a conanconfig.yml file

positional arguments:
  reference             Package reference 'pkg/version' to install
                        configuration from or path to 'conanconfig.yml' file

options:
  -h, --help            show this help message and exit
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True
  -l LOCKFILE, --lockfile LOCKFILE
                        Path to a lockfile. Use --lockfile="" to avoid
                        automatic use of existing 'conan.lock' file
  --lockfile-partial    Do not raise an error if some dependency is not found
                        in lockfile
  --lockfile-out LOCKFILE_OUT
                        Filename of the updated lockfile
  -f, --force           Force the re-installation of configuration
  --insecure            Allow insecure server connections when using SSL
  --url URL             (Experimental) Provide Conan repository URL (for first
                        install without remotes)
  -pr PROFILE, --profile PROFILE
                        Profile to install config
  -s SETTINGS, --settings SETTINGS
                        Settings to install config
  -o OPTIONS, --options OPTIONS
                        Options to install config

```

This command allows to install configuration from a Conan package stored in a Conan server.

The packages containing configuration follow some special rules:

- They must define the `package_type = "configuration"`
- The configuration files must be packaged in the final “binary” package, following the same layout as they would for other `conan config install` cases.
- They cannot be used as `requires` of other packages, because that would result in a chicken-and-egg problem.
- They cannot contain `requires` to other packages
- The configuration packages are created with `conan create` and `conan export-pkg` as other packages, and uploaded to the servers with `conan upload`

To install a configuration from a Conan configuration package, it is possible:

- To generate a lockfile file with `--lockfile-out`. This lockfile file can be passed to `conan config install-pkg --lockfile` (it will automatically loaded it if is named `conan.lock` and found in the current directory) in the future to guarantee the same exact version.
- Version ranges can be used `conan config install-pkg "myconf/[>=1.0 <2]"` is correct, and it will install the latest one in that range.
- `conan config install-pkg` always look in the server for the latest version or revision.
- If the same version and revision was downloaded and installed from the server, `conan config install-pkg` will be a no-op unless `--force` is used, in this case the configuration will be overwritten.

It is also possible to make the version of the configuration affect all packages `package_id` and be part of the binary model, by activating the `core.package_id:config_mode` conf (this is also experimental), to any available mode, like `minor_mode`. Note that the order of the installation of packages in case multiple configuration packages are installed is important. This is why Conan will raise an error if the relative order of installed configuration packages changes as the result of installing updates for those configuration packages.

As the `conan config install-pkg` command downloads the package from a Conan remote server, it can download from an already existing remote,
or it can download from a Conan remote directly specifying the repository URL:

```bash
$ conan config install-pkg myconf/version --url=<url/conan/remote/repo>
```

In the same way that `conan remote add` can define `--insecure` to disable the SSL verification for that remote, it is possible to disable it for `conan config install-pkg` with:

```bash
$ conan config install-pkg myconf/version --url=<url/conan/remote/repo> --insecure
```

When specifying the `--url` argument, a Conan remote named `config_install_url` is created on the fly.
That means that if authentication is desired via env-vars, the env-var names will be `CONAN_LOGIN_USERNAME_CONFIG_INSTALL_URL`
or `CONAN_PASSWORD_CONFIG_INSTALL_URL`.

Conan configuration packages can also be parameterized depending on profiles, settings and options.
For example, if some organization would like to manage their configuration slightly differently for Windows and other platforms they could do:

```python
import os
from conan import ConanFile
from conan.tools.files import copy

class Conf(ConanFile):
    name = "myconf"
    version = "0.1"
    settings = "os"
    package_type = "configuration"
    def package(self):
        f = "win" if self.settings.os == "Windows" else "nix"
        copy(self, "*.conf", src=os.path.join(self.build_folder, f), dst=self.package_folder)
```

And if they had a layout with different `global.conf` for the different platforms, like:

```text
conanfile.py
win/global.conf
nix/global.conf
```

They could create and upload their configuration package as:

```bash
$ conan export-pkg . -s os=Windows
$ conan export-pkg . -s os=Linux
$ conan upload "*" -r=remote -c
```

Then, developers could do:

```bash
$ conan config install-pkg "myconf/[*]" -s os=Linux
# or even implicitly, if they default build profile defines os=Linux
$ conan config install-pkg "myconf/[*]"
```

And they will get the correct configuration for their platform.

#### SEE ALSO
- If you lock installed configuration packages in a lockfile, you could use the
  [conan lock upgrade-config](https://docs.conan.io/2//reference/commands/lock/upgrade_config.html.md#reference-commands-lock-upgrade-config) command
  to update such a lockfile.

### conanconfig.yml

The `conan config install-pkg` admits also as an input a yaml `conanconfig.yml` file that can contain more than one package requirement, something like:

```yaml
packages:
    - myconf_a/0.1
    - myconf_b/0.1
    - myconf_c/[>=1 <2]
```

and be used like `conan config install-pkg .` or even just `conan config install-pkg`.

The file also admits the definition of `urls` with the same meaning as the `--url` command line argument, to simplify the initial installation
of configuration when doing a Conan setup:

```yaml
packages:
    - myconf_a/0.1
    - myconf_b/0.1
    - myconf_c/[>=1 <2]
urls:
    - https://my/conan/remote/repo/url
```

Like in the `remotes.json` file, the `urls` in the `conanconfig.yml` file can also add the `verify_ssl` specifier to disable SSL verification,
with the same behavior as the command line argument `--insecure`:

```yaml
packages:
    - myconf/0.1
urls:
    - url: https://some.server.com
      verify_ssl: false
```

#### IMPORTANT
When installing more than 1 configuration package, the order of installation is important, as the later installed packages can overwrite
configuration files installed by the previous ones. Consequently, if you decide to make the configuration part of the packages `package_id`
via `core.package_id:config_mode` conf, the order is taken into account.

Then any installation or re-installation of packages or updates that change this order will be raised as an error. For example if
after installing the configuration from the `conanconfig.yml` above we try to do a `conan config install-pkg myconf_a/0.2`, that
will be raised as an error, because that would make `myconf_a` to be the latest installed one, not the first.

But on the other hand, doing an update with the previous file will not be an error, because it will re-install the `myconf_a`, `myconf_b`
and `myconf_c` in order. Likewise, doing an update only for `myconf_c` wouldn’t be an error, because it is the last one and
preserves the relative order.

### Configuration packages in lockfiles

When a configuration package is stored in a lockfile, with the `--lockfile-out` argument, it will create an entry in the lockfile `config_requires` entry.
This entry has different purposes:

- When installing configuration packages with `conan config install-pkg` using command line arguments or a `conanconfig.yml` file that contains version ranges, or even pinned versions, but no recipe-revision, the provided lockfile can constraint that input to force and guarantee the exact version and recipe revision for that package defined in the lockfile.
- When using a lockfile as input in regular `conan install/build/create/graph-info`, etc, it will perform a check of the installed configuration packages, and if they are not aligned with the lockfile defined `config_requires` it will raise an error. Users then can issue a `conan config install-pkg` command to install the required configuration packages so their environments align. The idea is that lockfiles `config_requires` are there to guarantee the same configuration. The check goes in both directions, configuration packages already installed in the current user cache must satisfy the lockfile constraints, and lockfile declared `config_requires` must be installed. If for any reason, this behaviour wouldn’t be desired, it is possible to use a different lockfile just for the configurations, independent from the regular packages lockfiles, avoiding in this way a populated `config_requires` when using regular packages installation commands.

## conan config list

```text
$ conan config list -h
usage: conan config list [-h] [-f FORMAT] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF]
                         [pattern]

Show all the Conan available configurations: core and tools.

positional arguments:
  pattern               Filter configuration items that matches this pattern

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Select the output format: json
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True

```

Displays all the Conan built-in configurations. There are 2 groups:

- `core.xxxx`: These can only be defined in `global.conf` and are used by Conan internally
- `tools.xxxx`: These can be defined both in `global.conf` and profiles, and will be used by
  recipes and tools used within recipes, like `CMakeToolchain`

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

It is possible to list only the configurations that match a given pattern, like:

```bash
$  conan config list proxy
core.net.http:clean_system_proxy: If defined, the proxies system env-vars will be discarded
core.net.http:no_proxy_match: List of urls to skip from proxies configuration
core.net.http:proxies: Dictionary containing the proxy configuration
```

#### SEE ALSO
- These configurations can be defined in `global.conf`, profile files and command line, see
  [Conan configuration files](https://docs.conan.io/2//reference/config_files.html.md#reference-config-files)

## conan config show

```text
$ conan config show -h
usage: conan config show [-h] [-f FORMAT] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF]
                         pattern

Get the value of the specified conf

positional arguments:
  pattern               Conf item(s) pattern for which to query their value

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Select the output format: json
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True

```

Shows the values of the conf items that match the given pattern.

For a *global.conf* consisting of

```text
tools.build:jobs=42
tools.files.download:retry_wait=10
tools.files.download:retry=7
core.net.http:timeout=30
core.net.http:max_retries=5
zlib*/:tools.files.download:retry_wait=100
zlib*/:tools.files.download:retry=5
```

You can get all the values:

```text
$ conan config show "*"

core.net.http:max_retries: 5
core.net.http:timeout: 30
tools.files.download:retry: 7
tools.files.download:retry_wait: 10
tools.build:jobs: 42
zlib*/:tools.files.download:retry: 5
zlib*/:tools.files.download:retry_wait: 100
```

Or just those referring to the `tools.files` section:

```text
$ conan config show "*tools.files*"

tools.files.download:retry: 7
tools.files.download:retry_wait: 10
zlib*/:tools.files.download:retry: 5
zlib*/:tools.files.download:retry_wait: 100
```

Notice the first `*` in the pattern. This will match all the package patterns.
Removing it will make the command only show global confs:

```text
$ conan config show "tools.files*"

tools.files.download:retry: 7
tools.files.download:retry_wait: 10
```

## conan config clean

```text
$ conan config clean -h
usage: conan config clean [-h] [--out-file OUT_FILE]
                          [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                          [-cc CORE_CONF]

(Experimental) Clean the configuration files in the Conan home folder, while
keeping installed packages

options:
  -h, --help            show this help message and exit
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True

```

Removes all the custom configuration from the Conan home, such as `remotes.json`, profiles, settings, plugins, extensions, etc.
This does not remove packages, only the configuration files.
