Configure settings and options in recipes
=========================================

.. important::

    In this example, we retrieve the CMake Conan package from a Conan repository with
    packages compatible with Conan 2.0. To run this example successfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``

We already explained what :ref:`Conan settings and options
are<settings_and_options_difference>` and how to use them to build your projects for
different configurations like Debug, Release, with static or shared libraries, etc. In
this section, we explain how to configure these settings and options for example, in the
case that a certain setting or option does not apply to a Conan recipe. We will also give a
short introduction on how Conan models binary compatibility and how that relates to
options and settings.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/configure_options_settings

You will notice some changes in the `conanfile.py` file from the previous recipe.
Let's check the relevant parts:

.. code-block:: python

    ...
    from conan.tools.build import check_min_cppstd
    ...

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...
        options = {"shared": [True, False], 
                   "fPIC": [True, False],
                   "with_fmt": [True, False]}

        default_options = {"shared": False, 
                           "fPIC": True,
                           "with_fmt": True}
        ...

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC
            #del self.settings.compiler.cppstd
            #del self.settings.compiler.libcxx

        def configure(self):
            if self.options.shared:
                del self.options.fPIC
        ...


You can see that we added a ``configure()`` method to the recipe. Let's explain what's the
objective of this method and how it's different from the ``config_options()`` method we
already had defined in our recipe:

* ``configure()``: this method is useful to modify the available options or settings of
  the recipe. For example, in this case, we **delete the fPIC option**, because it should
  only be True if we are building the library as shared. In fact, some build systems will
  add this flag automatically when building a shared library.


* ``config_options()``: this method is executed before the ``configure()`` method. In
  fact, options are not given a value yet in this method. This method is used to
  **constraint** the available options in a package, before they are given a value. So when a
  value is tried to be assigned it will raise an error. In this case we are **deleting the
  fPIC option** in Windows because that option does not exist for that operating system.

Be aware that deleting an option in the ``config_options()`` or in the ``configure()`` has
not the same result. Deleting it in the ``config_options()`` is like if we never had
declared it in the recipe and it will raise an exception saying that the option does not
exist. Nevertheless, if we delete it in the ``configure()`` method we can pass the option
but it will just have no effect.

As you have noticed, both in the ``configure()`` and ``config_options()`` methods we are
**deleting** an option if certain conditions meet. But, why are we doing that and what are
the implications of removing that options? This is related to how Conan identify packages
that are binary compatible with the configuration set in the profile. Let's get a bit
deeper into this topic:

Conan packages binary compatibililty: the *Package ID*
------------------------------------------------------

We already used Conan in previous examples to build for different configurations, for
example for *Debug* and *Release*. When you build one package for each of those
configurations, Conan will create a new binary. Each of those binaries are related to a
generated hash called the *Package ID*. The *Package ID* is just a way to convert a set of
settings, options and information about the requirements of the package to a unique
identifier. Let's build our package for *Release* and *Debug* configurations and what's the
generated binaries *Package ID*.

