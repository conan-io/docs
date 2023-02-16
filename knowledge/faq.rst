.. _faq:

FAQ
===

.. seealso::

    There is a great community behind Conan with users helping each other in `Cpplang Slack`_.
    Please join us in the ``#conan`` channel!

Troubleshooting
---------------

ERROR: Missing prebuilt package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When installing packages (with :command:`conan install` or :command:`conan create`) it is possible
that you get an error like the following one:

.. code-block:: text

    ERROR: Missing binary: zlib/1.2.11:b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed

    zlib/1.2.11: WARN: Can't find a 'zlib/1.2.11' package binary 'b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed' for the configuration:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu11
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos
    [options]
    fPIC=True
    shared=False

    ERROR: Missing prebuilt package for 'zlib/1.2.11'
    Check the available packages using 'conan list zlib/1.2.11:* -r=remote'
    or try to build locally from sources using the '--build=zlib/1.2.11' argument

    More Info at 'https://docs.conan.io/en/2/knowledge/faq.html#error-missing-prebuilt-package'

This means that the package recipe ``zlib/1.2.11`` exists, but for some reason there is no
precompiled package for your current settings or options. Maybe the package creator didn't build and
shared pre-built packages at all and only uploaded the package recipe, or they are only
providing packages for some platforms or compilers. E.g. the package creator built
packages from the recipe for apple-clang 11, but you are using apple-clang 14.
Also you may want to check your `package ID mode` as it may
have an influence on the packages available for it.

By default, Conan doesn't build packages from sources. There are several possibilities to
overcome this error:

- You can try to build the package for your settings from sources, indicating some build
  policy as argument, like :command:`--build zlib` or :command:`--build missing`. If the
  package recipe and the source code work for your settings you will have your binaries
  built locally and ready for use.

- If building from sources fails, and you are using the `conancenter` remote, you can open
  an issue in `the Conan Center Index repository
  <https://github.com/conan-io/conan-center-index>`_


.. _`Cpplang Slack`: https://cppalliance.org/slack/
