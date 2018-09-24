.. _plugins:

Plugins
=======

The Conan plugins is a feature intended to extend the Conan functionalities and let users customize the client behavior at determined
points.

Plugin structure
----------------

Plugins are Python files containing **pre** and **post** functions that will be executed prior and after a determined task performed by the
Conan client. Those tasks could be Conan commands, recipe interactions such as exporting or packaging or interactions with the remotes.

Here you can see an example of a simple plugin:

.. code-block:: python
   :caption: *example_plugin.py*

    from conans import tools


    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        conanfile_content = tools.load(conanfile_path)
        test = "[RECIPE METADATA]"
        metadata_error = False
        for field in ["url", "license", "description"]:
            field_value = getattr(conanfile, field, None)
            if not field_value:
                metadata_error = True
                output.error("%s Conanfile doesn't have '%s'. It is recommended to add it as attribute"
                            % (test, field))

    def pre_source(output, conanfile, conanfile_path, **kwargs):
        conanfile_content = tools.load(conanfile_path)
        if "def source(self):" in conanfile_content:
            test = "[INMUTABLE SOURCES]"
            valid_content = [".zip", ".tar", ".tgz", ".tbz2", ".txz"]
            invalid_content = ["git checkout master", "git checkout devel", "git chekcout develop"]
            if "git clone" in conanfile_content and "git checkout" in conanfile_content:
                fixed_sources = True
                for invalid in invalid_content:
                    if invalid in conanfile_content:
                        fixed_sources = False
            else:
                fixed_sources = False
                for valid in valid_content:
                    if valid in conanfile_content:
                        fixed_sources = True

            if not fixed_sources:
                output.error("%s Source files does not come from and inmutable place. Checkout to a "
                            "commit/tag or download a compressed source file" % test)

This plugin is only checking the recipe content prior to the recipe being exported and prior to downloadin the sources. Basically the
``pre_export()`` function is checking the attributes of the ``conanfile`` object to see if there is an URL, a license and a description and
warning the user with a message through the ``output``. This is done **before** the recipe is exported to the local cache.

The ``pre_source()`` function checks if the recipe contains a ``source()`` method (this time it is using the conanfile content instead of
the ``conanfile`` object) and in that case it checks if the download of the sources are likely coming from inmutable places (a compressed
file or a determined :command:`git checkout`). This is done **before** the **source()** method of the recipe is called.

Any kind of Python scripting can be executed. You can create global functions and called them from different plugin functions, import them
from a relative module and warn, error or even raise to block the Conan client execution.

As you can see each function receives some parameters but not all of them are available for all functions as this may change depending on
the context of the commands being executed such as the recipe being in the local cache or not.

.. important::

    A detailed description of the functions allowed and its parameters as well as their execution can be found in it dedicated reference
    section: :ref:`plugins_reference`.

Other useful task where a plugin may come handy are the upload and download actions. There are **pre** and **post** functions for every
donwload/upload as a whole and for fine download task such as recipe and package downloads/uploads.

For example they can be used to sign the packages before being uploaded and checking that signature when they are donwloaded.

.. code-block:: python
   :caption: *signing_plugin.py*

    from conans import tools


    def pre_upload_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

    def post_download_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

Official Plugins
----------------

There are two official plugins ready to be used in Conan. You could take as an starting point to create your own ones.

attribute_checker
+++++++++++++++++

The first one is the *attribute_checker.py* plugin that it is shipped with the Conan client. It has the functionality of warning when
recipes do not contain some metada attributes.

.. code-block:: python
   :caption: *attribute_checker.py*

    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        # Check basic meta-data
        for field in ["url", "license", "description"]:
            field_value = getattr(conanfile, field, None)
            if not field_value:
                output.warn("Conanfile doesn't have '%s'. It is recommended to add it as attribute"
                            % field)

This plugin comes activated by default.

Conan Center plugin
+++++++++++++++++++

This plugin has been created to perform some the checks that the Conan team make as part of the process of accepting a new library into the
Conan Center central respository in Bintray (LINK).

This plugin is not shipped with the Conan plugin but stored in a repository to improve it separeted from the Conan source code.

The plugin performs various checks during development (LINK) of a package and also during the creation and it has been designed to not
block the Conan client execution and only printing error traces.

.. info::

    Conan Center plugin GitHub repository: (LINK)

It has been preliminary tested with some recipes but will require some iterations for it to be mature. However, it is a good plugin to use
for anyone willing to :ref:`include their recipe into Conan Center<conan_center_flow>`.
