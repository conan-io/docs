.. _consuming_packages_different_configurations:

Building for multiple configurations: Release, Debug, Static and Shared
=======================================================================

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/consuming_packages/different_configurations


So far, we built a simple CMake project that depended on the **zlib** library and learned
about ``tool_requires``, a special type of ``requirements`` for build-tools like CMake. In
both cases, we did not specify anywhere that we wanted to build the application in
*Release* or *Debug* mode, or if we wanted to link against *static* or *shared* libraries.
That is because Conan, if not instructed otherwise, will use a default configuration
declared in the 'default profile'. This default profile was created in the first example
when we run the :command:`conan profile detect` command. Conan stores this file in the
**/profiles** folder, located in the Conan user home. You can check the contents of your
default profile by running the :command:`conan config home` command to get the location of the
Conan user home and then showing the contents of the default profile in the **/profiles**
folder:

.. code-block:: bash

    $ conan config home
    Current Conan home: /Users/tutorial_user/.conan2

    # output the file contents
    $ cat /Users/tutorial_user/.conan2/profiles/default
    [settings]
    os=Macos
    arch=x86_64
    compiler=apple-clang
    compiler.version=14.0
    compiler.libcxx=libc++
    compiler.cppstd=gnu11
    build_type=Release
    [options]
    [tool_requires]
    [env]

    # The default profile can also be checked with the command "conan profile show"


As you can see, the profile has different sections. The ``[settings]`` section is the one
that has information about things like the operating system, architecture, compiler, and
build configuration.

When you call a Conan command setting the ``--profile`` argument,
Conan will take all the information from the profile and apply it to the packages you want
to build or install. If you don't specify that argument it's equivalent to call it with
``--profile=default``. These two commands will behave the same:

.. code-block:: bash

    $ conan install . --build=missing
    $ conan install . --build=missing --profile=default


You can store different profiles and use them to build for different settings. For example,
to use a ``build_type=Debug``, or adding a ``tool_requires`` to all the packages you build
with that profile. We will create a *debug* profile to try building with different configurations:

.. code-block:: text
    :caption: <conan home>/profiles/debug
    :emphasize-lines: 8

    [settings]
    os=Macos
    arch=x86_64
    compiler=apple-clang
    compiler.version=14.0
    compiler.libcxx=libc++
    compiler.cppstd=gnu11
    build_type=Debug


.. _different_configurations_modify_settings:

Modifying settings: use Debug configuration for the application and its dependencies
------------------------------------------------------------------------------------

Using profiles is not the only way to set the configuration you want to use. You can also
override the profile settings in the Conan command using the ``--settings`` argument. For
example, you can build the project from the previous examples in *Debug* configuration
instead of *Release*.

Before building, please check that we modified the source code from the previous example to show the build configuration the
sources were built with:

.. code-block:: cpp
    :emphasize-lines: 6-10

    #include <stdlib.h>
    ...

    int main(void) {
        ...
        #ifdef NDEBUG
        printf("Release configuration!\n");
        #else
        printf("Debug configuration!\n");
        #endif

        return EXIT_SUCCESS;
    }

Now let's build our project for *Debug* configuration:

.. code-block:: bash

    $ conan install . --output-folder=build --build=missing --settings=build_type=Debug


As we explained above, this is the equivalent of having *debug* profile and running these
command using the ``--profile=debug`` argument instead of the
``--settings=build_type=Debug`` argument.

This :command:`conan install` command will check if we already have the required libraries in the local cache
(Zlib) for Debug configuration and obtain them if not. It will also set the build
configuration in the ``conan_toolchain.cmake`` toolchain that the CMakeToolchain generator
creates so that when we build the application it's built in *Debug* configuration. Now
build your project as you did in the previous examples and check in the output how it was
built in *Debug* configuration:

.. code-block:: bash
    :caption: Windows
    :emphasize-lines: 8

    # assuming Visual Studio 15 2017 is your VS version and that it matches your default profile
    $ cd build
    $ cmake .. -G "Visual Studio 15 2017" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build . --config Debug
    $ Debug\compressor.exe
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11
    Debug configuration!

.. code-block:: bash
    :caption: Linux, macOS
    :emphasize-lines: 7
    
    $ cd build
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Debug
    $ cmake --build .
    $ ./compressor
    Uncompressed size is: 233
    Compressed size is: 147
    ZLIB VERSION: 1.2.11
    Debug configuration!


.. _different_configurations_modify_options:

Modifying options: linking the application dependencies as shared libraries
---------------------------------------------------------------------------

So far, we have been linking *Zlib* statically in our application. That's because in the
Zlib's Conan package there's an attribute set to build in that mode by default. We can
change from **static** to **shared** linking by setting the ``shared`` option to ``True``
using the ``--options`` argument. To do so, please run:


.. code-block:: bash

    $ conan install . --output-folder=build --build=missing --options=zlib/1.2.11:shared=True


Doing this, Conan will install the *Zlib* shared libraries, generate the files to build with
them and, also the necessary files to locate those dynamic libraries when running the
application.

.. note::

    Options are defined per-package. In this case we were defining that we wanted that specific
    version of zlib/1.2.11 as a shared library. If we had other dependencies and we want all of
    our dependencies (whenever possible) as shared libraries, we would use ``-o *:shared=True``,
    with the ``*`` pattern that matches all package references.


Let's build the application again after configuring it to link *Zlib* as a
shared library:

