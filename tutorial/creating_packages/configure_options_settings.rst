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
    :emphasize-lines: 25

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
the implications of removing that option? This is related to how Conan identify packages
that are binary compatible with the configuration set in the profile. Let's get a bit
deeper into this topic:

Conan packages binary compatibililty: the *Package ID*
------------------------------------------------------

We already used Conan in previous examples to build for different configurations, for
example for *Debug* and *Release*. When you build one package for each of those
configurations, Conan will create a new binary. Each of those binaries are related to a
generated hash called the *Package ID*. The *Package ID* is just a way to convert a set of
settings, options and information about the requirements of the package to a unique
identifier. Let's build our package for *Release* and *Debug* configurations and checks
the generated binaries *Package ID*.

.. code-block:: bash
    :emphasize-lines: 6,19,29,42
    
    $ conan create . --build=missing -s compiler.cppstd=gnu11 -s build_type=Release -tf=None # -tf=None will skip buildiing the test_package
    ...
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
    hello/1.0: Created package revision 3bd9faedc711cbb4fdf10b295268246e
    hello/1.0: Full package reference: hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:738feca714b7251063cc51448da0cf4811424e7c#3bd9faedc711cbb4fdf10b295268246e
    hello/1.0: Package folder /Users/carlosz/.conan2/p/5c497cbb5421cbda/p

    $ conan create . --build=missing -s compiler.cppstd=gnu11 -s build_type=Debug -tf=None # -tf=None will skip buildiing the test_package
    ...
    [ 50%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [100%] Linking CXX static library libhello.a
    [100%] Built target hello
    hello/1.0: Package '3d27635e4dd04a258d180fe03cfa07ae1186a828' built
    hello/1.0: Build folder /Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/b/build/Debug
    hello/1.0: Generated conaninfo.txt
    hello/1.0: Generating the package
    hello/1.0: Temporary package folder /Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/p
    hello/1.0: Calling package()
    hello/1.0: CMake command: cmake --install "/Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/b/build/Debug" --prefix "/Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/p"
    hello/1.0: RUN: cmake --install "/Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/b/build/Debug" --prefix "/Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/p"
    -- Install configuration: "Debug"
    -- Installing: /Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/p/lib/libhello.a
    -- Installing: /Users/carlosz/.conan2/p/tmp/19a2e552db727a2b/p/include/hello.h
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello.a
    hello/1.0: Package '3d27635e4dd04a258d180fe03cfa07ae1186a828' created
    hello/1.0: Created package revision 67b887a0805c2a535b58be404529c1fe
    hello/1.0: Full package reference: hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:3d27635e4dd04a258d180fe03cfa07ae1186a828#67b887a0805c2a535b58be404529c1fe
    hello/1.0: Package folder /Users/carlosz/.conan2/p/c7796386fcad5369/p

As you can see Conan generated two package ID's:

* Package *738feca714b7251063cc51448da0cf4811424e7c* for Release
* Package *3d27635e4dd04a258d180fe03cfa07ae1186a828* for Debug

These two Package ID's are calculated taking the set of settings, options and some
information about the requirements (we will explain this later in the documentation) and
calculating a hash with them. So, for example, in this case they are the result of the
information depicted in the diagram below.

.. image:: /images/conan-package_id.png
   :width: 680 px
   :align: center

Those Package ID's are different because the build_type is different. Now, when you want
to install a package, Conan will:

* Collect the settings and options applied, along with some information about the
  requirements and calculate the hash for the corresponding Package ID.

* If that Package ID matches one of the packages stored in the local Conan cache it will
  use that. If not, and we have any Conan remote configured, it will search for a package
  with that Package ID in the remotes.

* If that calculated Package ID is not found in the local cache and remotes, Conan will
  try to build that package from sources (this actually depends on the value of the
  ``--build`` argument). This build will generate a new Package ID that was not already stored.

This flow is simplified, there is far more to Package ID calculation than what is
shown here, recipes themselves can even adjust their own package id calculations, we can
have different recipe and package revisions besides Package ID's and there's also a
built-in mechanism in Conan that can be configured to declare that some packages with a
certain Package ID are compatible with other. But let's get that aside to explain what the
concept of the Package ID is.

Maybe you have now the intuituion of why we delete settings or options in Conan recipes.
If you do that, those values will not be added to the computation of the Package ID, so
even if you define them the resulting package will be the same. You can check this
behaviour, for example with the fPIC option that is deleted when we build with with the
option shared=True. Regardless the value you pass for the fPIC option the generated
Package ID will be the same for the **hello/1.0** binary:

.. code-block:: bash
    
    $ conan conan create . --build=missing -s compiler.cppstd=gnu11 -o shared=True -o fPIC=True -tf=None
    ...
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.dylib' file: libhello.dylib
    hello/1.0: Package '2a899fd0da3125064bf9328b8db681cd82899d56' created
    hello/1.0: Created package revision f0d1385f4f90ae465341c15740552d7e
    hello/1.0: Full package reference: hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:2a899fd0da3125064bf9328b8db681cd82899d56#f0d1385f4f90ae465341c15740552d7e
    hello/1.0: Package folder /Users/carlosz/.conan2/p/8a55286c6595f662/p

    $ conan conan create . --build=missing -s compiler.cppstd=gnu11 -o shared=True -o fPIC=True -tf=None
    ...
    -------- Computing dependency graph --------
    Graph root
        virtual
    Requirements
        fmt/8.1.1#601209640bd378c906638a8de90070f7 - Cache
        hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3 - Cache

    -------- Computing necessary packages --------
    Requirements
        fmt/8.1.1#601209640bd378c906638a8de90070f7:d1b3f3666400710fec06446a697f9eeddd1235aa#24a2edf207deeed4151bd87bca4af51c - Skip
        hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:2a899fd0da3125064bf9328b8db681cd82899d56#f0d1385f4f90ae465341c15740552d7e - Cache

    -------- Installing packages --------

    -------- Installing (downloading, building) binaries... --------
    hello/1.0: Already installed!

As you can see, the first run created the `2a899fd0da3125064bf9328b8db681cd82899d56`
package, and the second one, regardless of the different value of the fPIC option, said we
already had the `2a899fd0da3125064bf9328b8db681cd82899d56` package installed.

This is more evident for some packages like the ones that package header only libraries.
In that case, there's no binary code we need to link with, but just some header files to
add to our project. In this cases the Package ID of the Conan package should not be
affected by settings or options.

- Poner el ejemplo de borrarle el compiler a la librería?
- Que quiere decir borrar un setting o una opción?


Read more
---------

- compatibililty.py
- packge id modes