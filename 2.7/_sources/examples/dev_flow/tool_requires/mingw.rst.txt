.. _examples_dev_flow_tool_requires_mingw:

Using a MinGW as tool_requires to build with gcc in Windows
-----------------------------------------------------------

If we had MinGW installed in our environment, we could define a profile like:

.. code-block::

    [settings]
    os=Windows
    compiler=gcc
    compiler.version=12
    compiler.libcxx=libstdc++11
    compiler.threads=posix
    compiler.exception=sjlj
    arch=x86_64
    build_type=Release

    [buildenv]
    PATH+=(path)C:/path/to/mingw/bin
    # other environment we might need like
    CXX=C:/path/to/mingw/bin/g++
    # etc

    [conf]
    # some configuration like 'tools.build:compiler_executables' might be needed for some cases


But we can also use a Conan package that contains a copy of the MinGW compiler and use it
as a ``tool_requires`` instead:

.. code-block::
    :caption: mingw-profile.txt

    [settings]
    os=Windows
    compiler=gcc
    compiler.version=12
    compiler.libcxx=libstdc++11
    compiler.threads=posix
    compiler.exception=seh
    arch=x86_64
    build_type=Release


    [tool_requires]
    mingw-builds/12.2.0


With this profile we can for example create a package in Windows with:


.. code-block:: bash

    # Using a basic template project
    $ conan new cmake_lib -d name=mypkg -d version=0.1
    $ conan create . -pr=mingw
    ...
    -- The CXX compiler identification is GNU 12.2.0
    ...


    ======== Testing the package: Executing test ========
    mypkg/0.1 (test package): Running test()
    mypkg/0.1 (test package): RUN: .\example
    mypkg/0.1: Hello World Release!
    mypkg/0.1: _M_X64 defined
    mypkg/0.1: __x86_64__ defined
    mypkg/0.1: _GLIBCXX_USE_CXX11_ABI 1
    mypkg/0.1: MSVC runtime: MultiThreadedDLL
    mypkg/0.1: __cplusplus201703
    mypkg/0.1: __GNUC__12
    mypkg/0.1: __GNUC_MINOR__2
    mypkg/0.1: __MINGW32__1
    mypkg/0.1: __MINGW64__1
    mypkg/0.1 test_package


.. seealso::

    - The ConanCenter web page for the `mingw-builds package <https://conan.io/center/recipes/mingw-builds>`_
    - The ``conan-center-index`` `mingw-builds Github repo recipe <https://github.com/conan-io/conan-center-index/tree/master/recipes/mingw-builds/all>`_
