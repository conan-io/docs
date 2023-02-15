.. _local_package_development_flow:

Package development flow
=========================

This section introduces the **Conan local development flow**, which allows you to work on
packages in your local project directory without having to export the contents of the
package to the Conan cache first.

This local workflow encourages users to perform trial-and-error in a local sub-directory
relative to their recipe, much like how developers typically test building their projects
with other build tools. The strategy is to test the `conanfile.py` methods individually
during this phase.

Let's use this flow for the ``hello`` package we created in :ref:`the previous
section<tutorial_creating_packages>`.

Please, first of all, clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/developing_packages/local_package_development_flow

You can check the contents of the folder:

..  code-block:: text

    .
    ├── conanfile.py
    └── test_package
        ├── CMakeLists.txt
        ├── CMakeUserPresets.json
        ├── conanfile.py
        └── src
            └── example.cpp

conan source
^^^^^^^^^^^^

You will generally want to start off with the :command:`conan source` command. The
strategy here is that you’re testing your source method in isolation, and downloading the
files to a temporary sub-folder relative to the *conanfile.py*. This relative folder is
defined by the :ref:`self.folders.source<layout_folders_reference>` property in the
``layout()`` method. In this case, as we are using the pre-defined :ref:`
cmake_layout<cmake_layout>` we set the value with the ``src_folder`` argument.

Let's have a look at the recipe's ``source()`` and ``layout()`` method:

..  code-block:: python

    ...

    def source(self):
        # Please, be aware that using the head of the branch instead of an inmutable tag
        # or commit is not a good practice in general
        get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", 
            strip_root=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    ...


Now run the :command:`conan source` command and check the results:

.. code-block:: bash

    $ conan source .
    conanfile.py (hello/1.0): Calling source() in /Users/.../local_package_development_flow/src
    Downloading main.zip
    conanfile.py (hello/1.0): Unzipping 3.7KB
    Unzipping 100 %        

You can see that a new `src` folder appeared with all the `hello` library sources.

..  code-block:: text
    :emphasize-lines: 3-10

    .
    ├── conanfile.py
    ├── src
    │   ├── CMakeLists.txt
    │   ├── LICENSE
    │   ├── README.md
    │   ├── include
    │   │   └── hello.h
    │   └── src
    │       └── hello.cpp
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── src
            └── example.cpp

Now it's easy to check the sources and validate them. Once you've got your source method
right and it contains the files you expect, you can move on to testing the various
attributes and methods related to downloading dependencies.

conan install
^^^^^^^^^^^^^

After :command:`conan source`, we can run the :command:`conan install` command. This
command will install all the requirements of the recipe if needed and finally prepare all
the files that are necessary for building running the ``generate()`` method.

We can check all the parts from our recipe that are involved in this step:

.. code-block:: python

    ...

    class helloRecipe(ConanFile):

        ...
    
        generators = "CMakeDeps"

        ...

        def layout(self):
            cmake_layout(self, src_folder="src")

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()

        ...

You can see that a new `build` folder appeared with all the files that Conan needs for
building the library like a toolchain for `CMake` and several environment configuration
files.

..  code-block:: text
    :emphasize-lines: 3-10


    .
    ├── build
    │   └── Release
    │       └── generators
    │           ├── CMakePresets.json
    │           ├── cmakedeps_macros.cmake
    │           ├── conan_toolchain.cmake
    │           ├── conanbuild.sh
    │           ├── conanbuildenv-release-x86_64.sh
    │           ├── conanrun.sh
    │           ├── conanrunenv-release-x86_64.sh
    │           ├── deactivate_conanbuild.sh
    │           └── deactivate_conanrun.sh
    ├── conanfile.py
    ├── src
    │   ├── CMakeLists.txt
    │   ├── CMakeUserPresets.json
    │   ├── LICENSE
    │   ├── README.md
    │   ├── include
    │   │   └── hello.h
    │   └── src
    │       └── hello.cpp
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── src
            └── example.cpp

Now, all the files necessary for building are generated and you can move on to testing the
``build()`` method.

conan build
^^^^^^^^^^^

Running the After :command:`conan build` command will invoke the `build()` method:

.. code-block:: python

    ...

    class helloRecipe(ConanFile):

        ...
    
        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        ...

Let's run :command:`conan build`:

.. code-block:: bash

    $ conan build .
    ...
    -- Conan toolchain: C++ Standard 11 with extensions ON
    -- Conan toolchain: Setting BUILD_SHARED_LIBS = OFF
    -- Configuring done
    -- Generating done
    -- Build files have been ...
    conanfile.py (hello/1.0): CMake command: cmake --build ...
    conanfile.py (hello/1.0): RUN: cmake --build ...
    [100%] Built target hello

For most of the recipes, that should have a very simple ``build()`` method, you can also
invoke the build system directly, without invoking Conan, as you have locally all the files
available for building. If you check the contents of src folder, you will find a
`CMakeUserPresets.json` file that you can use to configure and build the `conan-release`
preset. Let's try:

.. code-block:: bash

    $ cd src
    $ cmake --preset conan-release
    ...
    -- Configuring done
    -- Generating done

    $ cmake --build --preset conan-release
    ...
    [100%] Built target hello

You can check that the results invoking CMake directly are equivalent to the ones we got
using the :command:`conan build` command.

.. include:: ../../../../tutorial/cmake_presets_note.rst

conan export-pkg
^^^^^^^^^^^^^^^^

Now that we built the package binaries locally we can also package those artifacts in the
Conan local cache using the :command:`conan export-pkg` command.

..  code-block:: bash

    $ conan export-pkg .
    conanfile.py (hello/1.0) package(): Packaged 1 '.h' file: hello.h
    conanfile.py (hello/1.0) package(): Packaged 1 '.a' file: libhello.a
    conanfile.py (hello/1.0): Package 'b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed' created
    conanfile.py (hello/1.0): Created package revision f09ef573c22f3919ba26ee91ae444eaa
    ...
    conanfile.py (hello/1.0): Package folder /Users/...
    conanfile.py (hello/1.0): Exported package binary

Now you can list the packages in the local Cache and check that the ``hello/1.0`` package was
created.

..  code-block:: bash

    $ conan list hello/1.0
    Local Cache
    hello
        hello/1.0


conan test
^^^^^^^^^^

The final step to test the package for consumers is the test command. This step is quite
straight-forward. You just have to provide the folder where the `test package` is
(``./test_package``) and the reference you are testing (``hello/1.0``):

.. code-block:: bash

    $ conan test test_package hello/1.0

    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example

    -------- Testing the package: Running test() --------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release!
    hello/1.0: __x86_64__ defined
    hello/1.0: __cplusplus201103
    hello/1.0: __GNUC__4
    hello/1.0: __GNUC_MINOR__2
    hello/1.0: __clang_major__14
    hello/1.0: __apple_build_version__14000029


.. seealso::

    - Reference for conan source, install, build, export-pkg and test commands.
    - cpp and folders Reference
    - cmake_layout reference
    - package prebuilt binaries example
    - link all the commands.
