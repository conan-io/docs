.. _running_packages:

Running and deploying packages
================================
Executables and applications including shared libraries can also be distributed, deployed and run with Conan. This might have
some advantages compared to deploying with other systems:

- A unified development and distribution tool, for all systems and platforms
- Manage any number of different deployment configurations in the same way you manage them for development
- Use a Conan server remote to store all your applications and runtimes for all Operating Systems, platforms and targets

There are different approaches:

Using virtual environments
---------------------------

We can create a package that contains an executable, for example from the default package template created by :command:`conan new`:

.. code-block:: bash

    $ conan new Hello/0.1

The source code used contains an executable called ``greet``, but it is not packaged by default. Let's modify the recipe
``package()`` method to also package the executable:

.. code-block:: python

    def package(self):
        self.copy("*greet*", src="bin", dst="bin", keep_path=False)


Now we create the package as usual, but if we try to run the executable it won't be found:

.. code-block:: bash

    $ conan create . user/testing
    ...
    Hello/0.1@user/testing package(): Copied 1 '.h' files: hello.h
    Hello/0.1@user/testing package(): Copied 1 '.exe' files: greet.exe
    Hello/0.1@user/testing package(): Copied 1 '.lib' files: hello.lib

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

    $ conan install Hello/0.1@user/testing -g virtualrunenv

This will generate a few files that can be called to activate and deactivate the required environment variables

.. code-block:: bash

    $ activate_run.sh # $ source activate_run.sh in Unix/Linux
    $ greet
    > Hello World!
    $ deactivate_run.sh # $ source deactivate_run.sh in Unix/Linux

Imports
--------
It is possible to define a custom conanfile (either .txt or .py), with an ``imports`` section, that can retrieve from local
cache the desired files. This approach requires a user conanfile.
For more details see example below :ref:`runtime packages<repackage>`

Deployable packages
--------------------
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

    $ conan install Hello/0.1@user/testing
    ...
    > Hello/0.1@user/testing deploy(): Copied 1 '.exe' files: greet.exe
    $ bin\greet.exe
    > Hello World!

The deploy will create a *deploy_manifest.txt* file with the files that have been deployed.

Sometimes it is useful to adjust the package ID of the deployable package in order to deploy it regardless of the compiler it was compiled
with:

.. code-block:: python

    def package_id(self):
        del self.info.settings.compiler

.. seealso::

    Read more about the :ref:`deploy() <method_deploy>` method.

.. _using_deploy_generator:

Using deploy generator
----------------------

With the help of the :ref:`deploy generator <deploy_generator>`, it's possible to have all dependencies of the application to be copied into 
a single place for the later repackaging into the desired distribution format.
For instance, if the application depends on boost, we may not know that it also requires many other 3rt-party libraries, 
such as 
`zlib <https://zlib.net/>`_, 
`bzip2 <https://sourceware.org/bzip2/>`_, 
`lzma <https://tukaani.org/xz/>`_, 
`zstd <https://facebook.github.io/zstd/>`_, 
`iconv <https://www.gnu.org/software/libiconv/>`_, etc. 

.. code-block:: bash

    $ conan install . -g deploy

This helps to collect all the dependencies into a single place, moving them out of the conan cache directory.

.. _using_json_generator:

Using json generator
--------------------

A more advanced approach is to use the :ref:`json generator <json_generator>`:
file containing all required information about dependencies:

.. code-block:: bash

    $ conan install . -g json

The file produced is fully machine-readable and could be used by scripts to prepare the distribution.

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

            dep_lib_dirs = dict()
            dep_bin_dirs = dict()

            for lib_path in lib_paths:
                if os.listdir(lib_path):
                    lib_dir = os.path.relpath(lib_path, root)
                    dep_lib_dirs[lib_path] = lib_dir
            for bin_path in bin_paths:
                if os.listdir(bin_path):
                    bin_dir = os.path.relpath(bin_path, root)
                    dep_bin_dirs[bin_path] = bin_dir

Then, the information collected might be used to copy the required files into the destination:

