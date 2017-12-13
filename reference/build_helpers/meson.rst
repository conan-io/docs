.. _meson_build_helper_reference:


Meson
=====


.. code-block:: python

   from conans import ConanFile, Meson

   class ExampleConan(ConanFile):
       ...


       def build(self):
           meson = Meson(self)
           meson.configure(cache_build_dir="build")
           meson.build()



Methods
-------

- **constructor** (conanfile, backend=None, build_type=None)

    - **conanfile**: Use ``self``.
    - **backend**: Specify a backend to be used, otherwise it will use "Ninja".
    - **build_type**: Force to use a build type, ignoring the read from the settings.

- **configure** (args=None, defs=None, source_dir=None, build_dir=None, pkg_config_paths=None)

    - **args**: A list of additional arguments to be passed to the ``configure`` script. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **defs**: A list of definitions
    - **source_dir**: Default conanfile.source_folder.
    - **build_dir**: Default conanfile.build_folder
    - **cache_build_dir**: Use the given subfolder as build folder when building the package in the local cache.
      This argument doesn't have effect when the package is being built in user folder with ``conan build`` but overrides **build_dir** when working in the local cache.
      See :ref:`self.in_local_cache<in_local_cache>`.
    - **pkg_config_paths**: A list containing paths to locate the pkg-config files (\*.pc). Default conanfile.build_folder.

- **build** (args=None, build_dir=None, targets=None)

    - **args**: A list of additional arguments to be passed to the ``make`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build_dir**: Default conanfile.build_folder
    - **targets**: A list of targets to be built.
