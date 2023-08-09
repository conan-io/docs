Binary model
++++++++++++

Important attributes that define the package binaries model, which settings, options, package type, etc.
affect the final packaged binaries.


.. _reference_conanfile_attributes_package_type:

package_type
------------

Optional. Declaring the ``package_type`` will help Conan:

- To choose better the default ``package_id_mode`` for each dependency, that is, how a change
  in a dependency should affect the ``package_id`` to the current package.
- Which information from the dependencies should be propagated to the consumers, like
  headers, libraries, runtime information. See :ref:`here <reference_conanfile_package_type_trait_inferring>`
  to see what traits are propagated based on the ``package_type`` information.

The valid values are:

- **application**: The package is an application.
- **library**: The package is a generic library. It will try to determine
  the type of library (from ``shared-library``, ``static-library``, ``header-library``)
  reading the ``self.options.shared`` (if declared) and the ``self.options.header_only``
- **shared-library**: The package is a shared library.
- **static-library**: The package is a static library.
- **header-library**: The package is a header only library.
- **build-scripts**: The package only contains build scripts.
- **python-require**: The package is a python require.
- **unknown**: The type of the package is unknown.


.. _conan_conanfile_properties_settings:

settings
--------

List of strings with the first level settings (from :ref:`reference_config_files_settings_yml`) that the recipe
needs, because:
- They are read for building (e.g: `if self.settings.compiler == "gcc"`)
- They affect the ``package_id``. If a value of the declared setting changes, the ``package_id`` has to be different.

The most common is to declare:

.. code-block:: python

    settings = "os", "compiler", "build_type", "arch"

Once the recipe is loaded by Conan, the ``settings`` are processed and they can be read in the recipe, also
the sub-settings:

.. code-block:: python

    settings = "os", "arch"

    def build(self):
        if self.settings.compiler == "gcc":
            if self.settings.compiler.cppstd == "gnu20":
                # do some special build commands

If you try to access some setting that doesn't exist, like ``self.settings.compiler.libcxx``
for the ``msvc`` setting, Conan will fail telling that ``libcxx`` does not exist for that compiler.

If you want to do a safe check of settings values, you could use the ``get_safe()`` method:

.. code-block:: python

    def build(self):
        # Will be None if doesn't exist (not declared)
        arch = self.settings.get_safe("arch")
        # Will be None if doesn't exist (doesn't exist for the current compiler)
        compiler_version = self.settings.get_safe("compiler.version")
        # Will be the default version if the return is None
        build_type = self.settings.get_safe("build_type", default="Release")

The ``get_safe()`` method returns ``None`` if that setting or sub-setting doesn't
exist and there is no default value assigned.

It's also feasible to check the possible values defined in :ref:`reference_config_files_settings_yml` using the
``possible_values()`` method:

.. code-block:: python

    def generate(self):
        # Print if Android exists as OS in the whole settings.yml
        is_android = "Android" in self.settings.possible_values()["os"]
        self.output.info(f"Android in settings.yml: {is_android}")
        # Print the available versions for the compiler used by the HOST profile
        compiler_versions = self.settings.compiler.version.possible_values()
        self.output.info(f"[HOST] Versions for {str(self.settings.compiler)}:  {', '.join(compiler_versions)}")
        # Print the available versions for the compiler used by the BUILD profile
        compiler_versions = self.settings_build.compiler.version.possible_values()
        self.output.info(f"[BUILD] Versions for {str(self.settings.compiler)}:  {', '.join(compiler_versions)}")


As you can see above, doing ``self.settings.possible_values()`` returns the
whole :ref:`reference_config_files_settings_yml` as a Python dict-like object, and doing
``self.settings.compiler.version.possible_values()`` for instance returns the available versions for the compiler
used by the consumer.

If you want to do a safe deletion of settings, you could use the ``rm_safe()`` method.
For example, in the ``configure()`` method a typical pattern for a C library would be:

.. code-block:: python

    def configure(self):
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")


.. seealso::

    - :ref:`reference_config_files_settings_yml`.
    - Removing settings in the ``package_id()`` method. <MISSING PAGE>


.. _conan_conanfile_properties_options:

options
-------

Dictionary with traits that affects only the current recipe, where the key is the
option name and the value is a list of different values that the option can take.
By default any value change in an option, changes the ``package_id``. Check the
``default_options`` field to define default values for the options.

Values for each option can be typed or plain strings (``"value"``, ``True``, ``42``,...).

There are two special values:

- ``None``: Allow the option to have a ``None`` value (not specified) without erroring.
- ``"ANY"``:  For options that can take any value, not restricted to a set.

.. code-block:: python

    class MyPkg(ConanFile):
        ...
        options = {
            "shared": [True, False],
            "option1": ["value1", "value2"],
            "option2": ["ANY"],
            "option3": [None, "value1", "value2"],
            "option4": [True, False, "value"],
    }

Once the recipe is loaded by Conan, the ``options`` are processed and they can be read in the recipe. You can also
use the method ``.get_safe()`` (see :ref:`settings attribute<conan_conanfile_properties_settings>`) to avoid Conan raising an Exception if the option
doesn't exist:

.. code-block:: python

    class MyPkg(ConanFile):
        options = {"shared": [True, False]}

        def build(self):
            if self.options.shared:
                # build the shared library
            if self.options.get_safe("foo", True):
                pass

In boolean expressions, like ``if self.options.shared``:

- equals ``True`` for the values ``True``, ``"True"`` and ``"true"``, and any other value that
  would be evaluated the same way in Python code.
