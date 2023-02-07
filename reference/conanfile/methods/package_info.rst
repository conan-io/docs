.. _reference_conanfile_methods_package_info:

package_info()
==============

The ``package_info()`` method is the one responsible of defining the information to the consumers of the package, so those consumers can easily and automatically consume this package.
The ``generate()`` method of the consumers is the place where the information defined in the ``package_info()`` will be mapped to the specific build system of the consumer. Then, if we want a package to be consumed by different build systems (like it happens with ConanCenter recipes for the community), it is very important that this information is complete.

.. important::

    This method defines information exclusively for **consumers** of this package, not for itself. This method executes after the binary has been built and packaged.
    The information that is consumed in the build should be processed in ``generate()`` method.


Library and build information
-----------------------------

Each package has to specify certain build information for its consumers. This can be done in the ``cpp_info`` attribute.

.. code-block:: python

    # Binaries to link
    self.cpp_info.libs = []  # The libs to link against
    self.cpp_info.system_libs = []  # System libs to link against
    self.cpp_info.frameworks = []  # OSX frameworks that consumers will link against
    self.cpp_info.objects = []  # precompiled objects like .obj .o that consumers will link
    # Directories
    self.cpp_info.includedirs = ['include']  # Ordered list of include paths
    self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
    self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
    self.cpp_info.resdirs = []  # Directories where resources, data, etc. can be found
    self.cpp_info.srcdirs = []  # Directories where sources can be found (debugging, reusing sources)
    self.cpp_info.builddirs = []  # Directories where build scripts for consumers can be found
    self.cpp_info.frameworkdirs = []  # Directories where OSX frameworks can be found
    # Flags
    self.cpp_info.defines = []  # preprocessor definitions
    self.cpp_info.cflags = []  # pure C flags
    self.cpp_info.cxxflags = []  # C++ compilation flags
    self.cpp_info.sharedlinkflags = []  # linker flags
    self.cpp_info.exelinkflags = []  # linker flags
    # Properties
    self.cpp_info.set_property("property_name", "property_value")
    # Structure
    self.cpp_info.components = {} # Dictionary with the different components a package may have
    self.cpp_info.requires = None  # List of components from requirements

Binaries to link:

- **libs**: Ordered list of compiled libraries (contained in the package) the consumers should link. Empty by default.
- **system_libs**: Ordered list of system libs (not contained in the package) the consumers should link. Empty by default.
- **frameworks**: Ordered list of OSX frameworks (contained or not in the package), the consumers should link. Empty by default.
- **objects**: Ordered list of precompiled objects (.obj, .o) contained in the package the consumers should link. Empty by default

Directories:

- **includedirs**: List of relative paths (starting from the package root) of directories where headers can be found. By default it is
  initialized to ``['include']``, and it is rarely changed.
- **libdirs**: List of relative paths (starting from the package root) of directories in which to find library object binaries (\*.lib,
  \*.a, \*.so, \*.dylib). By default it is initialized to ``['lib']``, and it is rarely changed.
- **bindirs**: List of relative paths (starting from the package root) of directories in which to find library runtime binaries (like executable
  Windows .dlls). By default it is initialized to ``['bin']``, and it is rarely changed.
- **resdirs**: List of relative paths (starting from the package root) of directories in which to find resource files (images, xml, etc). By
  default it is empty.
- **srcdirs**: List of relative paths (starting from the package root) of directories in which to find sources (like
  .c, .cpp). By default it is empty. It might be used to store sources (for later debugging of packages, or to reuse those sources building
  them in other packages too).
- **builddirs**: List of relative paths (starting from package root) of directories that can contain build scripts that could be used by the consumers. Empty by default.
- **frameworkdirs**: List of relative paths (starting from the package root), of directories containing OSX frameworks. 

Flags:

- **defines**: Ordered list of preprocessor directives. It is common that the consumers have to specify some sort of defines in some cases,
  so that including the library headers matches the binaries.
- **cflags**, **cxxflags**, **sharedlinkflags**, **exelinkflags**: List of flags that the consumer should activate for proper behavior.
  Rarely used.

Properties:
- **set_property()** allows to define some built-in and user general properties to be propagated with the ``cpp_info`` model for consumers. They might contain build-system specific information. Some built-in properties are ``cmake_file_name``, ``cmake_target_name``, ``pkg_config_name``, that can define specific behavior for ``CMakeDeps`` or ``PkgConfigDeps`` generators. For more information about these, read the specific build system integration documentation.

Structure:

- **components**: Dictionary with names as keys and a component object as value to model the different components a
  package may have: libraries, executables...
- **requires**: **Experimental** List of components from the requirements this package (and its consumers) should link with. It will
  be used by generators that add support for components features.


