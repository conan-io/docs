.. _tutorial_creating_configure:

Configure settings and options in recipes
=========================================

We already explained :ref:`Conan settings and options<settings_and_options_difference>`
and how to use them to build your projects for different configurations like Debug,
Release, with static or shared libraries, etc. In this section, we explain how to
configure these settings and options in the case that one of them does not apply to a
Conan package. We will introduce briefly how Conan models binary compatibility and how
that relates to options and settings.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/configure_options_settings

You will notice some changes in the **conanfile.py** file from the previous recipe.
Let's check the relevant parts:

.. code-block:: python
    :emphasize-lines: 21

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

        def configure(self):
            if self.options.shared:
                # If os=Windows, fPIC will have been removed in config_options()
                # use rm_safe to avoid double delete errors
                self.options.rm_safe("fPIC")
        ...


You can see that we added a :ref:`configure() method<reference_conanfile_methods_configure>` to the recipe. Let's explain what's the
objective of this method and how it's different from the ``config_options()`` method we
already had defined in the recipe:

* ``configure()``: use this method to configure which options or settings of the recipe
  are available. For example, in this case, we **delete the fPIC option**, because it
  should only be **True** if we are building the library as shared (in fact, some build
  systems will add this flag automatically when building a shared library).


* ``config_options()``: This method is used to **constrain** the available options in a
  package **before they take a value**. If a value is assigned to a setting or option that is
  deleted inside this method, Conan will raise an error. In this case we are **deleting
  the fPIC option** in Windows because that option does not exist for that operating
  system. Note that this method is executed before the ``configure()`` method.

Be aware that deleting an option using the ``config_options()`` method has a different result from using the ``configure()`` 
method. Deleting the option in ``config_options()`` **is like we never declared
it in the recipe** which will raise an exception saying that the option does not exist.
However, if we delete it in the ``configure()`` method we can pass the option but it
will have no effect. For example, if you try to pass a value to the ``fPIC`` option in
Windows, Conan will raise an error warning that the option does not exist:

.. code-block:: text
    :caption: Windows

    $ conan create . --build=missing -o fPIC=True
    ...
    -------- Computing dependency graph --------
    ERROR: option 'fPIC' doesn't exist
    Possible options are ['shared', 'with_fmt']


As you have noticed, the ``configure()`` and ``config_options()`` methods **delete an
option** if certain conditions are met. Let's explain why we are doing this and the
implications of removing that option. It is related to how Conan identifies packages that
are binary compatible with the configuration set in the profile. In the next section, we
introduce the concept of the **Conan package ID**.


.. _creating_packages_configure_options_settings:

Conan packages binary compatibility: the **package ID**
-------------------------------------------------------

We used Conan in previous examples to build for different configurations like *Debug* and
*Release*. Each time you create the package for one of those configurations, Conan will
build a new binary. Each of them is related to a **generated hash** called **the package
ID**. The package ID is just a way to convert a set of settings, options and information
about the requirements of the package to a unique identifier. 

Let's build our package for *Release* and *Debug* configurations and check
the generated binaries package IDs.

