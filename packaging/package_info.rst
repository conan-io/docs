Packaging approaches
=====================

Package recipes have three methods to control the packages binary compatibility and to implement different packaging approaches: ``package_id()``, ``build_id()`` and ``package_info()``

Package binary compatibility
-----------------------------

Each package binary has an identifier (ID) which is a SHA1 hash of the package configuration (settings, options, requirements), that allows consumers to reuse an existing package without building it again from sources.

The elements that define the package ID are the package configuration and the ``package_id()`` recipe method. The package configuration is:

- The package settings, as specified in the recipe ``settings = "os", "compiler", ...``
- The package options, as specified in the recipe ``options = {"myoption": [True, False]}`` with possible default values as ``default_options="myoption=True"``
- The package requirements, as defined in the package ``requires = "Pkg/0.1@user/channel"`` or in the ``requirements()`` method.
  
Those elements are first declared in the recipe, but it is at install time when they get specific
values (as "os=Windows", "compiler=gcc", etc). Once all those elements have a value, they are hashed,
and a SHA1 ID is computed. This will be the package identifier. It means that all configurations
that obtain the same ID, will be be binary compatible.

For example, a header-only library with no dependencies will have no settings, options or requirements.
Hashing such empty items will always obtain the same ID, irrespective of os, compiler, etc. That is pretty
right, the final package for a header-only is just one package for all configurations, containing such headers.

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
                
Note that the object being modified is called ``self.info``, not ``self.settings``. Also, any string is valid, as long as it will be the same for the settings you want it to be the same package.

Read more about this in :ref:`how_to_define_abi_compatibility`


Single configuration packages
--------------------------------

A typical approach is to have each package contain the artifacts just for one configuration. In this
approach, for example, the debug pre-compiled libraries will be in a different package than the
release pre-compiled libraries.

So if there is a package recipe that builds a “hello” library, there will be one package containing the release version of the "hello.lib" library and a different package containing a debug version of that library (in the figure denoted as "hello_d.lib", to make it clear, it is not necessary to use different names). 

.. image:: /images/single_conf_packages.png
    :height: 300 px
    :width: 400 px
    :align: center


In this approach, the ``package_info()`` method can just set the appropriate values for consumers,
to let them know about the package library names, and necessary definitions and compile flags.

.. code-block:: python
  
    class HelloConan(ConanFile):

        settings = "os", "compiler", "build_type", "arch"
        
        def package_info(self):
            self.cpp_info.libs = ["mylib"]


It is very important to note that it is declaring the ``build_type`` as a setting. This means that a different package will be generated for each different value of such setting.

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

If the developer wants to switch configuration of the dependencies, he will usually switch with:

.. code-block:: bash

    $ conan install -s build_type=Release ... 
    // when need to debug
    $ conan install -s build_type=Debug ... 

These switches will be fast, since all the dependencies are already cached locally.

This process has some advantages: it is quite easy to implement and maintain. The packages are of minimal size, so disk space and transfers are faster, and builds from sources are also kept to the necessary minimum. The decoupling of configurations might help with isolating issues related to mixing different types of artifacts, and also protecting valuable information from deploy and distribution mistakes. For example, debug artifacts might contain symbols or source code, which could help or directly provide means for reverse engineering. So distributing debug artifacts by artifacts could be a very risky issue. 

Read more about this in :ref:`package_info`


Multi configuration packages
--------------------------------

It is possible that someone wants to package both debug and release artifacts in the same package,
so it can be consumed from IDEs like Visual Studio changing debug/release configuration from the IDE,
and not having to specify it in the command line. This type of package will include different artifacts for different configurations, like both the release and debug version of the "hello" library, in the same package.

.. image:: /images/multi_conf_packages.png
    :height: 300 px
    :width: 400 px
    :align: center

.. note::

    A complete working example of the following code can be found in a github repo. You should be able to run:

    .. code:: bash

        $ git clone https://github.com/memsharded/hello_multi_config
        $ cd hello_multi_config
        $ conan test_package -s build_type=Release
        $ conan test_package -s build_type=Debug --build=missing



Creating a multi-configuration Debug/Release package is not difficult, using ``CMake`` for example
could be:


.. code-block:: python

    def build(self):
        cmake = CMake(self)
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


Build once, package many
--------------------------

It’s possible that an already existing build script is building binaries for different configurations at once, like debug/release, or different architectures (32/64bits), or library types (shared/static). If such build script is used in the previous “Single configuration packages” approach, it will definitely work without problems, but we’ll be wasting precious build time, as we’ll be re-building the whole project for each package, then extracting the relevant artifacts for the given configuration, leaving the others.

It is possible to specify the logic, so the same build can be reused to create different packages, which will be more efficient:

.. image:: /images/build_once.png
    :height: 300 px
    :width: 400 px
    :align: center


This can be done by defining a build_id() method in the package recipe that will specify the logic.

.. code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def build_id(self):
        self.info_build.settings.build_type = "Any"

    def package(self):
        if self.settings.build_type == "Debug":
            #package debug artifacts
        else: 
            # package release

Note that the ``build_id()`` method uses the ``self.info_build`` object to alter the build hash. If the method doesn’t change it, the hash will match the package folder one. By setting ``build_type="Any"``, we are forcing that for both Debug and Release values of ``build_type``, the hash will be the same (the particular string is mostly irrelevant, as long as it is the same for both configurations). Note that the build hash ``sha3`` will be different of both ``sha1`` and ``sha2`` package identifiers.

This doesn’t imply that there will be strictly one build folder. There will be a build folder for every configuration (architecture, compiler version, etc). So if we just have Debug/Release build types, and we’re producing N packages for N different configurations, we’ll have N/2 build folders, saving half of the build time.


Read more about this in :ref:`build_id`