It is common that different configurations will produce different ``package_info``, for example, the library names might change in different OSs,
or different ``system_libs`` will be used depending on the compiler and OS:

.. code-block:: python

    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}

    def package_info(self):
        if not self.settings.os == "Windows":
            self.cpp_info.libs = ["zmq-static"] if not self.options.shared else ["zmq"]
        else:
            ...

        if not self.options.shared:
            self.cpp_info.defines = ["ZMQ_STATIC"]
        if self.settings.os == "Windows" and self.settings.compiler == "msvc":
            self.cpp_info.system_libs.append("ws2_32")


Components
++++++++++
TBD


buildenv_info, runenv_info
--------------------------

The ``buildenv_info`` and ``runenv_info`` attributes are ``Environment`` objects that allow to define information for the consumers in the form of environment variables.
They can use any of the ``Environment`` methods to define such information:

.. code-block:: python

    settings = "os", "compiler", "arch", "build_type"

    def package_info(self):
        self.buildenv_info.define("MYVAR", "1")
        self.buildenv_info.prepend_path("MYPATH", "my/path")
        if self.settings.os == "Android":
            arch = "myarmarch" if self.settings.arch=="armv8" else "otherarch"
            self.buildenv_info.append("MY_ANDROID_ARCH", f"android-{arch})

        self.runenv_info.append_path("MYRUNPATH", "my/run/path")
        if self.settins.os == "Windows":
            self.runenv_info.define_path("MYPKGHOME", "my/home")


Note that these objects are not tied to either regular ``requires`` or ``tool_requires``, any package recipe can use both. The difference between ``buildenv_info`` and ``runenv_info`` is that the former is applied when Conan is building something from source, like in the ``build()`` method, while the later would be used when executing something in the "host" context that would need the runtime activated. 

Conan ``VirtualBuildEnv`` generator will be used by default in consumers, collecting the information from ``buildenv_info`` (and some ``runenv_info`` from the "build" context) to create the ``conanbuild`` environment script, which runs by default in all ``self.run(cmd, env="conanbuild")`` calls. The ``VirtualRunEnv`` generator will also be used by default in consumers collecting the ``runenv_info`` from the "host" context creating the ``conanrun`` environment script, which can be explicitly used with ``self.run(<cmd>, env="conanrun")``.


.. note:: 

    **Best practices**

    It is not necessary to add ``bindirs`` to the ``PATH`` environment variable, this will be automatically done by the consumer ``VirtualBuildEnv`` and ``VirtualRunEnv`` generators.
    Likewise, it is not necessary to add ``includedirs``, ``libdirs`` or any other dirs to environment variables, as this information will be typically managed by other generators.


conf_info
---------

``tool_requires`` packages in the "build" context can transmit some ``conf`` configuration to its immediate consumers, with the ``conf_info`` attribute. For example, one Conan
package packaging the AndroidNDK could do:

.. code-block:: python

    def package_info(self):
        self.conf_info.define_path("tools.android:ndk_path", "path/to/ndk/in/package")

``conf_info`` from packages can still be overwritten from profiles values, because user profiles will have higher priority.


.. note::

    **Best practices**

    - The ``package_info()`` method is not strictly necessary if you have other means of propagating information for consumers. For example, if your package creates ``xxx-config.cmake`` files at build time, and they are put in the final package, it might not be necessary to define ``package_info()`` at all, and in the consumer side the ``CMakeDeps`` would not be necessary either, as ``CMakeToolchain`` is able to inject the paths to locate the ``xxx-config.cmake`` files inside the packages. This approach can be good for private usage of Conan, albeit some limitations of CMake, like not being able to manage multi-configuration projects (like Visual Studio switching Debug/Release in the IDE, that ``CMakeDeps`` can provide), limitations in some cross-build scenarios using packages that are both libraries and build tools (like ``protobuf``, that also ``CMakeDeps`` can handle).
    - Providing a ``package_info()`` is very necessary if consumers can use different build systems, like in ConanCenter. In this case, it is necessary a bit of repetition, and coding the ``package_info()`` might feel duplicating the package ``xxx-config.cmake``, but automatically extracting the info from CMake is not feasible at this moment.
    - If you plan to use editables or the local development flow, there's a need to check the ``layout()`` and define the information for ``self.cpp.build`` and ``self.cpp.source``.
    - It is not necessary to add ``bindirs`` to the ``PATH`` environment variable, this will be automatically done by the consumer ``VirtualBuildEnv`` and ``VirtualRunEnv`` generators.
    - The **paths** defined in ``package_info()`` shouldn't be converted to any specific format (like the one required by Windows subsystems). Instead, it is the responsibility of the consumer to translate these paths to the adequate format.


.. seealso::
    
    See :ref:`the defining package information tutorial<tutorial_creating_define_package_info>` for more information.
