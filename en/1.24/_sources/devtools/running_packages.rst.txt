.. _running_packages:

Running and deploying packages
==============================

Executables and applications including shared libraries can also be distributed, deployed and run with Conan. This might have
some advantages compared to deploying with other systems:

- A unified development and distribution tool, for all systems and platforms.
- Manage any number of different deployment configurations in the same way you manage them for development.
- Use a Conan server remote to store all your applications and runtimes for all Operating Systems, platforms and targets.

There are different approaches:

Using virtual environments
--------------------------

We can create a package that contains an executable, for example from the default package template created by :command:`conan new`:

.. code-block:: bash

    $ conan new hello/0.1

The source code used contains an executable called ``greet``, but it is not packaged by default. Let's modify the recipe
``package()`` method to also package the executable:

.. code-block:: python

    def package(self):
        self.copy("*greet*", src="bin", dst="bin", keep_path=False)

Now we create the package as usual, but if we try to run the executable it won't be found:

.. code-block:: bash

    $ conan create . user/testing
    ...
    hello/0.1@user/testing package(): Copied 1 '.h' files: hello.h
    hello/0.1@user/testing package(): Copied 1 '.exe' files: greet.exe
    hello/0.1@user/testing package(): Copied 1 '.lib' files: hello.lib

    $ greet
    > ... not found...

By default, Conan does not modify the environment, it will just create the package in the local cache, and that is not
in the system PATH, so the ``greet`` executable is not found.

The ``virtualrunenv`` generator generates files that add the package's default binary locations to the necessary paths:

- It adds the dependencies ``lib`` subfolder to the ``DYLD_LIBRARY_PATH`` environment variable (for OSX shared libraries)
- It adds the dependencies ``lib`` subfolder to the ``LD_LIBRARY_PATH`` environment variable (for Linux shared libraries)
- It adds the dependencies ``bin`` subfolder to the ``PATH`` environment variable (for executables)

So if we install the package, specifying such ``virtualrunenv`` like:

.. code-block:: bash

    $ conan install hello/0.1@user/testing -g virtualrunenv

This will generate a few files that can be called to activate and deactivate the required environment variables

.. code-block:: bash

    $ activate_run.sh # $ source activate_run.sh in Unix/Linux
    $ greet
    > Hello World Release!
    $ deactivate_run.sh # $ source deactivate_run.sh in Unix/Linux

Imports
-------

It is possible to define a custom conanfile (either *.txt* or *.py*), with an ``imports()`` section, that can retrieve from local
cache the desired files. This approach requires a user conanfile.

For more details see the example below :ref:`runtime packages<repackage>`.

Deployable packages
-------------------

With the ``deploy()`` method, a package can specify which files and artifacts to copy to user space or to other
locations in the system. Let's modify the example recipe adding the ``deploy()`` method:

.. code-block:: python

    def deploy(self):
        self.copy("*", dst="bin", src="bin")

And run :command:`conan create`

.. code-block:: bash

    $ conan create . user/testing

With that method in our package recipe, it will copy the executable when installed directly:

.. code-block:: bash

    $ conan install hello/0.1@user/testing
    ...
    > hello/0.1@user/testing deploy(): Copied 1 '.exe' files: greet.exe
    $ bin\greet.exe
    > Hello World Release!

The deploy will create a *deploy_manifest.txt* file with the files that have been deployed.

Sometimes it is useful to adjust the package ID of the deployable package in order to deploy it regardless of the compiler it was compiled
with:

.. code-block:: python

    def package_id(self):
        del self.info.settings.compiler

.. seealso::

    Read more about the :ref:`deploy() <method_deploy>` method.

.. _deployable_deploy_generator:

Using the `deploy` generator
----------------------------

The :ref:`deploy generator <deploy_generator>` is used to have all the dependencies of an application copied into a single place. Then all
the files can be repackaged into the distribution format of choice.

For instance, if the application depends on boost, we may not know that it also requires many other 3rt-party libraries, 
such as 
`zlib <https://zlib.net/>`_, 
`bzip2 <https://sourceware.org/bzip2/>`_, 
`lzma <https://tukaani.org/xz/>`_, 
`zstd <https://facebook.github.io/zstd/>`_, 
`iconv <https://www.gnu.org/software/libiconv/>`_, etc. 

