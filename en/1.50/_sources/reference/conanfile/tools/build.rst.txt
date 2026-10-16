.. _conan_tools_build:

conan.tools.build
=================

conan.tools.build.cross_building()
----------------------------------

.. code-block:: python

    def cross_building(conanfile=None, skip_x64_x86=False):


Check it we are cross building comparing the *build* and *host* settings. Returns ``True``
in the case that we are cross-building.

Parameters:

- **conanfile**: Conanfile object, use always ``self``.
- **skip_x64_x86**: Will not consider the as cross-building the case of building in 64 bit
  architecture for 32 bit architecture, like ``build_arch=x86_64`` and ``host_arch=x86``
  for example.


conan.tools.build.can_run()
---------------------------

.. code-block:: python

    def can_run(conanfile):


Validates whether is possible to run a non-native app on the same architecture.
It returns the configuration value for ``tools.build.cross_building:can_run`` if exists, otherwise, it returns ``False`` if we are cross-building, else, ``True``.

It's an useful feature for the case your architecture can run more than one target. For instance, Mac M1 machines can run both ``armv8`` and ``x86_64``.

Parameters:

- **conanfile**: Conanfile object, use always ``self``.


conan.tools.build.check_min_cppstd
----------------------------------


.. code-block:: python

    def check_min_cppstd(conanfile, cppstd, gnu_extensions=False)


Check if provided ``conanfile.settings.compiler.cppstd`` fits the minimal version required (specified in the argument ``cppstd``).
In case it doesn't, a ``ConanInvalidConfiguration`` exception will be raised.

Parameters:

- **conanfile**: The current recipe object. Always use ``self``.
- **cppstd**: Minimal cppstd version required.
- **gnu_extensions**: GNU extension is required (e.g gnu17).


conan.tools.build.default_cppstd
----------------------------------

.. code-block:: python

    def default_cppstd(conanfile, compiler=None, compiler_version=None):



Get the default ``compiler.cppstd`` for the "conanfile.settings.compiler" and "conanfile
settings.compiler_version" or for the parameters "compiler" and "compiler_version" if specified.
Returns the default ``compiler.cppstd`` for the specified compiler.

Parameters:

- **conanfile**: The current recipe object. Always use ``self``.
- **compiler**: Name of the compiler e.g. gcc
- **compiler_version**: Version of the compiler e.g. 12


conan.tools.build.supported_cppstd
----------------------------------

.. code-block:: python

    def supported_cppstd(conanfile, compiler=None, compiler_version=None):



Get the a list of supported ``compiler.cppstd`` for the "conanfile.settings.compiler" and
"conanfile.settings.compiler_version" or for the parameters "compiler" and "compiler_version"
if specified. Returns a list of supported ``cppstd`` values.


Parameters:

- **conanfile**: The current recipe object. Always use ``self``.
- **compiler**: Name of the compiler e.g: gcc
- **compiler_version**: Version of the compiler e.g: 12