.. code-block:: python

    from distutils.dir_util import copy_tree

    if not os.path.isdir(destination):
        os.makedirs(destination)
    for src_lib_dir, dst_bin_dir in dep_lib_dirs.items():
        copy_tree(src_lib_dir, os.path.join(destination, dst_lib_dir))
    for src_bin_dir, dst_bin_dir in dep_bin_dirs.items():
        copy_tree(src_bin_dir, os.path.join(destination, dst_bin_dir))

The advantage over the ``deploy`` generator is fine-grained control: here we copy only binaries and libraries.
It's also could be easily modified to apply some sort of filtering (e.g. to copy only shared libraries, 
and omit any static libraries or auxiliary files such as pkg-config .pc files).
The extracted information may also be used to generate a simple startup script (as described below):

.. code-block:: python

    executable = "MyApp"  # just an example
    varname = "$APPDIR"

    def _format_dirs(dirs):
        return ":".join(["%s/%s" % (varname, d) for d in dirs])

    path = _format_dirs(bin_dirs.values())
    ld_library_path = _format_dirs(bin_dirs.values())
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

.. note::

    The full example might be found on `GitHub <https://github.com/SSE4/conan-deploy-tool>`_.

.. _deployment_challenges:

Deployment challenges
---------------------

C standard library
------------------

At the very least, the application depends on C standard library. The most wide-spread variant is GNU C library or just 
`glibc <https://www.gnu.org/software/libc/>`_.
also, there are other implementations, such as 
`newlib <https://sourceware.org/newlib/>`_ or 
`musl <https://www.musl-libc.org/>`_, used in embedded environments.
Glibc is not a just C standard library, as it provides:
- C functions (e.g. malloc(), sin(), etc.) for various language standards, include C99
- POSIX functions (e.g. posix threads aka pthread)
- BSD functions (e.g. BSD sockets)
- wrappers for OS-specific APIs (e.g. Linux system calls)

even if your application doesn't use directly any of these functions, they are often used by other libraries, 
so, in practice, it's almost always in actual use.

To illustrate the problem, it's possible to compile simple hello-world application via ``conanio/gcc9`` image:

.. code-block:: text

    #include <cstring>
    #include <cstdio>
    #include <memory>

    int main(int argc, char ** argv)
    {
        const char * msg = "argv[0] = ";
        size_t size1 = strlen(msg);
        size_t size2 = strlen(argv[0]) + 1;
        char * a = new char[size1 + size2];
        memcpy(a, msg, size1);
        memcpy(a + size1, argv[0], size2);
        printf("%s\n", a);
        delete [] a;
    }

Running the compiled application on the ``centos:6`` docker image results in an error:

.. code-block:: console

    $ /hello
    /hello: /lib64/libc.so.6: version `GLIBC_2.14' not found (required by /hello)

There are several solutions to the problem:

- `LibcWrapGenerator <https://github.com/AppImage/AppImageKit/tree/stable/v1.0/LibcWrapGenerator>`_
- `glibc_version_header <https://github.com/wheybags/glibc_version_header>`_
- `bingcc <https://github.com/sulix/bingcc>`_

Some people also advice to use static of glibc, but it's strongly discouraged. One of the reasons is that newer glibc 
might be using syscalls that are not available in the previous versions, so it will randomly fail in runtime, which is 
much harder to debug (the situation about system calls is described below).

It's possible to model either ``glibc`` version or Linux distribution name in conan by defining custom conan settings (``settings.yml``), 
check out sections :ref:`add_new_settings` and :ref:`add_new_sub_settings`. The process of adopting distribution as a setting in conan:

- define new sub-setting, for instance `os.distro`, as explained in the section :ref:`add_new_sub_settings`
- define compatibility mode, as explained by sections :ref:`method_package_id` and :ref:`method_build_id` (e.g. you may consider some ``Ubuntu`` and ``Debian`` packages to be compatible with each other)
- generate N different packages for each distro
- generate deployable artifacts for each distro, as explained in section :ref:`deployment`

C++ standard library
--------------------

Usually, the default C++ standard library is `libstdc++ <https://gcc.gnu.org/onlinedocs/libstdc++/>`_, but `libc++ <https://libcxx.llvm.org/>`_ is also extremely popular. Besides that, there are other well-known implementations, e.g. `stlport <http://www.stlport.org/>`_.

