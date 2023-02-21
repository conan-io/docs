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
  headers, libraries, runtime information...

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

List of strings with the first level settings (from ``settings.yml``) that the recipe
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

The ``get_safe()`` method will return ``None`` if that setting or sub-setting doesn't
exist and there is no default value assigned.

If you want to do a safe deletion of settings, you could use the ``rm_safe()`` method.
For example, in the ``configure()`` method a typical pattern for a C library would be:

.. code-block:: python

    def configure(self):
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

.. seealso::

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
                            "z*: shared": True}


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

TODO: Complete, https://github.com/conan-io/conan/pull/11295


info
----

Object used exclusively in ``package_id()`` method:

- The <MISSING PAGE> ``package_id(self)`` method to control the unique ID for a package:

     .. code-block:: python

        def package_id(self):
            self.info.clear()