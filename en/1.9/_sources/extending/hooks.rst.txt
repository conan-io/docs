.. _hooks:

Hooks [EXPERIMENTAL]
======================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The Conan hooks is a feature intended to extend the Conan functionalities and let users customize the client behavior at determined
points.

Hook structure
----------------

Hooks are Python files containing **pre** and **post** functions that will be executed prior and after a determined task performed by the
Conan client. Those tasks could be Conan commands, recipe interactions such as exporting or packaging or interactions with the remotes.

Here you can see an example of a simple hook:

.. code-block:: python
   :caption: *example_hook.py*

    from conans import tools


    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        test = "%s/%s" % (reference.name, reference.version)
        for field in ["url", "license", "description"]:
            field_value = getattr(conanfile, field, None)
            if not field_value:
                output.error("%s Conanfile doesn't have '%s'. It is recommended to add it as attribute: %s"
                            % (test, field, conanfile_path))

    def pre_source(output, conanfile, conanfile_path, **kwargs):
        conanfile_content = tools.load(conanfile_path)
        if "def source(self):" in conanfile_content:
            test = "[IMMUTABLE SOURCES]"
            valid_content = [".zip", ".tar", ".tgz", ".tbz2", ".txz"]
            invalid_content = ["git checkout master", "git checkout devel", "git checkout develop"]
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
                output.error("%s Source files does not come from and immutable place. Checkout to a "
                            "commit/tag or download a compressed source file for %s" % (test, str(reference)))

This hook is only checking the recipe content prior to the recipe being exported and prior to downloading the sources. Basically the
``pre_export()`` function is checking the attributes of the ``conanfile`` object to see if there is an URL, a license and a description and
warning the user with a message through the ``output``. This is done **before** the recipe is exported to the local cache.

The ``pre_source()`` function checks if the recipe contains a ``source()`` method (this time it is using the conanfile content instead of
the ``conanfile`` object) and in that case it checks if the download of the sources are likely coming from immutable places (a compressed
file or a determined :command:`git checkout`). This is done **before** the **source()** method of the recipe is called.

Any kind of Python scripting can be executed. You can create global functions and call them from different hook functions, import from a
relative module and warn, error or even raise to abort the Conan client execution.

As you can see each function receives some parameters but not all of them are available for all functions as this may change depending on
the context of the commands being executed such as the recipe being in the local cache or not.

.. important::

    A detailed description of the functions allowed and its parameters as well as their execution can be found in it dedicated reference
    section: :ref:`hooks_reference`.

Other useful task where a hook may come handy are the upload and download actions. There are **pre** and **post** functions for every
download/upload as a whole and for fine download tasks such as recipe and package downloads/uploads.

For example they can be used to sign the packages (including a file with the signature) when the package is created and and checking that
signature every time they are downloaded.

.. code-block:: python
   :caption: *signing_hook.py*

    import os
    from conans import tools

    SIGNATURE = "this is my signature"

    def post_package(output, conanfile, conanfile_path, **kwargs):
        sign_path = os.path.join(conanfile.package_folder, ".sign")
        tools.save(sign_path, SIGNATURE)
        output.success("Package signed successfully")

    def post_download_package(output, conanfile_path, reference, package_id, remote_name, **kwargs):
        package_path = os.path.abspath(os.path.join(os.path.dirname(conanfile_path), "..", "package", package_id))
        sign_path = os.path.join(package_path, ".sign")
        content = tools.load(sign_path)
        if content != SIGNATURE:
            raise Exception("Wrong signature")

Importing from a module
-----------------------

The hook interface should always be placed inside a Python file with the name of the hook and stored in the *hooks* folder. However,
you can use functionalities from imported modules if you have them installed in your system or if they are installed with Conan:

.. code-block:: python
   :caption: example_hook.py

    import requests
    from conans import tools

    def post_export(output, conanfile, conanfile_path, reference, **kwargs):
        cmakelists_path = os.path.join(os.path.dirname(conanfile_path), "CMakeLists.txt")
        tools.replace_in_file(cmakelists_path, "PROJECT(MyProject)", "PROJECT(MyProject CPP)")
        r = requests.get('https://api.github.com/events')

You can also import functionalities from a relative module:

.. code-block:: text

    hooks
    ├── custom_module
    │   ├── custom.py
    │   └── __init__.py
    └── my_hook.py

Inside the *custom.py* from my *custom_module* there is:

.. code-block:: python

    def my_printer(output):
        output.info("my_printer(): CUSTOM MODULE")

And it can be used in hook importing the module:

.. code-block:: python

    from custom_module.custom import my_printer


    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        my_printer(output)

Storage, activation and sharing
-------------------------------

Hooks are Python files stored under *~/.conan/hooks* folder and **their file name should be the same used for activation** (without the
*.py* extension).

The activation of the hooks is done in the *conan.conf* section named ``[hooks]``. The hook names listed under this section will be
considered activated.

.. code-block:: text
   :caption: *conan.conf*

    ...
    [hooks]
    attribute_checker
    conan-center

They can be easily activated and deactivated from the command line using the :command:`conan config set` command:

.. code-block:: bash

    $ conan config set hooks.attribute_checker  # Activates 'attribute_checker'

    $ conan config rm hooks.attribute_checker  # Deactivates 'attribute_checker'

There is also an environment variable ``CONAN_HOOKS`` to list the active hooks. Hooks listed in *conan.conf* will be loaded into
this variable and values in the environment variable will be used to load the hooks.

Hooks are considered part of the Conan client configuration and can be shared as usual with the :ref:`conan_config_install` command.

Official Hooks
----------------

There is a simple *attribute_checker* hook ready to be used in Conan. You can take it as a starting point to create your own ones.

attribute_checker
+++++++++++++++++

This hook is shipped together with the Conan client and its functionality is warning when recipes do not contain some metadata attributes.

.. code-block:: python
   :caption: *attribute_checker.py*

    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        # Check basic meta-data
        for field in ["url", "license", "description"]:
            field_value = getattr(conanfile, field, None)
            if not field_value:
                output.warn("Conanfile doesn't have '%s'. It is recommended to add it as attribute"
                            % field)

This hook comes activated by default.
