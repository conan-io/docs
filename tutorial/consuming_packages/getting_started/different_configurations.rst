.. _consuming_packages_getting_started_different_configurations:

Building for multiple configurations: Release, Debug, Static and Shared
=======================================================================

.. important::

    In this example, we will retrieve the CMake Conan package from a Conan repository with
    packages compatible for Conan 2.0. To run this example succesfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd tutorial/consuming_packages/getting_started/different_configurations


So far, we built a simple CMake project that depended on the **zlib** library and learned
about ``tool_requires``, a special type or requirements for build tools like CMake. In
both cases we did not specify anywhere that we wanted to build the application in
*Release* or *Debug* mode, or if we wanted to link against *static* or *shared* libraries.
That is because Conan, if not instructed otherwise, will use a default configuration
declared in the 'default profile'. This default profile was created in the first example
when we run the ``conan profile detect`` command. Conan stores this file in the **/profiles**
folder, located in the Conan user home. You can check the contents of your default
profile:

Run the ``conan config`` command and get the location of the Conan user home, then show
the contents of the default profile:

.. code-block:: bash

    $ conan config home
    Current Conan home: /Users/tutorial_user/.conan2

    # output the file contents
    $ cat /Users/tutorial_user/.conan2/profiles/default
    [settings]
    os=Macos
    arch=x86_64
    compiler=apple-clang
    compiler.version=13.0
    compiler.libcxx=libc++
    compiler.cppstd=gnu98
    build_type=Release
    [options]
    [tool_requires]
    [env]


You can use the ``--profile`` argument to specify the profile you want to use when calling
Conan. If you don't specify that argument it's equivalent to call it with
``--profile=default``. These two commands will behave exactly the same:

.. code-block:: bash

    $ conan install . --build=missing
    $ conan install . --build=missing --profile=default


You can store different profiles and use them at your criteria. For example, to use a
``build_type=Debug``, or adding some ``tool_requires``.

Using profiles is not the only way to set the configuration you want to use to build your
project. You can always override the profile settings in the Conan command using the
``--settings`` argument. For example, you can build the project from the previous examples
in *Debug* configuration instead of *Release*.




Read more
---------

- Installing configurations with conan config install
- VS Multi-config
- Example about how settings and options influence the package id
- Cross compiling using --profile:build and --profile:host
- Using patterns for settings and options
