.. _conan_tools_apple_fix_apple_shared_install_name:

conan.tools.apple.fix_apple_shared_install_name()
-------------------------------------------------

.. currentmodule:: conan.tools.apple

.. autofunction:: fix_apple_shared_install_name

This tool will search for all the *dylib* files in the conanfile's *package_folder* and fix 
the library *install names* (the ``LC_ID_DYLIB`` header). Libraries and executables
inside the package folder will also have the ``LC_LOAD_DYLIB`` fields updated to reflect
the patched install names. Executables inside the package will also get an ``LC_RPATH`` 
entry pointing to the relative location of the libraries inside the package folder. 
This is done using the *install_name_tool* utility available in macOS, as outlined below:

* For ``LC_ID_DYLIB`` which is the field containing the install name of the library, it
  will change the install name to one that uses the ``@rpath``. For example, if the
  install name is ``/path/to/lib/libname.dylib``, the new install name will be
  ``@rpath/libname.dylib``. This is done by internally executing something like: 
  
.. code-block:: bash
  
  install_name_tool /path/to/lib/libname.dylib -id @rpath/libname.dylib

* For ``LC_LOAD_DYLIB`` which is the field containing the path to the library
  dependencies, it will change the path of the dependencies to one that uses the
  ``@rpath``. For example, if a binary has a dependency on ``/path/to/lib/dependency.dylib``, 
  this will be updated to be ``@rpath/dependency.dylib``. This is done for both libraries
  and executables inside the package folder, invoking `install_name_tool` as below:

.. code-block:: bash
  
  install_name_tool /path/to/lib/libname.dylib -change /path/to/lib/dependency.dylib @rpath/dependency.dylib

* For ``LC_RPATH``, in those cases in which the packages also contain binary executables
  that depend on libraries within the same package, entries will be added to reflect
  the location of the libraries relative to the executable. If a package has executables
  in the `bin` subfolder and libraries in the `lib` subfolder, this can be performed
  with an invocation like this:

.. code-block:: bash

  install_name_tool /path/to/bin/my_executable -add_rpath @executable_path/../lib


This tool is typically needed by recipes that use Autotools as the build system and in the
case that the correct install names are not fixed in the library being packaged. Use this
tool, if needed, in the conanfile's ``package()`` method like:

.. code-block:: python

    from conan.tools.apple import fix_apple_shared_install_name

    class HelloConan(ConanFile):

      ...

      def package(self):
          autotools = Autotools(self)
          autotools.install()
          fix_apple_shared_install_name(self)

.. _conan_tools_apple_is_apple_os:

conan.tools.apple.is_apple_os()
-------------------------------

.. currentmodule:: conan.tools.apple

.. autofunction:: is_apple_os

.. _conan_tools_apple_to_apple_arch:

conan.tools.apple.to_apple_arch()
---------------------------------

.. currentmodule:: conan.tools.apple

.. autofunction:: to_apple_arch

.. _conan_tools_apple_XCRun:

conan.tools.apple.XCRun()
-------------------------

.. currentmodule:: conan.tools.apple

.. autoclass:: XCRun
    :members:
