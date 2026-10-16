.. spelling::

  ing
  ver

.. _conan_conanfile_attributes:

Attributes
==========

.. contents::
    :local:

.. include:: ./attributes/references.inc
.. include:: ./attributes/metadata.inc
.. include:: ./attributes/requirements.inc
.. include:: ./attributes/sources.inc
.. include:: ./attributes/binary_model.inc
.. include:: ./attributes/build.inc
.. include:: ./attributes/folders.inc
.. include:: ./attributes/layout.inc
.. include:: ./attributes/consumers.inc



Other
+++++

dependencies
------------

Conan recipes provide access to their dependencies via the ``self.dependencies`` attribute.


.. code-block:: python

    class Pkg(ConanFile):
        requires = "openssl/0.1"

        def generate(self):
            openssl = self.dependencies["openssl"]
            # access to members
            openssl.ref.version
            openssl.ref.revision # recipe revision
            openssl.options
            openssl.settings

.. seealso::

    Read here :ref:`the complete reference of self.dependencies <conan_conanfile_model_dependencies>`.


conf
----

In the ``self.conf`` attribute we can find all the conf entries declared in the :ref:`[conf]<reference_config_files_profiles_conf>`  section of the profiles.
in addition of the declared :ref:`self.conf_info<conan_conanfile_model_conf_info>` entries from the first level tool requirements.
The profile entries have priority.


.. code-block:: python

    from conan import ConanFile

    class MyConsumer(ConanFile):

      tool_requires = "my_android_ndk/1.0"

      def generate(self):
          # This is declared in the tool_requires
          self.output.info("NDK host: %s" % self.conf.get("tools.android:ndk_path"))
          # This is declared in the profile at [conf] section
          self.output.info("Custom var1: %s" % self.conf.get("user.custom.var1"))


.. note::

    The ``conf`` attribute is a **read-only** attribute. It can only be defined in profiles and command lines, but it should never be set by recipes.
    Recipes can only read its value via ``self.conf.get()`` method.


Output
------

.. _conanfile_output_attribute:

Output contents
---------------

Use the ``self.output`` to print contents to the output.

..  code-block:: python

   self.output.success("This is good, should be green")
   self.output.info("This is neutral, should be white")
   self.output.warning("This is a warning, should be yellow")
   self.output.error("Error, should be red")

Additional output methods are available and you can produce different outputs with different colors.
See :ref:`the output documentation<reference_conanfile_output>` for the list of available output methods.


.. _revision_mode_attribute:

revision_mode
-------------

This attribute allow each recipe to declare how the revision for the recipe itself should
be computed. It can take three different values:

- ``"hash"`` (by default): Conan will use the checksum hash of the recipe manifest to
  compute the revision for the recipe.
- ``"scm"``: if the project is inside a Git repository the commit ID will be used as the
  recipe revision. If there is no repository it will raise an error.
- ``"scm_folder"``: This configuration applies when you have a mono-repository project, but
  still want to use *scm* revisions. In this scenario, the revision of the exported
  `conanfile.py` will correspond to the commit ID of the folder where it's located. This
  approach allows multiple `conanfile.py` files to exist within the same Git repository,
  with each file exported under its distinct revision.

When ``scm`` or ``scm_folder`` is selected, the Git commit will be used, but by default
the repository must be clean, otherwise it would be very likely that there are uncommitted
changes and the build wouldn't be reproducible. So if there are dirty files, Conan will raise
an error. If there are files that can be dirty in the repo, but do not belong at all to the
recipe or the package, then it is possible to exclude them from the check with the ``core.scm:excluded``
configuration, which is a list of patterns (fnmatch) to exclude.



upload_policy
-------------

Controls when the current package built binaries are uploaded or not
    
- ``"skip"``: The precompiled binaries are not uploaded. This is useful for "installer"
  packages that just download and unzip something heavy (e.g. android-ndk), and is useful
  together with the ``build_policy = "missing"``

    .. code-block:: python
        :emphasize-lines: 2

        class Pkg(ConanFile):
            upload_policy = "skip"


required_conan_version
----------------------

Recipes can define a module level ``required_conan_version`` that defines a valid version range of
Conan versions that can load and understand the current ``conanfile.py``. The syntax is:

.. code-block:: python
    
    from conan import ConanFile
    
    required_conan_version = ">=2.0"
    
    class Pkg(ConanFile):
        pass

Version ranges as in ``requires`` are allowed. 
Also there is a ``global.conf`` file ``core:required_conan_version`` configuration that can
define a global minimum, maximum or exact Conan version to run, which can be very convenient
to maintain teams of developers and CI machines to use the desired range of versions.

.. _conan_conanfile_attributes_implements:

implements
----------

A list is used to define a series of option configurations that Conan will handle
automatically. This is especially handy for avoiding boilerplate code that tends to repeat
in most of the recipes. The syntax is as follows:

.. code-block:: python
    
    from conan import ConanFile
        
    class Pkg(ConanFile):
        implements = ["auto_shared_fpic", "auto_header_only", ...]


Currently these are the automatic implementations provided by Conan:

- ``"auto_shared_fpic"``: automatically manages ``fPIC`` and ``shared`` options. Adding this
  implementation will have both effect in the
  :ref:`configure<reference_conanfile_methods_configure_implementations>` and
  :ref:`config_options<reference_conanfile_methods_config_options_implementations>` steps
  when those methods are not explicitly defined in the recipe.

- ``"auto_header_only"``: automatically manages the package ID clearing settings. Adding this
  implementation will have effect in the
  :ref:`package_id<reference_conanfile_methods_package_id_implementations>` step
  when the method is not explicitly defined in the recipe.

.. warning::

    This is a 2.0-only feature, and it will not work in 1.X


alias
-----

.. warning::
    
    While aliases can technically still be used in Conan 2, their usage is not recommended
    and they may be fully removed in future releases. Users are encouraged to adapt to the
    :ref:`newer versioning features<devops_versioning>` for a more standardized and efficient
    package management experience. 

In Conan 2, the `alias` attribute remains a part of the recipe, allowing users to define
an alias for a package version. Normally, you would create one using the ``conan new``
command with the ``alias`` template and the exporting the recipe with conan export:

.. code-block:: shell

    $ conan new alias -d name=mypkg -d version=latest -d target=1.0 
    $ conan export .

Note that when requiring the alias, you must place the version in parentheses ``()`` to
explicitly declare the use of an alias as a requirement:

.. code-block:: python

    class Consumer(ConanFile):
    
        ... 
        requires = "mypkg/(latest)" 
        ...


.. _conan_conanfile_attributes_extension_properties:

extension_properties
--------------------

The ``extensions_properties`` attribute is a dictionary intended to define and pass information from the
recipes to the Conan extensions.

At the moment, the only defined properties are ``compatibility_cppstd`` and ``compatibility_cstd``, that allows disabling the behavior
of :ref:`the default compatibility.py extension <reference_extensions_binary_compatibility>`, that considers 
binaries built with different ``compiler.cppstd`` and ``compiler.cstd`` values ABI-compatible among them. 
To disable this behavior for the current package, it is possible to do it with:

.. code-block:: python

  class Pkg(ConanFile):
      extension_properties = {"compatibility_cppstd": False}

If it is necessary to do it conditionally, it is also possible to define its value inside recipe ``compatibility()``
method:

.. code-block:: python

  class Pkg(ConanFile):

      def compatibility(self):
          self.extension_properties = {"compatibility_cppstd": False}
