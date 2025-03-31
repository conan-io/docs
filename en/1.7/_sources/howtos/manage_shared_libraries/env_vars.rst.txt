.. _manage_shared_libraries_env_vars:

Manage Shared Libraries with Environment Variables
==================================================

The shared libraries, are loaded at runtime. The application executable needs to know where to find the
required shared libraries when it runs.

Depending on the operating system, we can use environment variables to help the dynamic linker to find the
shared libraries:

+--------------------------------+----------------------------------------------------------------------+
| OPERATING SYSTEM               | ENVIRONMENT VARIABLE                                                 |
+================================+======================================================================+
| WINDOWS                        | PATH                                                                 |
+--------------------------------+----------------------------------------------------------------------+
| LINUX                          | LD_LIBRARY_PATH                                                      |
+--------------------------------+----------------------------------------------------------------------+
| OSX                            | DYLD_LIBRARY_PATH                                                    |
+--------------------------------+----------------------------------------------------------------------+

If your package recipe (A) is generating shared libraries you can declare the needed environment variables
pointing to the package directory. This way, any other package depending on (A) will automatically have
the right environment variable set, so they will be able to locate the (A) shared library.

Similarly if you use the :ref:`virtualenv generator<virtual_environment_generator>` and you
activate it, you will get the paths needed to locate the shared libraries in your terminal.

Example
-------

We are packaging a tool called ``toolA`` with a library and an executable that, for example, compress data.

The package offers two flavors, shared library or static library (embedded in the executable of the tool and
available to link with).
You can use the ``toolA`` package library to develop another executable or library or you can just use the
executable provided by the package. In both cases, if you choose to install the `shared` package of ``toolA``
you will need to have the shared library available.

.. code-block:: python

    import os
    from conans import tools, ConanFile

    class ToolA(ConanFile):
        ....
        name = "toolA"
        version = "1.0"
        options = {"shared": [True, False]}
        default_options = "shared=False"

        def build(self):
            # build your shared library

        def package(self):
            # Copy the executable
            self.copy(pattern="toolA*", dst="bin", keep_path=False)

            # Copy the libraries
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", keep_path=False)
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
            else:
                ...

Using the tool from a different package
---------------------------------------

If we are creating now a package that uses the ``ToolA`` executable to compress some data. You can
execute directly ``toolA`` using RunEnvironment build helper to set the environment variables accordingly:

.. code-block:: python

    import os
    from conans import tools, ConanFile

    class PackageB(ConanFile):
        name = "packageB"
        version = "1.0"
        requires = "toolA/1.0@myuser/stable"

        def build(self):
            exe_name = "toolA.exe" if self.settings.os == "Windows" else "toolA"
            self.run("%s --someparams" % exe_name, run_environment=True)
            ...

Building an application using the shared library from ``toolA``
---------------------------------------------------------------

As we are building a final application, probably we will want to distribute it together with the
shared library from the ``toolA``, so we can use the :ref:`Imports<imports_txt>` to import the required
shared libraries to our user space.

.. code-block:: python
   :caption: *conanfile.txt*

    [requires]
    toolA/1.0@myuser/stable

    [generators]
    cmake

    [options]
    toolA:shared=True

    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder
    lib, *.so* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder

Now you can build the project:

.. code-block:: bash

    $ mkdir build && cd build
    $ conan install ..
    $ cmake .. -G "Visual Studio 14 Win64"
    $ cmake --build . --config Release
    $ cd bin && mytool

The previous example will work only in Windows and OSX (changing the CMake generator), because the
dynamic linker will look in the current directory (the binary directory) where we copied the shared
libraries too.

In Linux you still need to set the ``LD_LIBRARY_PATH``, or in OSX, the ``DYLD_LIBRARY_PATH``:

.. code-block:: bash

   $ cd bin && LD_LIBRARY_PATH=$(pwd) && ./mytool

Using shared libraries from dependencies
----------------------------------------

If you are executing something that depends on shared libraries belonging to your dependencies, such shared libraries have to be found at
runtime. In Windows, it is enough if the package added its binary folder to the system ``PATH``. In Linux and OSX, it is necessary that the
``LD_LIBRARY_PATH`` and ``DYLD_LIBRARY_PATH`` environment variables are used.

Security restrictions might apply in OSX
(`read this thread <https://stackoverflow.com/questions/35568122/why-isnt-dyld-library-path-being-propagated-here>`_), so the
``DYLD_LIBRARY_PATH`` environment variable is not directly transferred to the child process. In that case, you have to use it explicitly in
your *conanfile.py*:

.. code-block:: python

    def test(self):
        # self.run('./myexe") # won't work, even if 'DYLD_LIBRARY_PATH' is in the env
        with tools.environment_append({"DYLD_LIBRARY_PATH": [self.deps_cpp_info["toolA"].lib_paths]}):
            self.run('DYLD_LIBRARY_PATH=%s ./myexe" % os.environ['DYLD_LIBRARY_PATH'])

Or you could use ``RunEnvironment`` helper described above.

Using ``virtualrunenv`` generator
---------------------------------

:ref:`virtualrunenv generator<virtual_run_environment_generator>` will set the environment variables ``PATH``, ``LD_LIBRARY_PATH``,
``DYLD_LIBRARY_PATH`` pointing to *lib* and *bin* folders automatically.

.. code-block:: python
   :caption: *conanfile.txt*

    [requires]
    toolA/1.0@myuser/stable

    [options]
    toolA:shared=True

    [generators]
    virtualrunenv

In the terminal window:

.. code-block:: bash

    $ conan install .
    $ source activate_run
    $ toolA --someparams
    # Only For Mac OS users to avoid restrictions:
    $ DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH toolA --someparams
