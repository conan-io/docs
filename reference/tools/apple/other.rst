.. _conan_tools_apple_fix_apple_shared_install_name:

conan.tools.apple.fix_apple_shared_install_name()
-------------------------------------------------

.. currentmodule:: conan.tools.apple

.. autofunction:: fix_apple_shared_install_name

This tool will search for all the *dylib* files in the  *conanfile.package_folder* and fix
both the ``LC_ID_DYLIB`` and ``LC_LOAD_DYLIB`` fields on those files using the
*install_name_tool* utility available in macOS.

* For ``LC_ID_DYLIB`` which is the field containing the install name of the library, it
  will change the install name to one that uses the ``@rpath``. For example, if the
  install name is ``/path/to/lib/libname.dylib``, the new install name will be
  ``@rpath/libname.dylib``. This is done by executing internally something like: 

.. code-block:: bash
  
  install_name_tool /path/to/lib/libname.dylib -id @rpath/libname.dylib

* For ``LC_LOAD_DYLIB`` which is the field containing the path to the library
  dependencies, it will change the path of the dependencies to one that uses the
  ``@rpath``. For example, if the path is ``/path/to/lib/dependency.dylib``, the new path
  will be ``@rpath/dependency.dylib``. This is done by executing internally something
  like:

.. code-block:: bash
  
  install_name_tool /path/to/lib/libname.dylib -change /path/to/lib/dependency.dylib @rpath/dependency.dylib

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