.. code-block:: bash

    $ conan install . -g deploy

This helps to collect all the dependencies into a single place, moving them out of the Conan cache.

.. _deployable_json_generator:

Using the `json` generator
--------------------------

A more advanced approach is to use the :ref:`json generator <json_generator>`. This generator works in a similar fashion as the
`deploy` one, although it doesn't copy the files to a directory. Instead, it generates a JSON file with all the information about the
dependencies including the location of the files in the Conan cache.

.. code-block:: bash

    $ conan install . -g json

The *conanbuildinfo.json* file produced, is fully machine-readable and could be used by scripts to prepare the files and recreate the
appropriate format for distribution. The following code shows how to read the library and binary directories from the *conanbuildinfo.json*:

.. code-block:: python

        import os
        import json

        data = json.load(open("conanbuildinfo.json"))

        dep_lib_dirs = dict()
        dep_bin_dirs = dict()

        for dep in data["dependencies"]:
            root = dep["rootpath"]
            lib_paths = dep["lib_paths"]
            bin_paths = dep["bin_paths"]

            for lib_path in lib_paths:
                if os.listdir(lib_path):
                    lib_dir = os.path.relpath(lib_path, root)
                    dep_lib_dirs[lib_path] = lib_dir
            for bin_path in bin_paths:
                if os.listdir(bin_path):
                    bin_dir = os.path.relpath(bin_path, root)
                    dep_bin_dirs[bin_path] = bin_dir

While with the `deploy` generator, all the files were copied into a folder. The advantage with the `json` one is that you have fine-grained
control over the files and those can be directly copied to the desired layout.

In that sense, the script above could be easily modified to apply some sort of filtering (e.g. to copy only shared libraries, 
and omit any static libraries or auxiliary files such as pkg-config .pc files).

Additionally, you could also write a simple startup script for your application with the extracted information like this:

.. code-block:: python

    executable = "MyApp"  # just an example
    varname = "$APPDIR"

    def _format_dirs(dirs):
        return ":".join(["%s/%s" % (varname, d) for d in dirs])

    path = _format_dirs(set(dep_bin_dirs.values()))
    ld_library_path = _format_dirs(set(dep_lib_dirs.values()))
    exe = varname + "/" + executable

    content = """#!/usr/bin/env bash
    set -ex
    export PATH=$PATH:{path}
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{ld_library_path}
    pushd $(dirname {exe})
    $(basename {exe})
    popd
    """.format(path=path,
           ld_library_path=ld_library_path,
           exe=exe)

Running from packages
---------------------

If a dependency has an executable that we want to run in the conanfile, it can be done directly in code
using the ``run_environment=True`` argument. It internally uses a ``RunEnvironment()`` helper.
For example, if we want to execute the :command:`greet` app while building the ``Consumer`` package:

.. code-block:: python

    from conans import ConanFile, tools, RunEnvironment

    class ConsumerConan(ConanFile):
        name = "Consumer"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        requires = "hello/0.1@user/testing"

        def build(self):
            self.run("greet", run_environment=True)

Now run :command:`conan install` and :command:`conan build` for this consumer recipe:

.. code-block:: bash

    $ conan install . && conan build .
    ...
    Project: Running build()
    Hello World Release!

Instead of using the environment, it is also possible to explicitly access the path of the dependencies:

.. code-block:: python

    def build(self):
        path = os.path.join(self.deps_cpp_info["Hello"].rootpath, "bin")
        self.run("%s/greet" % path)

Note that this might not be enough if shared libraries exist. Using the ``run_environment=True`` helper above 
is a more complete solution.

Finally, there is another approach: the package containing the executable can add its *bin* folder directly to the ``PATH``.
In this case the **Hello** package conanfile would contain:

.. code-block:: python

    def package_info(self):
        self.cpp_info.libs = ["hello"]
        self.env_info.PATH = os.path.join(self.package_folder, "bin")

We may also define ``DYLD_LIBRARY_PATH`` and ``LD_LIBRARY_PATH`` if they are required for the executable.

The consumer package is simple, as the ``PATH`` environment variable contains the ``greet`` executable:

.. code-block:: python

    def build(self):
        self.run("greet")


Read the :ref:`next section <create_installer_packages>` for a more comprenhensive explanation about using
packaged executables in your recipe methods. 


.. _repackage:

