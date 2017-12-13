.. _meson_build_helper_reference:


Meson
=====


.. code-block:: python

   from conans import ConanFile, Meson

   class ExampleConan(ConanFile):
       ...


       def build(self):
           meson = Meson(self)
           meson.configure()
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
    - **pkg_config_paths**: A list containing paths to locate the pkg-config files (\*.pc). Default conanfile.build_folder.

- **build** (args=None, build_dir=None, targets=None)

    - **args**: A list of additional arguments to be passed to the ``make`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build_dir**: Default conanfile.build_folder
    - **targets**: A list of targets to be built.