Similarly to glibc, running the application linked with libstdc++ on the older system may result in an error (running on ``centos:6``):

.. code-block:: text

    #include <filesystem>
    #include <iostream>

    int main(int argc, char ** argv)
    {
        std::filesystem::path p(argv[0]);
        std::cout << "size: " << std::filesystem::file_size(p) << std::endl;
    }

.. code-block:: console

    $ /hello
    /hello: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by /hello)
    /hello: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.26' not found (required by /hello)

Fortunately, this is much easier to address (compare to glibc), by just adding ``-static-libstdc++`` compiler flag.

Compiler runtime
----------------

Besides C and C++ runtime libraries, there are compiler runtime libraries that are in use. They usually provide lower-level functions,
such as compiler intrinsics, or support for exception handling. Functions from these runtime libraries are rarely referenced directly in code,
they are mostly implicitly inserted by the compiler itself.

.. code-block:: console

    $ ldd ./a.out
    libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f6626aee000)

Anyway, it's pretty easy to avoid such dependency by the usage of the ``-static-libgcc`` compiler flag.

System API (system calls)
-------------------------

New system calls are often introduced with new releases of `Linux kernel <https://www.kernel.org/>`_. If the application, or 3rd-party libraries want to take advantage of these new features, they sometimes directly refer to such system calls, instead of using wrappers provided by ``glibc``.
As a result, if the application was compiled on a machine with a newer kernel and build system used to auto-detect available system calls, it may fail to
execute properly on machines with older kernels.

Running from packages
---------------------

If a dependency has an executable that we want to run in the conanfile, it can be done directly in code
using the ``run_environment=True`` argument. It internally uses a ``RunEnvironment`` helper. 
For example, if we want to execute the ``greet`` app while building the ``Consumer`` package:

.. code-block:: python

    from conans import ConanFile, tools, RunEnvironment

    class ConsumerConan(ConanFile):
        name = "Consumer"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        requires = "Hello/0.1@user/testing"

        def build(self):
            self.run("greet", run_environment=True)


Now run :command:`conan install` and :command:`conan build` for this consumer recipe:

.. code-block:: bash

    $ conan install . && conan build .
    ...
    Project: Running build()
    Hello World!

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


.. _repackage:

Runtime packages and re-packaging
----------------------------------
It is possible to create packages that contain only runtime binaries, getting rid of all build-time dependencies.
If we want to create a package from the above "Hello" one, but only containing the executable (remember that the above
package also contains a library, and the headers), we could do:

.. code-block:: python

    from conans import ConanFile

    class HellorunConan(ConanFile):
        name = "HelloRun"
        version = "0.1"
        build_requires = "Hello/0.1@user/testing"
        keep_imports = True

        def imports(self):
            self.copy("greet*", src="bin", dst="bin")

        def package(self):
            self.copy("*")


This recipe has the following characteristics:

- It includes the ``Hello/0.1@user/testing`` package as ``build_requires``.
  That means that it will be used to build this `HelloRun` package, but once the `HelloRun` package is built,
  it will not be necessary to retrieve it.
- It is using ``imports()`` to copy from the dependencies, in this case, the executable
- It is using the ``keep_imports`` attribute to define that imported artifacts during the ``build()`` step (which
  is not define, then using the default empty one), are kept and not removed after build
- The ``package()`` method packages the imported artifacts that will be created in the build folder.

To create and upload this package to a remote:

.. code-block:: bash

    $ conan create . user/testing
    $ conan upload HelloRun* --all -r=my-remote


Installing and running this package can be done using any of the methods presented above. For example:

.. code-block:: bash

    $ conan install HelloRun/0.1@user/testing -g virtualrunenv
    # You can specify the remote with -r=my-remote
    # It will not install Hello/0.1@...
    $ activate_run.sh # $ source activate_run.sh in Unix/Linux
    $ greet
    > Hello World!
    $ deactivate_run.sh # $ source deactivate_run.sh in Unix/Linux