- equals ``False`` for the values ``False``, ``"False"`` and ``"false"``, also for the empty
  string and for ``0`` and ``"0"`` as expected.

Notice that a comparison using ``is`` is always ``False`` because the types would be different as it is encapsulated
inside a Python class.

If you want to do a safe deletion of options, you could use the ``rm_safe()`` method.
For example, in the ``config_options()`` method a typical pattern for Windows library
would be:

.. code-block:: python

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

.. seealso::

    - Read the :ref:`Getting started, creating packages<creating_packages_create_your_first_conan_package>` to know how to declare and how to
      define a value to an option.
    - Removing options in the ``package_id()`` method. <MISSING PAGE>
    - About the package_type and how it plays when a ``shared`` option is declared. <MISSING PAGE>


.. _conan_conanfile_properties_default_options:

default_options
---------------

The attribute ``default_options`` defines the default values for the options, both for the
current recipe and for any requirement.
This attribute should be defined as a python dictionary.


.. code-block:: python

    class MyPkg(ConanFile):
        ...
        requires = "zlib/1.2.8", "zwave/2.0"
        options = {"build_tests": [True, False],
                    "option2": "ANY"}
        default_options = {"build_tests": True,
                            "option1": 42,
                            "z*:shared": True}


You can also assign default values for options of your requirements using "<reference_pattern>: option_name", being
a valid ``reference_pattern`` a ``name/version`` or any pattern with ``*`` like the example above.

You can also set the options conditionally to a final value with ``configure()`` instead of using ``default_options``:

.. code-block:: python

    class OtherPkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        options = {"some_option": [True, False]}
        # Do NOT declare 'default_options', use 'config_options()'

        def configure(self):
            if self.options.some_option == None:
                if self.settings.os == 'Android':
                    self.options.some_option = True
                else:
                    self.options.some_option = False

Take into account that if a value is assigned in the ``configure()`` method it cannot be overridden.

.. seealso::

    Read more about the <MISSING PAGE>method_configure_config_options method.


options_description
-------------------

The ``options_description`` attribute is an optional attribute that can be defined in the
form of a dictionary where the key is the option name and the value is a description of
the option in text format. This attribute is useful for providing additional information
about the functionality and purpose of each option, particularly when the option is not
self-explanatory or has complex or special behavior.

The format for each dictionary entry should be:

- Key: Option name. Must be a string and must match one of the keys in the ``options`` dictionary.
- Value: Description of the option. Must be a string and can be as long as necessary.

For example:

.. code-block:: python

    class MyPkg(ConanFile):
        ...
        options = {"option1": [True, False],
                   "option2": "ANY"}

        options_description = {
            "option1": "Describe the purpose and functionality of 'option1'. ",
            "option2": "Describe the purpose and functionality of 'option2'. ",
        }

info
----

Object used exclusively in ``package_id()`` method:

- The <MISSING PAGE> ``package_id(self)`` method to control the unique ID for a package:

     .. code-block:: python

        def package_id(self):
            self.info.clear()


package_id_{embed,non_embed,unknown}_mode
-----------------------------------------

The ``package_id_embed_mode, package_id_non_embed_mode, package_id_unknown_mode`` are class attributes that can be defined in recipes to define the effect they have on their consumers ``package_id``. Can be declared as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0.0"
        package_id_embed_mode = "full_mode"
        package_id_non_embed_mode = "patch_mode"
        package_id_unknown_mode = "minor_mode"
        

Possible values are (following the semver definition of MAJOR.MINOR.PATCH):

- ``patch_mode``: New patches, minors, and major releases of the package will require a new binary (new ``package_id``) of the consumers. New recipe revisions will not require new binaries of the consumers. For example if we create a new ``pkg/1.0.1`` version and some consumer has ``requires = "pkg/[>=1.0 <2.0]"``, such a consumer will build a new binary against this specific new ``1.0.1`` version. But if we just change the recipe, producing a new ``recipe_revision``, the consumers will not require building a new binary.
- ``minor_mode``: New minor and major releases of this package will require a new binary of the consumers. New patches and new revisions will not require new binaries of the consumers. This is the default for the "non-embed-mode", as it allows fine control by the users to decide when to rebuild things or not.
- ``major_mode``: Only new major releases will require new binaries. Any other modifications and new versions will not require new binaries from the consumers.
- ``full_mode``: The full identifier of this package, including ``pkgname/version@user/channel#recipe_revision:package_id`` will be used in the consumers ``package_id``, then requiring to build a new binary of the consumer for every change of this package (as any change either in source or configuration will produce a different ``recipe_revision`` or ``package_id`` respectively). This is the default for the "embed-mode".
- ``unrelated_mode``: No change in this package will ever produce a new binary in the consumer. 

The 3 different attributes are:

- ``package_id_embed_mode``: Define the mode for "embedding" cases, that is, a shared library linking a static library, an application linking a static library, an application or a library linking a header-only library. The default for this mode is ``full_mode``
- ``package_id_non_embed_mode``. Define the mode for "non-embedding" cases, that is, a shared library linking another shared library, a static library linking another static library, an application executable linking a shared library. The default for this mode is ``minor_mode``.
- ``package_id_unknown_mode``: Define the mode when the relationship between packages is unknown. If it is not possible to deduce the package type, because there are no ``shared`` or ``header_only`` options defined, or because ``package_type`` is not defined, then, this mode will be used. The default for this mode is ``semver_mode`` (similar to Conan 1.X behavior).