Runtime packages and re-packaging
----------------------------------

It is possible to create packages that contain only runtime binaries, getting rid of all build-time dependencies.
If we want to create a package from the above "hello" one, but only containing the executable (remember that the above
package also contains a library, and the headers), we could do:

.. code-block:: python

    from conans import ConanFile

    class HellorunConan(ConanFile):
        name = "hello_run"
        version = "0.1"
        build_requires = "hello/0.1@user/testing"
        keep_imports = True

        def imports(self):
            self.copy("greet*", src="bin", dst="bin")

        def package(self):
            self.copy("*")

This recipe has the following characteristics:

- It includes the ``hello/0.1@user/testing`` package as ``build_requires``.
  That means that it will be used to build this `hello_run` package, but once the `hello_run` package is built,
  it will not be necessary to retrieve it.
- It is using ``imports()`` to copy from the dependencies, in this case, the executable
- It is using the ``keep_imports`` attribute to define that imported artifacts during the ``build()`` step (which
  is not define, then using the default empty one), are kept and not removed after build
- The ``package()`` method packages the imported artifacts that will be created in the build folder.

To create and upload this package to a remote:

.. code-block:: bash

    $ conan create . user/testing
    $ conan upload hello_run* --all -r=my-remote

Installing and running this package can be done using any of the methods presented above. For example:

.. code-block:: bash

    $ conan install hello_run/0.1@user/testing -g virtualrunenv
    # You can specify the remote with -r=my-remote
    # It will not install hello/0.1@...
    $ activate_run.sh # $ source activate_run.sh in Unix/Linux
    $ greet
    > Hello World Release!
    $ deactivate_run.sh # $ source deactivate_run.sh in Unix/Linux

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
`newlib <https://sourceware.org/newlib/>`_ or `musl <https://www.musl-libc.org>`_, used for embedded development.

To illustrate the problem, a simple hello-world application compiled in a modern Ubuntu distribution will give the following error when it
is run in a Centos 6 one:

.. code-block:: console

    $ /hello
    /hello: /lib64/libc.so.6: version 'GLIBC_2.14' not found (required by /hello)

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
`libc++ <https://libcxx.llvm.org>`_ and `stlport <http://www.stlport.org>`_ are other well-known implementations.

Similarly to the standard C library `glibc`, running the application linked with libstdc++ in the older system may result in an error:

.. code-block:: console

    $ /hello
    /hello: /usr/lib64/libstdc++.so.6: version 'GLIBCXX_3.4.21' not found (required by /hello)
    /hello: /usr/lib64/libstdc++.so.6: version 'GLIBCXX_3.4.26' not found (required by /hello)

Fortunately, this is much easier to address by just adding ``-static-libstdc++`` compiler flag. Unlike C runtime, C++ runtime can be 
linked statically safely, because it doesn't use system calls directly, but instead relies on ``libc`` to provide required wrappers.

Compiler runtime
++++++++++++++++

Besides C and C++ runtime libraries, the compiler runtime libraries are also used by applications. Those libraries usually provide
lower-level functions, such as compiler intrinsics or support for exception handling. Functions from these runtime libraries are rarely
referenced directly in code and are mostly implicitly inserted by the compiler itself.

.. code-block:: console

    $ ldd ./a.out
    libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f6626aee000)

you can avoid this kind of dependency by the using of the ``-static-libgcc`` compiler flag. However, it's not always sane thing to do, as 
there are certain situations when applications should use shared runtime. The most common is when the application wishes to throw and catch 
exceptions across different shared libraries. Check out the `GCC manual <https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html>`_ for the 
detailed information.

System API (system calls)
+++++++++++++++++++++++++

New system calls are often introduced with new releases of `Linux kernel <https://www.kernel.org>`_. If the application, or 3rd-party
libraries, want to take advantage of these new features, they sometimes directly refer to such system calls (instead of using wrappers
provided by ``glibc``).

As a result, if the application was compiled on a machine with a newer kernel and build system used to auto-detect available system calls,
it may fail to execute properly on machines with older kernels.

The solution is to either use a build machine with lowest supported kernel, or model supported operation system (just like in case of ``glibc``). 
Check out sections :ref:`add_new_settings` and :ref:`add_new_sub_settings` to get a piece of information on how to model distribution in conan settings.
