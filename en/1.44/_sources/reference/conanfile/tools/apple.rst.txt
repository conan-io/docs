.. _conan_tools_apple:

conan.tools.apple
=================

.. warning::

    These tools are **experimental** and subject to breaking changes.


XcodeDeps
---------

Available since: `1.42.0 <https://github.com/conan-io/conan/releases>`_

The ``XcodeDeps`` tool is the dependency information generator for *Xcode*. It will generate multiple
*.xcconfig* configuration files, the can be used by consumers using *xcodebuild* or *Xcode*. To use
them just add the generated configuration files to the Xcode project or set the ``-xcconfig``
argument from the command line.

The ``XcodeDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "XcodeDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    XcodeDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.apple import XcodeDeps

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "libpng/1.6.37@" # Note libpng has zlib as transitive dependency

        def generate(self):
            xcode = XcodeDeps(self)
            xcode.generate()

When the ``XcodeDeps`` generator is used, every invocation of ``conan install`` will
generate several configuration files, per dependency and configuration. For the *conanfile.py*
above, for example:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ conan install conanfile.py -s build_type=Debug

This generator is multi-configuration. It will generate different files for the different
*Debug/Release* configurations for each requirement. It will also generate one single file
(*conandeps.xcconfig*) aggregating all the files for the direct dependencies (just *libpng* in this
case). The above commands generate the following files:

.. code-block:: bash

    .
    ├── conan_libpng.xcconfig
    ├── conan_libpng_debug_x86_64.xcconfig
    ├── conan_libpng_release_x86_64.xcconfig
    ├── conan_libpng_vars_debug_x86_64.xcconfig
    ├── conan_libpng_vars_release_x86_64.xcconfig
    ├── conan_zlib.xcconfig
    ├── conan_zlib_debug_x86_64.xcconfig
    ├── conan_zlib_release_x86_64.xcconfig
    ├── conan_zlib_vars_debug_x86_64.xcconfig
    ├── conan_zlib_vars_release_x86_64.xcconfig
    └── conandeps.xcconfig


The first ``conan install`` with the default *Release* and *x86_64* configuration generates: 

- *conan_libpng_vars_release_x86_64.xcconfig*: declares some intermediate variables that are included in *conan_libpng_release_x86_64.xcconfig*
- *conan_libpng_release_x86_64.xcconfig*: includes *conan_libpng_vars_release_x86_64.xcconfig* and declares variables with conditional logic to be considered only for the active configuration in *Xcode* or the one passed by command line to *xcodebuild*.
- *conan_libpng.xcconfig*: includes *conan_libpng_release_x86_64.xcconfig* and declares the following *Xcode* build settings: ``HEADER_SEARCH_PATHS``, ``GCC_PREPROCESSOR_DEFINITIONS``, ``OTHER_CFLAGS``, ``OTHER_CPLUSPLUSFLAGS``, ``FRAMEWORK_SEARCH_PATHS``, ``LIBRARY_SEARCH_PATHS``, ``OTHER_LDFLAGS``. It also includes the generated *xcconfig* files for transitive dependencies (*conan_zlib.xcconfig* in this case).
- Same 3 files will be generated for each dependency in the graph. In this case, as *zlib* is a dependency of *libpng* it will generate: *conan_zlib_vars_release_x86_64.xcconfig*, *conan_zlib_release_x86_64.xcconfig* and *conan_zlib.xcconfig*.
- *conandeps.xcconfig*: configuration files including all direct dependencies, in this case, it just includes ``conan_libpng.xcconfig``.

The second ``conan install -s build_type=Debug`` generates: 

- *conan_libpng_vars_debug_x86_64.xcconfig*: same variables as the one below for *Debug* configuration.
- *conan_libpng_debug_x86_64.xcconfig*: same variables as the one below for *Debug* configuration.
- *conan_libpng.xcconfig*: this file has been already creted by the previous command, now it's modified to add the include for *conan_libpng_debug_x86_64.xcconfig*.
- Like in the previous command the same 3 files will be generated for each dependency in the graph. In this case, as *zlib* is a dependency of *libpng* it will generate: *conan_zlib_vars_debug_x86_64.xcconfig*, *conan_zlib_debug_x86_64.xcconfig* and *conan_zlib.xcconfig*.
- *conandeps.xcconfig*: configuration files including all direct dependencies, in this case, it just includes ``conan_libpng.xcconfig``.

If you want to add this dependencies to you Xcode project, you just have to add the
*conandeps.xcconfig* configuration file for all of the configurations you want to use (usually
*Debug* and *Release*).

Custom configurations
+++++++++++++++++++++

If your Xcode project defines custom configurations, like ``ReleaseShared``, or ``MyCustomConfig``,
it is possible to define it into the ``XcodeDeps`` generator, so different project configurations can
use different set of dependencies. Let's say that our current project can be built as a shared library,
with the custom configuration ``ReleaseShared``, and the package also controls this with the ``shared``
option:

.. code-block:: python

    from conans import ConanFile
    from conan.tools.apple import XcodeDeps

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        options = {"shared": [True, False]}
        default_options = {"shared": False}
        requires = "zlib/1.2.11"

        def generate(self):
            xcode = XcodeDeps(self)
            # We assume that -o *:shared=True is used to install all shared deps too
            if self.options.shared:
                xcode.configuration = str(self.settings.build_type) + "Shared"
            xcode.generate()

This will manage to generate new *.xcconfig* files for this custom configuration, and when you switch
to this configuration in the IDE, the build system will take the correct values depending wether we
want to link with shared or static libraries.