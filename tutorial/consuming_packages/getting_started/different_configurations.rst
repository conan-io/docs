.. _consuming_packages_getting_started_different_configurations:

Building for multiple configurations: Release, Debug, Static and Shared
=======================================================================

.. important::

    In this example, we will retrieve the CMake Conan package from a Conan repository with
    packages compatible for Conan 2.0. To run this example succesfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


So far, we have built a simple CMake project that depended on the **zlib** library and
learned about ``tool_requires``, a special type or requirements to use build tools. In
both cases we did not specify anywhere that we wanted to build the application in
*Release* or *Debug* mode, or if we wanted to link against *static* or *shared* libraries.
That is because Conan, if not instructed otherwise will use a default configuration
declared in the 'default profile'. This default profile was created in the first example
when we run the ``conan profile`` command. Conan stores this file in the **/profiles**
folder, located in the Conan user home. You can check the contents of your default profile:

Run the ``conan config`` command and get the location of the Conan user home, then show
the contents of the default profile:

.. code-block:: bash

    $ conan config home
    Current Conan home: /Users/tutorial_user/.conan2
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


Read more
---------

- Installing configurations with conan config install
- VS Multi-config