.. code-block:: bash
    :caption: Windows

    $ cd build
    # assuming Visual Studio 15 2017 is your VS version and that it matches your default profile
    $ cmake .. -G "Visual Studio 15 2017" -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build . --config Release
    ...
    [100%] Built target compressor

.. code-block:: bash
    :caption: Linux, Macos
    
    $ cd build
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
    $ cmake --build .
    ...
    [100%] Built target compressor


Now, if you try to run the compiled executable you will see an error because the
executable can't find the shared libraries for *Zlib* that we just installed.

.. code-block:: bash
    :caption: Windows

    $ Release\compressor.exe
    (on a pop-up window) The code execution cannot proceed because zlib1.dll was not found. Reinstalling the program may fix this problem.
    # This error depends on the console being used and may not always pop up.
    # It could run correctly if the console gets the zlib dll from a different path.

.. code-block:: bash
    :caption: Linux
    
    $ ./compressor
    ./compressor: error while loading shared libraries: libz.so.1: cannot open shared object file: No such file or directory

.. code-block:: bash
    :caption: Macos

    $ ./compressor
    ./compressor: dyld[41259]: Library not loaded: @rpath/libz.1.dylib


This is because shared libraries (*.dll* in windows, *.dylib* in OSX and *.so* in Linux),
are loaded at runtime. That means that the application executable needs to know where are
the required shared libraries when it runs. On Windows, the dynamic linker will search in
the same directory then in the *PATH* directories. On OSX, it will search in the
directories declared in *DYLD_LIBRARY_PATH* as on Linux will use the *LD_LIBRARY_PATH*.

Conan provides a mechanism to define those variables and make it possible, for executables, to
find and load these shared libraries. This mechanism is the ``VirtualRunEnv`` generator.
If you check the output folder you will see that Conan generated a new file called
``conanrun.sh/bat``. This is the result of automatically invoking that ``VirtualRunEnv``
generator when we activated the ``shared`` option when doing the :command:`conan install`. This
generated script will set the **PATH**, **LD_LIBRARY_PATH**, **DYLD_LIBRARY_PATH** and
**DYLD_FRAMEWORK_PATH** environment variables so that executables can find the shared
libraries.

Activate the virtual environment, and run the executables again:

.. code-block:: bash
    :caption: Windows

    $ conanrun.bat
    $ Release\compressor.exe
    Uncompressed size is: 233
    Compressed size is: 147
    ...

.. code-block:: bash
    :caption: Linux, macOS
    
    $ source conanrun.sh
    $ ./compressor
    Uncompressed size is: 233
    Compressed size is: 147
    ...


Just as in the previous example with the ``VirtualBuildEnv`` generator, when we run the
``conanrun.sh/bat`` script a deactivation script called ``deactivate_conanrun.sh/bat`` is
created to restore the environment. Source or run it to do so:


.. code-block:: bash
    :caption: Windows

    $ deactivate_conanrun.bat

.. code-block:: bash
    :caption: Linux, macOS
    
    $ source deactivate_conanrun.sh

.. _settings_and_options_difference:

Difference between settings and options
---------------------------------------

You may have noticed that for changing between *Debug* and *Release* configuration we
used a Conan **setting**, but when we set *shared* mode for our executable we used a
Conan **option**. Please, note the difference between **settings** and **options**:

* **settings** are typically a project-wide configuration defined by the client machine.
  Things like the operating system, compiler or build configuration that will be common to
  several Conan packages and would not make sense to define one default value for only one
  of them. For example, it doesn’t make sense for a Conan package to declare “Visual
  Studio” as a default compiler because that is something defined by the end consumer, and
  unlikely to make sense if they are working in Linux.

* **options** are intended for package-specific configuration that can be set to a default
  value in the recipe. For example, one package can define that its default linkage is
  static, and this is the linkage that should be used if consumers don’t specify
  otherwise.

Introducing the concept of Package ID
-------------------------------------

When consuming packages like Zlib with different `settings` and `options`, you might
wonder how Conan determines which binary to retrieve from the remote. The answer lies in
the concept of the `package_id`.

The `package_id` is an identifier that Conan uses to determine the binary compatibility of
packages. It is computed based on several factors, including the package's `settings`,
`options`, and dependencies. When you modify any of these factors, Conan computes a new
`package_id` to reference the corresponding binary.

Here's a breakdown of the process:

1. **Determine Settings and Options**: Conan first retrieves the user's input settings and
   options. These can come from the command line or profiles like
   `--settings=build_type=Debug` or `--profile=debug`.
2. **Compute the Package ID**: With the current values for `settings`, `options`, and
   dependencies, Conan computes a hash. This hash serves as the `package_id`, representing
   the binary package's unique identity.
3. **Fetch the Binary**: Conan then checks its cache or the specified remote for a binary
   package with the computed `package_id`. If it finds a match, it retrieves that binary.
   If not, Conan can build the package from source or indicate that the binary is missing.

In the context of our tutorial, when we consumed Zlib with different `settings` and
`options`, Conan used the `package_id` to ensure that it fetched the correct binary that
matched our specified configuration.


.. seealso::

    - :ref:`VirtualRunEnv reference <conan_tools_env_virtualrunenv>`
    - :ref:`Cross-compiling using --profile:build and --profile:host <consuming_packages_cross_building_with_conan>`
    - :ref:`creating_packages_configure_options_settings`
    - :ref:`Installing configurations with conan config install <reference_commands_conan_config_install>`
    - VS Multi-config
    - :ref:`How settings and options influence the package id <reference_binary_model_settings_options>`
    - :ref:`Using patterns for settings and options <reference_config_files_profile_patterns>`
