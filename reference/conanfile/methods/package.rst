.. _reference_conanfile_methods_package:

package()
=========

The ``package()`` method is in charge of copying files from the ``source_folder`` and the temporary ``build_folder`` to the ``package_folder``, copying only those files and artifacts that will be part of the final package, like headers, compiler static and shared libraries, executables, license files, etc.

The ``package()`` method will be called once per different configuration that is creating a new package binary, which happens with ``conan install --build=pkg*``, ``conan create`` and ``conan export-pkg`` commands.

There are 2 main ways the ``package()`` method can do such a copy. The first one is an explicit ``copy()`` from the origin ``source_folder`` and ``build_folder`` to the ``package folder``:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import copy

    class Pkg(ConanFile):

        def package(self):
            # copying headers from source_folder
            copy(self, "*.h", join(self.source_folder, "include"), join(self.package_folder, "include"))
            # copying compiled .lib from build folder
            copy(self, "*.lib", self.build_folder, join(self.package_folder, "lib"), keep_path=False)

The second way is to use the ``install`` functionality of some build systems, provided that the build scripts implement such functionality. For example if the ``CMakeLists.txt`` of a package implements the correct CMake ``INSTALL`` instructions, it is possible to do:

.. code-block:: python

    def package(self):
        cmake = CMake(self)
        cmake.install()

Also, it is possible to combine both approaches, doing ``cmake.install()`` and also adding some ``copy()`` calls, for example to make sure some "License.txt" file is packaged that was not taken into account by the CMakeLists.txt script.

It is also possible to use conditionals in the ``package()`` method,
because different platforms might have different artifacts in different locations:

.. code-block:: python

    def package(self):
        if self.settings.os == "Windows":
            copy(self, "*.lib", src=os.path.join(self.build_folder, "libs"), ...)
            copy(self, "*.dll", ....)
        else:
            copy(self, "*.lib", src=os.path.join(self.build_folder, "build", "libs"), ...)

Though in most situations it might not be necessary, because pattern based copy will likely not find wrong artifacts like ``*.dll`` in a non-Windows build.

The ``package()`` method is also the one called when packaging precompiled binaries with ``conan export-pkg``. In this case the ``self.source_folder`` and ``self.build_folder`` refer to user space folders, as defined by the ``layout()`` method and the only folder in the Conan cache will be ``self.package_folder``.

.. note::

    **Best practices**

    The ``cmake.install()`` functionality should be called in the ``package()`` method, not in the ``build()`` method. It is not necessary to reuse the ``CMake(self)`` object, it shouldn't be reused among methods. Creating a new instance in every method is the recommended approach.


.. seealso::
    
    See :ref:` the package() method tutorial<creating_packages_package_method>` for more information.
