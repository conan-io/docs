<a id="conan-tools-apple-xcodebuild"></a>

# XcodeBuild

The `XcodeBuild` build helper is a wrapper around the command line invocation of Xcode. It
will abstract the calls like `xcodebuild -project app.xcodeproj -configuration <config>
-arch <arch> ...`

The `XcodeBuild` helper can be used like:

```python
from conan import conanfile
from conan.tools.apple import XcodeBuild

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def build(self):
        xcodebuild = XcodeBuild(self)
        xcodebuild.build("app.xcodeproj")
```

## Reference

### *class* XcodeBuild(conanfile)

#### \_\_init_\_(conanfile)

#### XcodeBuild.build(xcodeproj, target=None, configuration=None, cli_args=None)

Call to `xcodebuild` to build a Xcode project.

* **Parameters:**
  * **xcodeproj** – the *xcodeproj* file to build.
  * **target** – the target to build, in case this argument is passed to the `build()`
    method it will add the `-target` argument to the build system call. If not passed, it
    will build all the targets passing the `-alltargets` argument instead.
  * **configuration** – Build configuration to use (e.g., `Debug`, `Release`).
    Defaults to the recipe’s `settings.build_type`.
  * **cli_args** – Extra options to pass directly to `xcodebuild` (list of strings).
    Examples: `["-xcconfig", "<path/to/file.xcconfig>"]` or custom
    Xcode build settings like `["BUILD_LIBRARY_FOR_DISTRIBUTION=YES"]`.
* **Returns:**
  the return code for the launched `xcodebuild` command.

The `XcodeBuild.build()` method internally implements a call to `xcodebuild` like:

```bash
$ xcodebuild -project app.xcodeproj -configuration <configuration> -arch <architecture> <sdk> <verbosity> -target <target>/-alltargets *_DEPLOYMENT_TARGET=settings.os.version <cli_args>
```

Where:

- `configuration` is the configuration, typically *Release* or *Debug*, which will be obtained
  from `settings.build_type` unless you pass it explicitly via the `configuration` parameter.
- `architecture` is the build architecture, a mapping from the `settings.arch` to the
  common architectures defined by Apple ‘i386’, ‘x86_64’, ‘armv7’, ‘arm64’, etc.
- `sdk` is set based on the values of the `os.sdk` and `os.sdk_version` defining the
  `SDKROOT` Xcode build setting according to them. For example, setting `os.sdk=iOS`
  and os.sdk_version=8.3\` will pass `SDKROOT=iOS8.3` to the build system. In case you
  defined the `tools.apple:sdk_path` in your **[conf]** this value will
  take preference and will directly pass `SDKROOT=<tools.apple:sdk_path>` so **take into
  account** that for this case the skd located in that path should set your `os.sdk` and
  `os.sdk_version` settings values.
- `verbosity` is the verbosity level for the build and can take value ‘verbose’ or
  ‘quiet’ if set by `tools.build:verbosity` in your **[conf]**
- `cli_args` are the additional command line arguments passed via the
  `cli_args` parameter. These can include custom build settings like
  `BUILD_LIBRARY_FOR_DISTRIBUTION=YES`. You can also redirect build artifacts
  to the Conan build folder by passing `SYMROOT` and `OBJROOT` settings:
  ```python
  def build(self):
    xcodebuild = XcodeBuild(self)
    xcodebuild.build("app.xcodeproj", cli_args=[f"SYMROOT={self.build_folder}",
                                                f"OBJROOT={self.build_folder}"])
  ```

Additional parameters that are passed to `xcodebuild` (but before `cli_args`):

- Deployment target setting according to the values of `os` and `os.version` from profile,
  e.g. `MACOSX_DEPLOYMENT_TARGET=10.15` or `IPHONEOS_DEPLOYMENT_TARGET=15.0`

## conf

- `tools.build:verbosity` (or `tools.compilation:verbosity` as fallback) which accepts `quiet` or `verbose`,
  and sets the `-verbose` or `-quiet` flags in `XcodeBuild.install()`
- `tools.apple:sdk_path` path for the sdk location, will set the `SDKROOT` value with
  preference over composing the value from the `os.sdk` and `os.sdk_version` settings.
