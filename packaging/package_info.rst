Package identifiers and information
====================================

Packages provide two types of information for consumers. The first one would be the package
identifiers (ID), which is a SHA-1 hash of the package configuration (settings, options, requirements),
that allows consumers to reuse an existing package without building it again from sources.

The other type of information would be C/C++ build information, as include paths, library names, or
compile flags


Package IDs
------------

package_id
++++++++++

Each package has two elements that affect its ID: the configuration and the ``package_id()``
recipe method. The configuration is:

- The package settings, as specified in the recipe ``settings = "os", "compiler", ...``
- The package options, as specified in the recipe ``options = {"myoption": [True, False]}`` with
  possible default values as ``default_options="myoption=True"``
- The package requirements, as defined in the package ``requires = "Pkg/0.1@user/channel"`` or in
  the ``requirements()`` method.
  
Those elements are first declared in the recipe, but it is at install time when they get specific
values (as os=Windows, compiler=gcc, etc). Once all those elements have a value, they are hashed,
and a sha1 ID is computed. This will be the package identifier. It means that all configurations
that obtain the same ID, will be compatible.

For example, a header-only library with no dependencies will have no settings, options or requirements.
Hashing such empty items will obtain always the same ID, irrespective of os, compiler, etc. That is pretty
right, the final package for a header-only is just one package for all system, containing such headers.

If you need to change in some way that package compatibility, you can provide your own ``package_id()``
method, that can change the ``self.info`` object according to your compatibility model. For example,
a ``compiler.version`` setting is needed for building the package, which will be done with gcc-4.8.
But we know that such package will be compatible for gcc-4.9 for some reason (maybe just pure C code),
so we don't want to create a different binary for gcc-4.9 but let users with that configuration consume
the package created for gcc-4.8. You could do:

.. code-block:: python

    from conans import ConanFile, CMake, tools
    from conans.model.version import Version
    
    class PkgConan(ConanFile):
        name = "Pkg"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
    
        def package_id(self):
            v = Version(str(self.settings.compiler.version))
            if self.settings.compiler == "gcc" and (v >= "4.8" and v < "5.0"):
                self.info.settings.compiler.version = "gcc4.8/9"
                
Note that object being modified is ``self.info``. Also, any string is valid, as long as it will
be the same for the settings you want it to be the same package.

Read more about this in :ref:`how_to_define_abi_compatibility`

build_id
++++++++++
The ``build_id()`` methods is an optimization. If you find that you are doing exactly the same
build for two different packages, then you might want to use this method to redefine the build ID.
The build ID, by default is the same as the package ID, i.e. there is one build folder per package.
But if for any reason you have a build system that is building different artifacts in the same
build, and you want to create different packages with those artifacts, depending on different
settings, you don't want to rebuild again the same, as it it usually time consuming.

Read more about this in :ref:`build_id`

Package information
---------------------

Single configuration
+++++++++++++++++++++

A typical approach is to have each package contain the artifacts just for one configuration. In this
approach, for example, the debug pre-compiled libraries will be in a different package than the
release pre-compiled libraries.

In this approach, the ``package_info()`` method can just set the appropriate values for consumers,
to let them know about the package library names, and necessary definitions and compile flags.

.. code-block:: python
  
   def package_info(self):
        self.cpp_info.libs = ["mylib"]
        
The values that packages declare here (the ``include``, ``lib`` and ``bin`` subfolders are already
defined by default, so they define the include and library path to the package) are translated
to variables of the respective build system by the used generators. That is, if using the ``cmake``
generator, such above definition will be translated in ``conanbuildinfo.cmake`` to something like:

.. code-block:: cmake
  
    set(CONAN_LIBS_MYPKG mylib)
    ...
    set(CONAN_LIBS mylib ${CONAN_LIBS})
    
Those variables, will be used in the ``conan_basic_setup()`` macro to actually set cmake
relevant variables.

        
Read more about this in :ref:`package_info`

Multi configuration
+++++++++++++++++++++

It is possible that someone wants to package both debug and release artifacts in the same package,
so it can be consumed from IDEs like Visual Studio changing debug/release configuration from the IDE,
and not having to specify it in the command line.

Creating a multi-configuration Debug/Release package is not difficult, using ``CMake`` for example
could be:


.. code-block:: python

    def build(self):
        cmake = CMake(self.settings)
        if cmake.is_multi_configuration:
            cmd = 'cmake "%s" %s' % (self.conanfile_directory, cmake.command_line)
            self.run(cmd)
            self.run("cmake --build . --config Debug")
            self.run("cmake --build . --config Release")
        else:
            for config in ("Debug", "Release"):
                self.output.info("Building %s" % config)
                self.run('cmake "%s" %s -DCMAKE_BUILD_TYPE=%s'
                         % (self.conanfile_directory, cmake.command_line, config))
                self.run("cmake --build .")
                shutil.rmtree("CMakeFiles")
                os.remove("CMakeCache.txt")
                
In this case, we are assuming that the binaries will be differentiated with a suffix, in cmake syntax:

.. code-block:: cmake

    set_target_properties(mylibrary PROPERTIES DEBUG_POSTFIX _d)
    

Such a package can define its information for consumers as:

.. code-block:: python

    def package_info(self):
        self.cpp_info.release.libs = ["mylibrary"]
        self.cpp_info.debug.libs = ["mylibrary_d"]
        

This will translate to the cmake variables:

.. code-block:: cmake
  
    set(CONAN_LIBS_MYPKG_DEBUG mylibrary_d)
    set(CONAN_LIBS_MYPKG_RELEASE mylibrary)
    ...
    set(CONAN_LIBS_DEBUG mylibrary_d ${CONAN_LIBS_DEBUG})
    set(CONAN_LIBS_RELEASE mylibrary ${CONAN_LIBS_RELEASE})
    
And these variables will be correctly applied to each configuration by ``conan_basic_setup()``
helper.

In this case you can still use the general, no config-specific variables. For example, the
include directory, set by default to ``include`` is still the same for both debug and release. 
Those general variables will be applied for all configurations.

Also, you can use any custom configuration you might want, they are not restricted. For example,
if your package is a multilibrary package, you could try doing something like:

.. code-block:: python

    def package_info(self):
        self.cpp_info.regex.libs = ["myregexlib1", "myregexlib2"]
        self.cpp_info.filesystem.libs = ["myfilesystemlib"]
        
These specific config variables will not be automatically applied, but you can directly use them
in your consumer CMake build script.

.. note::
 
     The automatic conversion of multi-config variables to generators is currently only implemented
     in the ``cmake`` and ``txt`` generators. If you want to have support for them in another
     build system, please open a github issue for it.



