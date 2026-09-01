<a id="reference-tools-intel"></a>

# conan.tools.intel

## IntelCC

This tool helps you to manage the new Intel oneAPI [DPC++/C++](https://software.intel.com/content/www/us/en/develop/documentation/oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top.html) and
[Classic](https://software.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top.html) ecosystem in Conan.

#### WARNING
This generator is **experimental** and subject to breaking changes.

#### WARNING
macOS is not supported for the Intel oneAPI DPC++/C++ (icx/icpx or dpcpp) compilers. For macOS or Xcode support, you’ll have to use the Intel C++ Classic Compiler.

#### NOTE
Remember, you need to have installed previously the [Intel oneAPI software](https://www.intel.com/content/www/us/en/developer/tools/oneapi/toolkits.html).

This generator creates a `conanintelsetvars.sh|bat` wrapping the Intel script `setvars.sh|bat` that sets the Intel oneAPI
environment variables needed. That script is the first step to start using the Intel compilers because it’s setting some
important variables in your local environment.

#### NOTE
If you explicitly set `tools.intel:installation_path=""` configuration
(empty string), Conan will **not generate** the `conanintelsetvars`
script. In this case, you are expected to have already activated the Intel
oneAPI environment manually.

In summary, the `IntelCC` generator:

1. Reads your profile `[settings]` and `[conf]`.
2. Uses that information to generate a `conanintelsetvars.sh|bat` script with the command to load the Intel `setvars.sh|bat` script.
3. Then, you or the chosen generator will be able to run that script and use any Intel compiler to compile the project.

#### NOTE
You can launch the `conanintelsetvars.sh|bat` before calling your intel compiler to build a project.
Conan will also call it in the conanfile `build(self)` method when running any command with `self.run`.

At first, ensure you are using a *profile* like this one:

```text
[settings]
...
compiler=intel-cc
compiler.mode=dpcpp
compiler.version=2021.3
compiler.libcxx=libstdc++
build_type=Release

[buildenv]
CC=dpcpp
CXX=dpcpp

[conf]
tools.intel:installation_path=/opt/intel/oneapi
```

The `IntelCC` generator can be used by name in conanfiles:

```python
class Pkg(ConanFile):
    generators = "IntelCC"
```

```text
[generators]
IntelCC
```

And it can also be fully instantiated in the conanfile `generate()` method:

```python
from conan import ConanFile
from conan.tools.intel import IntelCC

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def generate(self):
        intelcc = IntelCC(self)
        intelcc.generate()
```

Now, running the command **conan install . -pr intelprofile** generates the `conanintelsetvars.sh|bat` script
which runs the Intel *setvars* script and loads all the variables into your local environment.

### Custom configurations

Apply different installation paths and command arguments simply by changing the `[conf]` entries. For instance:

```text
[settings]
...
compiler=intel-cc
compiler.mode=dpcpp
compiler.version=2021.3
compiler.libcxx=libstdc++
build_type=Release

[buildenv]
CC=dpcpp
CXX=dpcpp

[conf]
tools.intel:installation_path=/opt/intel/oneapi
tools.intel:setvars_args=--config="full/path/to/your/config.txt" --force
```

Run again a **conan install . -pr intelprofile**, then the `conanintelsetvars.sh` script (if we are using Linux OS)
will contain something like:

```bash
. "/opt/intel/oneapi/setvars.sh" --config="full/path/to/your/config.txt" --force
```

## Reference

### *class* IntelCC(conanfile)

Class that manages Intel oneAPI DPC++/C++/Classic Compilers vars generation

#### arch

arch setting

#### *property* ms_toolset

Get Microsoft Visual Studio Toolset depending on the mode selected

#### generate(scope='build')

Generate the Conan Intel file to be loaded in build environment by default

#### *property* installation_path

Get the Intel oneAPI installation root path

#### *property* command

The Intel oneAPI DPC++/C++ Compiler includes environment configuration scripts to
configure your build and development environment variables:

- On Linux, the file is a shell script called setvars.sh.
- On Windows, the file is a batch file called setvars.bat.
- Linux -> `>> . /<install-dir>/setvars.sh <arg1> <arg2> … <argn><arg1> <arg2> … <argn>`
  The compiler environment script file accepts an optional target architecture
  argument <arg>:
  - intel64: Generate code and use libraries for Intel 64 architecture-based targets.
  - ia32: Generate code and use libraries for IA-32 architecture-based targets.
- Windows -> `>> call <install-dir>\setvars.bat [<arg1>] [<arg2>]`
  Where <arg1> is optional and can be one of the following:
  - intel64: Generate code and use libraries for Intel 64 architecture (host and target).
  - ia32: Generate code and use libraries for IA-32 architecture (host and target).

  With the dpcpp compiler, <arg1> is intel64 by default.

  The <arg2> is optional. If specified, it is one of the following:
  - vs2019: Microsoft Visual Studio\* 2019
  - vs2017: Microsoft Visual Studio 2017

* **Returns:**
  str setvars.sh|bat command to be run

### conf

`IntelCC` uses these [configuration entries](https://docs.conan.io/2//reference/config_files/global_conf.html.md#reference-config-files-global-conf):

- `tools.intel:installation_path`: **(required)** argument to tell Conan the
  installation path, if it’s not defined, Conan will try to find it out
  automatically. If it is explicitly set to the empty string (`""`), Conan
  will **skip the generation** of the `conanintelsetvars` script, assuming the
  Intel environment has already been activated manually.
- `tools.intel:setvars_args`: **(optional)** it is used to pass whatever we want as arguments to our setvars.sh|bat file.
  You can check out all the possible ones from the Intel official documentation.