.. code-block:: bash
    :emphasize-lines: 6,19,29,42
    
    $ conan create . --build=missing -s build_type=Release -tf="" # -tf="" will skip ng the test_package
    ...
    [ 50%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [100%] Linking CXX static library libhello.a
    [100%] Built target hello
    hello/1.0: Package '738feca714b7251063cc51448da0cf4811424e7c' built
    hello/1.0: Build folder /Users/user/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release
    hello/1.0: Generated conaninfo.txt
    hello/1.0: Generating the package
    hello/1.0: Temporary package folder /Users/user/.conan2/p/tmp/7fe7f5af0ef27552/p
    hello/1.0: Calling package()
    hello/1.0: CMake command: cmake --install "/Users/user/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release" --prefix "/Users/user/.conan2/p/tmp/7fe7f5af0ef27552/p"
    hello/1.0: RUN: cmake --install "/Users/user/.conan2/p/tmp/7fe7f5af0ef27552/b/build/Release" --prefix "/Users/user/.conan2/p/tmp/7fe7f5af0ef27552/p"
    -- Install configuration: "Release"
    -- Installing: /Users/user/.conan2/p/tmp/7fe7f5af0ef27552/p/lib/libhello.a
    -- Installing: /Users/user/.conan2/p/tmp/7fe7f5af0ef27552/p/include/hello.h
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello.a
    hello/1.0: Package '738feca714b7251063cc51448da0cf4811424e7c' created
    hello/1.0: Created package revision 3bd9faedc711cbb4fdf10b295268246e
    hello/1.0: Full package reference: hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:738feca714b7251063cc51448da0cf4811424e7c#3bd9faedc711cbb4fdf10b295268246e
    hello/1.0: Package folder /Users/user/.conan2/p/5c497cbb5421cbda/p

    $ conan create . --build=missing -s build_type=Debug -tf="" # -tf="" will skip building the test_package
    ...
    [ 50%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [100%] Linking CXX static library libhello.a
    [100%] Built target hello
    hello/1.0: Package '3d27635e4dd04a258d180fe03cfa07ae1186a828' built
    hello/1.0: Build folder /Users/user/.conan2/p/tmp/19a2e552db727a2b/b/build/Debug
    hello/1.0: Generated conaninfo.txt
    hello/1.0: Generating the package
    hello/1.0: Temporary package folder /Users/user/.conan2/p/tmp/19a2e552db727a2b/p
    hello/1.0: Calling package()
    hello/1.0: CMake command: cmake --install "/Users/user/.conan2/p/tmp/19a2e552db727a2b/b/build/Debug" --prefix "/Users/user/.conan2/p/tmp/19a2e552db727a2b/p"
    hello/1.0: RUN: cmake --install "/Users/user/.conan2/p/tmp/19a2e552db727a2b/b/build/Debug" --prefix "/Users/user/.conan2/p/tmp/19a2e552db727a2b/p"
    -- Install configuration: "Debug"
    -- Installing: /Users/user/.conan2/p/tmp/19a2e552db727a2b/p/lib/libhello.a
    -- Installing: /Users/user/.conan2/p/tmp/19a2e552db727a2b/p/include/hello.h
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello.a
    hello/1.0: Package '3d27635e4dd04a258d180fe03cfa07ae1186a828' created
    hello/1.0: Created package revision 67b887a0805c2a535b58be404529c1fe
    hello/1.0: Full package reference: hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:3d27635e4dd04a258d180fe03cfa07ae1186a828#67b887a0805c2a535b58be404529c1fe
    hello/1.0: Package folder /Users/user/.conan2/p/c7796386fcad5369/p

As you can see Conan generated two package IDs:

* Package *738feca714b7251063cc51448da0cf4811424e7c* for Release
* Package *3d27635e4dd04a258d180fe03cfa07ae1186a828* for Debug

These two package IDs are calculated by taking the **set of settings, options and some
information about the requirements** (we will explain this later in the documentation) and
**calculating a hash** with them. So, for example, in this case, they are the result of the
information depicted in the diagram below.

.. image:: /images/conan-package_id.png
   :width: 680 px
   :align: center

Those package IDs are different because the **build_type** is different. Now, when you want
to install a package, Conan will:

* Collect the settings and options applied, along with some information about the
  requirements and calculate the hash for the corresponding package ID.

* If that package ID matches one of the packages stored in the local Conan cache Conan
  will use that. If not, and we have any Conan remote configured, it will search for a
  package with that package ID in the remotes.

* If that calculated package ID does not exist in the local cache and remotes, Conan will
  fail with a "missing binary" error message, or will try to build that package from
  sources (this depends on the value of the ``--build`` argument). This build will
  generate a new package ID in the local cache.

These steps are simplified, there is far more to package ID calculation than what we
explain here, recipes themselves can even adjust their package ID calculations, we can
have different recipe and package revisions besides package IDs and there's also a
built-in mechanism in Conan that can be configured to declare that some packages with a
certain package ID are compatible with other.

Maybe you have now the intuition of why we delete settings or options in Conan recipes.
If you do that, those values will not be added to the computation of the package ID, so
even if you define them, the resulting package ID will be the same. You can check this
behaviour, for example with the fPIC option that is deleted when we build with the
option ``shared=True``. Regardless of the value you pass for the fPIC option the generated
package ID will be the same for the **hello/1.0** binary:

.. code-block:: bash
    
    $ conan conan create . --build=missing -o shared=True -o fPIC=True -tf=""
    ...
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.dylib' file: libhello.dylib
    hello/1.0: Package '2a899fd0da3125064bf9328b8db681cd82899d56' created
    hello/1.0: Created package revision f0d1385f4f90ae465341c15740552d7e
    hello/1.0: Full package reference: hello/1.0#e6b11fb0cb64e3777f8d62f4543cd6b3:2a899fd0da3125064bf9328b8db681cd82899d56#f0d1385f4f90ae465341c15740552d7e
    hello/1.0: Package folder /Users/user/.conan2/p/8a55286c6595f662/p

    $ conan conan create . --build=missing -o shared=True -o fPIC=False -tf=""
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

As you can see, the first run created the ``2a899fd0da3125064bf9328b8db681cd82899d56``
package, and the second one, regardless of the different value of the fPIC option, said we
already had the ``2a899fd0da3125064bf9328b8db681cd82899d56`` package installed.

C libraries
^^^^^^^^^^^

There are other typical cases where you want to delete certain settings. Imagine that you
are packaging a C library. When you build this library, there are settings like the
compiler C++ standard (``settings.compiler.cppstd``) or the standard library used
(``self.settings.compiler.libcxx``) that won't affect the resulting binary at all. Then it
does not make sense that they affect to the package ID computation, so a typical pattern is
to delete them in the ``configure()`` method:

.. code-block:: python
    
    def configure(self):
        del self.settings.compiler.cppstd
        del self.settings.compiler.libcxx

Please, note that deleting these settings in the ``configure()`` method will modify the
package ID calculation but will also affect how the toolchain, and the build system
integrations work because the C++ settings do not exist.

Header-only libraries
^^^^^^^^^^^^^^^^^^^^^

A similar case happens with packages that package :ref:`header-only
libraries<creating_packages_other_header_only>`. In that case,
there's no binary code we need to link with, but just some header files to add to our
project. In this cases the package ID of the Conan package should not be affected by
settings or options. For that case, there's a simplified way of declaring that the
generated package ID should not take into account settings, options or any information
from the requirements, which is using the ``self.info.clear()`` method inside another recipe
method called ``package_id()``:

.. code-block:: python
    
    def package_id(self):
        self.info.clear()


We will explain the ``package_id()`` method later and explain how you can customize the
way the package ID for the package is calculated. You can also check the :ref:`Conanfile's
methods reference<reference_conanfile_methods>` if you want to know how this method works in
more detail.

Read more
---------

- :ref:`Header-only packages<creating_packages_other_header_only>`.
- Check the binary compatibility :ref:`compatibility.py extension <reference_extensions_binary_compatibility>`.
- Conan :ref:`package types<reference_conanfile_attributes_package_type>`.
- :ref:`Setting package_id_mode for requirements <reference_conanfile_methods_requirements_package_id_mode>`.
- Read the :ref:`binary model reference<reference_binary_model>` for a full view of the Conan binary model.
