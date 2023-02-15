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

In the ``self.conf`` attribute we can find all the conf entries declared in the <MISSING PAGE> [conf] section of the profiles.
in addition of the declared <MISSING PAGE> self.conf_info entries from the first level tool requirements.
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


.. _revision_mode_attribute:

revision_mode
-------------

This attribute allow each recipe to declare how the revision for the recipe itself should
be computed. It can take two different values:

- ``"hash"`` (by default): Conan will use the checksum hash of the recipe manifest to
  compute the revision for the recipe.
- ``"scm"``: the commit ID will be used as the recipe revision if it belongs to a known
  repository system (Git or SVN). If there is no repository it will raise an error.


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
