.. _integration_deployment:

Deployment
==========

If you have a project with all the dependencies managed by Conan and you want to deploy into a specific format, the process is the
following:

  - Extract the needed artifacts to a local directory either using the :ref:`deploy generator <deployable_deploy_generator>` or the
    :ref:`json generator <deployable_json_generator>`.
  - Convert the artifacts (typically executables, shared libraries and assets) to a different deploy format. You will find the specific steps
    for some of the most common deploy technologies below.

.. toctree::
   :maxdepth: 2

   deployment/system_package_manager
   deployment/makeself
   deployment/appimage
   deployment/snap
   deployment/flatpak

.. _deployment_challenges:

Deployment challenges
*********************

When deploying a C/C++ application there are some specific challenges that have to be solved when distributing your application. Here you
will find the most usual ones and some recommendations to overcome them.

The C standard library
++++++++++++++++++++++

A common challenge for all the applications no matter if they are written in pure C or in C++ is the dependency on C standard library. The
most wide-spread variant of this library is GNU C library or just `glibc <https://www.gnu.org/software/libc/>`_.

Glibc is not a just C standard library, as it provides:

- C functions (like ``malloc()``, ``sin()``, etc.) for various language standards, including C99.
- POSIX functions (like posix threads in the ``pthread`` library).
- BSD functions (like BSD sockets).
- Wrappers for OS-specific APIs (like Linux system calls)

Even if your application doesn't use directly any of these functions, they are often used by other libraries, 
so, in practice, it's almost always in actual use.

There are other implementations of the C standard library that present the same challenge, such as
`newlib <https://sourceware.org/newlib/>`_ or `musl <https://www.musl-libc.org/>`_, used for embedded development.

To illustrate the problem, a simple hello-world application compiled in a modern Ubuntu distribution will give the following error when it
is run in a Centos 6 one:

.. code-block:: console

    $ /hello
    /hello: /lib64/libc.so.6: version `GLIBC_2.14' not found (required by /hello)

This is because the versions of the ``glibc`` are different between those Linux distributions.

There are several solutions to this problem:

- `LibcWrapGenerator <https://github.com/AppImage/AppImageKit/tree/stable/v1.0/LibcWrapGenerator>`_
- `glibc_version_header <https://github.com/wheybags/glibc_version_header>`_
- `bingcc <https://github.com/sulix/bingcc>`_

Some people also advice to use static of glibc, but it's strongly discouraged. One of the reasons is that newer glibc  might be using
syscalls that are not available in the previous versions, so it will randomly fail in runtime, which is much harder to debug (the situation
about system calls is described below).

It's possible to model either ``glibc`` version or Linux distribution name in Conan by defining custom Conan sub-setting in the
*settings.yml* file (check out sections :ref:`add_new_settings` and :ref:`add_new_sub_settings`). The process will be similar to:

- Define new sub-setting, for instance `os.distro`, as explained in the section :ref:`add_new_sub_settings`.
- Define compatibility mode, as explained by sections :ref:`method_package_id` and :ref:`method_build_id` (e.g. you may consider some ``Ubuntu`` and ``Debian`` packages to be compatible with each other)
- Generate different packages for each distribution.
- Generate deployable artifacts for each distribution.

C++ standard library
++++++++++++++++++++

Usually, the default C++ standard library is `libstdc++ <https://gcc.gnu.org/onlinedocs/libstdc++/>`_, but
`libc++ <https://libcxx.llvm.org/>`_ and `stlport <http://www.stlport.org/>`_ are other well-known implementations.

Similarly to the standard C library `glibc`, running the application linked with libstdc++ in the older system may result in an error:

.. code-block:: console

    $ /hello
    /hello: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by /hello)
    /hello: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.26' not found (required by /hello)

Fortunately, this is much easier to address by just adding ``-static-libstdc++`` compiler flag.

Compiler runtime
++++++++++++++++

Besides C and C++ runtime libraries, the compiler runtime libraries are also used by applications. Those libraries usually provide
lower-level functions, such as compiler intrinsics or support for exception handling. Functions from these runtime libraries are rarely
referenced directly in code and are mostly implicitly inserted by the compiler itself.

.. code-block:: console

    $ ldd ./a.out
    libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f6626aee000)

you can avoid this kind of dependency by the using of the ``-static-libgcc`` compiler flag.

System API (system calls)
+++++++++++++++++++++++++

New system calls are often introduced with new releases of `Linux kernel <https://www.kernel.org/>`_. If the application, or 3rd-party
libraries, want to take advantage of these new features, they sometimes directly refer to such system calls (instead of using wrappers
provided by ``glibc``).

As a result, if the application was compiled on a machine with a newer kernel and build system used to auto-detect available system calls,
it may fail to execute properly on machines with older kernels.
