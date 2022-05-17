.. _examples_tools_meson_mesontoolchain_developer_flow:

MesonToolchain: using in developer flow
----------------------------------------

One of the advantages of using Conan toolchains is that they can help to achieve the exact same build
with local development flows, than when the package is created in the cache.

With the ``MesonToolchain`` it is possible to do:

.. code:: bash

    # Lets start in the folder containing the conanfile.py
    $ mkdir build && cd build
    # Install both debug and release deps and create the toolchain
    $ conan install ..
    # The build type Release is encoded in the toolchain already.
    # This conan_meson_native.ini is specific for release
    $ meson setup --native-file conan_meson_native.ini build .
    $ meson compile -C build
