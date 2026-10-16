<a id="conan-tools-meson-meson"></a>

# Meson

The `Meson()` build helper is intended to be used in the `build()` and `package()` methods, to call Meson commands automatically.

```python
from conan import ConanFile
from conan.tools.meson import Meson

class PkgConan(ConanFile):

    def build(self):
        meson = Meson(self)
        meson.configure()
        meson.build()

    def package(self):
        meson = Meson(self)
        meson.install()
```

## Reference

### *class* Meson(conanfile)

This class calls Meson commands when a package is being built. Notice that
this one should be used together with the `MesonToolchain` generator.

* **Parameters:**
  **conanfile** – `< ConanFile object >` The current recipe object. Always use `self`.

#### configure(reconfigure=False)

Runs `meson setup [FILE] "BUILD_FOLDER" "SOURCE_FOLDER" [-Dprefix=/]`
command, where `FILE` could be `--native-file conan_meson_native.ini`
(if native builds) or `--cross-file conan_meson_cross.ini` (if cross builds).

* **Parameters:**
  **reconfigure** – `bool` value that adds `--reconfigure` param to the final command.

#### build(target=None)

Runs `meson compile -C . -j[N_JOBS] [TARGET]` in the build folder.
You can specify `N_JOBS` through the configuration line `tools.build:jobs=N_JOBS`
in your profile `[conf]` section.

* **Parameters:**
  **target** – `str` Specifies the target to be executed.

#### install(cli_args=None)

Runs `meson install -C "." --destdir ..` in the build folder.

* **Parameters:**
  **cli_args** – List of arguments to be added to the command:
  `meson install -C "." --destdir ... arg1 arg2`

#### test()

Runs `meson test -v -C "."` in the build folder.

## conf

The `Meson` build helper is affected by these `[conf]` variables:

- `tools.meson.mesontoolchain:extra_machine_files=[<FILENAME>]` configuration to add
  your machine files at the end of the command using the correct parameter depending on
  native or cross builds. See [this Meson reference](https://mesonbuild.com/Machine-files.html#loading-multiple-machine-files) for more
  information.
- `tools.compilation:verbosity` which accepts one of `quiet` or `verbose` and sets the `--verbose` flag in `Meson.build()`
- `tools.build:verbosity` which accepts one of `quiet` or `verbose` and sets the `--quiet` flag in `Meson.install()`
- `tools.build:install_strip` (Since Conan 2.18.0) will pass `--strip` to the `meson install` call if set to `True`.