.. code-block:: bash
    
    $ conan create . --build=missing -s compiler.cppstd=gnu11 -s build_type=Release -tf=None # -tf=None will skip buildint the test_package
    Exporting the recipe
    hello/1.0: Exporting package recipe
    hello/1.0: Using the exported files summary hash as the recipe revision: e6b11fb0cb64e3777f8d62f4543cd6b3 
    hello/1.0: A new conanfile.py version was exported
    hello/1.0: Folder: /Users/carlosz/.conan2/p/4032f82fc586cb59/e
    hello/1.0: Exported revision: e6b11fb0cb64e3777f8d62f4543cd6b3

    -------- Input profiles --------
    Profile host:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu11
    compiler.libcxx=libc++
    compiler.version=13
    os=Macos
    [options]
    [tool_requires]
    [env]

    Profile build:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=14
    compiler.libcxx=libc++
    compiler.version=13
    os=Macos
    [options]
    [tool_requires]
    [env]


    -------- Computing dependency graph --------
    Graph root
        virtual
    Requirements
        fmt/8.1.1#601209640bd378c906638a8de90070f7 - Cache
        hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3 - Cache

    -------- Computing necessary packages --------
    hello/1.0: Forced build from source
    Requirements
        fmt/8.1.1#601209640bd378c906638a8de90070f7:d1b3f3666400710fec06446a697f9eeddd1235aa#b8e44285c03c783bd9ee49c0841815e1 - Cache
        hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:738feca714b7251063cc51448da0cf4811424e7c - Build

    -------- Installing packages --------

    -------- Installing (downloading, building) binaries... --------
    fmt/8.1.1: Already installed!
    hello/1.0: Calling source() in /Users/carlosz/.conan2/p/4032f82fc586cb59/s/.
    hello/1.0: Cloning git repo
    hello/1.0: Checkout: optional_fmt
    hello/1.0: Copying sources to build folder
    hello/1.0: Building your package in /Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b
    hello/1.0: Generator 'CMakeDeps' calling 'generate()'
    hello/1.0: Calling generate()
    hello/1.0: Aggregating env generators
    hello/1.0: Calling build()
    hello/1.0: CMake command: cmake -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE="/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/p" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" -DCMAKE_BUILD_TYPE="Release" "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/."
    hello/1.0: RUN: cmake -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE="/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/generators/conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/p" -DCMAKE_POLICY_DEFAULT_CMP0091="NEW" -DCMAKE_BUILD_TYPE="Release" "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/."
    -- Using Conan toolchain: /Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/generators/conan_toolchain.cmake
    -- Conan toolchain: Setting CMAKE_POSITION_INDEPENDENT_CODE=ON (options.fPIC)
    -- Conan toolchain: C++ Standard 11 with extensions ON
    -- Conan toolchain: Setting BUILD_SHARED_LIBS = OFF
    -- The CXX compiler identification is AppleClang 13.1.6.13160021
    -- Detecting CXX compiler ABI info
    -- Detecting CXX compiler ABI info - done
    -- Check for working CXX compiler: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ - skipped
    -- Detecting CXX compile features
    -- Detecting CXX compile features - done
    -- Conan: Target declared 'fmt::fmt'
    -- Configuring done
    -- Generating done
    CMake Warning:
    Manually-specified variables were not used by the project:

        CMAKE_POLICY_DEFAULT_CMP0091


    -- Build files have been written to: /Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release
    hello/1.0: CMake command: cmake --build "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release" '--' '-j16'
    hello/1.0: RUN: cmake --build "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release" '--' '-j16'
    [ 50%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [100%] Linking CXX static library libhello.a
    [100%] Built target hello
    hello/1.0: Package '738feca714b7251063cc51448da0cf4811424e7c' built
    hello/1.0: Build folder /Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release
    hello/1.0: Generated conaninfo.txt
    hello/1.0: Generating the package
    hello/1.0: Temporary package folder /Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/p
    hello/1.0: Calling package()
    hello/1.0: CMake command: cmake --install "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release" --prefix "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/p"
    hello/1.0: RUN: cmake --install "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release" --prefix "/Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/p"
    -- Install configuration: "Release"
    -- Installing: /Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/p/lib/libhello.a
    -- Installing: /Users/carlosz/.conan2/p/tmp/7fe7f5af0ef27552/p/include/hello.h
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello.a
    hello/1.0: Package '738feca714b7251063cc51448da0cf4811424e7c' created
    hello/1.0: Created package revision f9110f8892090e94a1ab892f216cc5bb
    hello/1.0: Full package reference: hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:738feca714b7251063cc51448da0cf4811424e7c#f9110f8892090e94a1ab892f216cc5bb
    hello/1.0: Package folder /Users/carlosz/.conan2/p/a5f69282294cd2ea/p




- Que quiere decir borrar un setting o una opción?




Read more
---------

- 