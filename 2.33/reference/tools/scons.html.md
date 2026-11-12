<a id="conan-tools-sconsdeps"></a>

# conan.tools.scons

## SConsDeps

The `SConsDeps` is the dependency generator for [SCons](https://scons.org/). It will
generate a SConscript_conandeps file containing the necessary information for SCons to
build against the desired dependencies.

The `SConsDeps` generator can be used by name in conanfiles:

```python
from conan import ConanFile

class Pkg(ConanFile):
    generators = "SConsDeps"
```

```text
[generators]
SConsDeps
```

It can also be fully instantiated in the conanfile `generate()` method:

```python
from conan import ConanFile
from conan.tools.scons import SConsDeps

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    def generate(self):
        tc = SConsDeps(self)
        tc.generate()
```

After executing the `conan install` command, the `SConsDeps` generator will create the
SConscript_conandeps file. This file will provide the following information for SCons:
`CPPPATH`, `LIBPATH`, `BINPATH`, `LIBS`, `FRAMEWORKS`, `FRAMEWORKPATH`,
`CPPDEFINES`, `CXXFLAGS`, `CCFLAGS`, `SHLINKFLAGS`, and `LINKFLAGS`. This information
is generated for the accumulated list of all dependencies and also for each one of the
requirements. You can load it in your consumer SConscript like this:

```python
...
info = SConscript('./SConscript_conandeps')
# You can use conandeps to get the information
# for all the dependencies.
flags = info["conandeps"]

# Or use the name of the requirement if
# you only want the information about that one.
flags = info["zlib"]

env.MergeFlags(flags)
...
```
