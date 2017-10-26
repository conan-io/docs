profiles/default
================

This is the typical ``~/.conan/profiles/default`` file:


.. code-block:: text

    [build_requires]
    [settings]
        os=Macos
        arch=x86_64
        compiler=apple-clang
        compiler.version=8.1
        compiler.libcxx=libc++
        build_type=Release
    [options]
    [scopes]
    [env]

The settings defaults are the setting values used whenever you issue a ``conan install`` command over
a ``conanfile`` in one of your projects. The initial values for these default settings are
auto-detected the first time you run a ``conan`` command.

You can override the default settings using the ``-s`` parameter in ``conan install`` and ``conan info``
commands but when you specify a profile, ``conan install --profile gcc48``, the default profile
won't be applied, unless you specify it with an ``include`` statement:

**myprofile.txt**

.. code-block:: text

   include(default)

   [settings]
   compiler=clang
   compiler.version=3.5
   compiler.libcxx=libstdc++11

   [env]
   CC=/usr/bin/clang
   CXX=/usr/bin/clang++

