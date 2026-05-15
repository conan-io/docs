<a id="consuming-packages-cross-building-with-conan"></a>

# How to cross-compile your applications using Conan: host and build contexts

Please, first clone the sources to recreate this project. You can find them in the
[examples2 repository](https://github.com/conan-io/examples2) on GitHub:

```bash
$ git clone https://github.com/conan-io/examples2.git
$ cd examples2/tutorial/consuming_packages/cross_building
```

In the previous examples, we learned how to use a *conanfile.py* or *conanfile.txt* to
build an application that compresses strings using the *Zlib* and *CMake* Conan packages.
Also, we explained that you can set information like the operating system, compiler or
build configuration in a file called the Conan profile. You can use that profile as an
argument (**--profile**) to invoke the **conan install** command. We also explained that
not specifying that profile is equivalent to using the **--profile=default** argument.

For all those examples, we used the same platform for building and running the
application. But, what if you want to build the application on your machine running Ubuntu
Linux and then run it on another platform like a
Raspberry Pi? Conan can model that case using two different profiles, one for the
machine that **builds** the application (Ubuntu Linux) and another for the machine that
**runs** the application (Raspberry Pi). We will explain this “two profiles” approach in
the next section.

## Conan two profiles model: build and host profiles

Even if you specify only one **--profile** argument when invoking Conan, Conan will
internally use two profiles. One for the machine that **builds** the binaries (called the
**build** profile) and another for the machine that **runs** those binaries (called the
**host** profile). Calling this command:

```bash
$ conan install . --build=missing --profile=someprofile
```

Is equivalent to:

```bash
$ conan install . --build=missing --profile:host=someprofile --profile:build=default
```

As you can see we used two new arguments:

* `profile:host`: This is the profile that defines the platform where the built binaries
  will run. For our string compressor application, this profile would be the one applied
  for the *Zlib* library that will run on a **Raspberry Pi**.
* `profile:build`: This is the profile that defines the platform where the binaries will be built.
  For our string compressor application, this profile would be the one
  used by the *CMake* tool that will compile it on the **Ubuntu Linux** machine.

Note that when you just use one argument for the profile `--profile` is equivalent to
`--profile:host`. If you don’t specify the `--profile:build` argument, Conan will use
the *default* profile internally.

So, if we want to build the compressor application on the Ubuntu Linux machine but run it
on a Raspberry Pi, we should use two different profiles. For the **build** machine, we
could use the default profile that in our case looks like this:

```bash
[settings]
os=Linux
arch=x86_64
build_type=Release
compiler=gcc
compiler.cppstd=gnu17
compiler.libcxx=libstdc++11
compiler.version=12
```

And the profile for the Raspberry Pi that is the **host** machine:

```bash
[settings]
os=Linux
arch=armv7hf
compiler=gcc
build_type=Release
compiler.cppstd=gnu17
compiler.libcxx=libstdc++11
compiler.version=12
[buildenv]
CC=arm-linux-gnueabihf-gcc-12
CXX=arm-linux-gnueabihf-g++-12
LD=arm-linux-gnueabihf-ld
```

#### IMPORTANT
Please, take into account that in order to build this example successfully, you should
have installed a toolchain that includes the compiler and all the tools to build the
application for the proper architecture. In this case, the host machine is a Raspberry
Pi 3 with *armv7hf* architecture operating system and we have the
*arm-linux-gnueabihf* toolchain installed on the Ubuntu machine.

If you have a look at the *raspberry* profile, there is a section named
`[buildenv]`. This section is used to set the environment variables that are needed to
build the application. In this case, we declare the `CC`, `CXX` and `LD` variables
pointing to the cross-build toolchain compilers and linker, respectively. Adding this
section to the profile will invoke the *VirtualBuildEnv* generator everytime we do a
**conan install**. This generator will add that environment information to the
`conanbuild.sh` script that we will source before building with CMake so that it can use
the cross-build toolchain.

#### NOTE
In some cases, you don’t have the toolchain available on the build platform. For those
cases, you can use a Conan package for the cross-compiler and add it to the
`[tool_requires]` section of the profile. For an example of cross-building using a
toolchain package, please check [this example](https://docs.conan.io/2//examples/cross_build/toolchain_packages.html.md#example-cross-build-toolchain-package-use).

### Build and host contexts

Now that we have our two profiles prepared, let’s have a look at our *conanfile.py*:

```python
from conan import ConanFile
from conan.tools.cmake import cmake_layout

class CompressorRecipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires("zlib/1.3.1")

    def build_requirements(self):
        self.tool_requires("cmake/3.27.9")

    def layout(self):
        cmake_layout(self)
```

As you can see, this is practically the same *conanfile.py* we used in the [previous
example](https://docs.conan.io/2//tutorial/consuming_packages/the_flexibility_of_conanfile_py.html.md#consuming-packages-flexibility-of-conanfile-py). We will require **zlib/1.3.1**
as a regular dependency and **cmake/3.27.9** as a tool needed for building the
application.

We will need the application to build for the Raspberry Pi with the cross-build
toolchain and also link the **zlib/1.3.1** library built for the same platform. On the
other side, we need the **cmake/3.27.9** binary to run on Ubuntu Linux. Conan manages this
internally in the dependency graph differentiating between what we call the “build
context” and the “host context”:

* The **host context** is populated with the root package (the one specified in the
  **conan install** or **conan create** command) and all its requirements
  added via `self.requires()`. In this case, this includes the compressor application
  and the **zlib/1.3.1** dependency.
* The **build context** contains the tool requirements used on the build machine. This
  category typically includes all the developer tools like CMake, compilers and linkers.
  In this case, this includes the **cmake/3.27.9** tool.

These contexts define how Conan will manage each of the dependencies. For example, as
**zlib/1.3.1** belongs to the **host context**, the `[buildenv]` build environment we
defined in the **raspberry** profile (profile host) will only apply to the **zlib/1.3.1**
library when building and won’t affect anything that belongs to the **build context** like
the **cmake/3.27.9** dependency.

Now, let’s build the application. First, call **conan install** with the
profiles for the build and host platforms. This will install the  **zlib/1.3.1**
dependency built for the *armv7hf* architecture and a **cmake/3.27.9** version that runs on a
64-bit architecture.

```bash
$ conan install . --build missing -pr:b=default -pr:h=./profiles/raspberry
```

Then, let’s call CMake to build the application. As we did in the previous example, we have
to activate the **build environment** running `source Release/generators/conanbuild.sh`. That will
set the environment variables needed to locate the cross-build toolchain and build the
application.

```bash
$ cd build
$ source Release/generators/conanbuild.sh
Capturing current environment in deactivate_conanbuildenv-release-armv7hf.sh
Configuring environment variables
$ cmake .. -DCMAKE_TOOLCHAIN_FILE=Release/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
$ cmake --build .
...
-- Conan toolchain: C++ Standard 17 with extensions ON
-- The C compiler identification is GNU 12.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/arm-linux-gnueabihf-gcc-12 - skipped
-- Detecting C compile features
-- Detecting C compile features - done    [100%] Built target compressor
...
$ source Release/generators/deactivate_conanbuild.sh
```

You could check that we built the application for the correct architecture by running the
`file` Linux utility:

```bash
$ file compressor
compressor: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV), dynamically
linked, interpreter /lib/ld-linux-armhf.so.3,
BuildID[sha1]=2a216076864a1b1f30211debf297ac37a9195196, for GNU/Linux 3.2.0, not
stripped
```

#### SEE ALSO
- [JFrog Academy Conan 2 Essentials Module 1, Lesson 5: Cross-Compiling Your Applications With Conan](https://academy.jfrog.com/path/conan-cc-package-manager/conan-2-essentials?utm_source=Conan+Docs)
- [Creating a Conan package for a toolchain](https://docs.conan.io/2//examples/cross_build/toolchain_packages.html.md#example-cross-build-toolchain-package)
- [Cross building to Android with the NDK](https://docs.conan.io/2//examples/cross_build/android/ndk.html.md#examples-cross-build-android-ndk)
- [VirtualBuildEnv reference](https://docs.conan.io/2//reference/tools/env/virtualbuildenv.html.md#conan-tools-env-virtualbuildenv)
- Cross-build using a tool_requires
- [How to require test frameworks like gtest: using test_requires](https://docs.conan.io/2//reference/conanfile/methods/build_requirements.html.md#reference-conanfile-methods-build-requirements-test-requires)
- Using Conan to build for iOS
