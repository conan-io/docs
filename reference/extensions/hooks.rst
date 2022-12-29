.. _reference_extensions_hooks:

Hooks
-----

The Conan hooks is a feature intended to extend the Conan functionalities and let users customize the client behavior at determined
points.

Hook structure
--------------

A hook is a Python function that will be executed at certain points of Conan workflow
to customize the client behavior without modifying the client sources or the recipe ones.
In the :ref:`hooks reference <hooks_reference>` you can find the full list of hook functions
and exhaustive documentation about their arguments.

Hooks can implement any functionality: it could be Conan commands, recipe interactions
such as exporting or packaging, or interactions with the remotes.

Here is an example of a simple hook:

.. code-block:: python
   :caption: *hook_example.py*

    import os
    from conan.tools.files import load

    def pre_export(conanfile):
        for field in ["url", "license", "description"]:
            field_value = getattr(conanfile, field, None)
            if not field_value:
                conanfile.output.error(f"[REQUIRED ATTRIBUTES] Conanfile doesn't have '{field}'.
                                          It is recommended to add it as attribute.")

    def pre_source(conanfile):
        conanfile_content = load(conanfile, os.path.join(conanfile.recipe_folder, "conanfile.py"))
        if "def source(self):" in conanfile_content:
            test = ""
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
                output.error(f"[IMMUTABLE SOURCES] Source files does not come from and immutable place. Checkout to a "
                            "commit/tag or download a compressed source file for {conanfile.ref}")

This hook checks the recipe content prior to it being exported and prior to downloading the sources. Basically the
``pre_export()`` function checks the attributes of the ``conanfile`` object to see if there is an URL, a license and a description and if missing,
warns the user with a message through the ``conanfile.output``. This is done **before** the recipe is exported to the local cache.

The ``pre_source()`` function checks if the recipe contains a ``source()`` method (this time it is using the *conanfile.py* content instead of
the ``conanfile`` object) and in that case it checks if the download of the sources are likely coming from immutable places (a compressed
file or a determined :command:`git checkout`). This is done **before** the **source()** method of the recipe is called.

Any kind of Python script can be executed. You can create global functions and call them from different hook functions, import from a
relative module and warn, error or even raise to abort the Conan client execution.


Other useful task where a hook may come handy are the upload and download actions. There are **pre** and **post** functions for every
download/upload as a whole and for fine download tasks such as recipe and package downloads/uploads.

For example they can be used to sign the packages (including a file with the signature) when the package is created and check that
signature every time they are downloaded.

.. code-block:: python
   :caption: *hook_package_signing.py*

    import os
    from conan.tools.files import save, load

    SIGNATURE = os.getenv("ENTERPRISE_CONAN_PKG_SIGNATURE", "default-signature")

    def post_package(conanfile):
        sign_path = os.path.join(conanfile.package_folder, ".sign")
        save(conanfile, sign_path, SIGNATURE)
        conanfile.output.info("Package signed successfully")

    def post_package_info(conanfile):
        sign_path = os.path.join(conanfile.package_folder, ".sign")
        content = load(conanfile, sign_path)
        if content != SIGNATURE:
            conanfile.output.error(f"[CHECK SIGNATURE] The signature file '{sign_path}' has a different content than the expected one.")


Importing from a module
-----------------------

The hook interface should always be placed inside a Python file with the name of the hook starting by *hook_* and with the extension *.py*.
It also should be stored in the *~/.conan2/extensions/hooks* folder. However, you can use functionalities from imported modules if you have
them installed in your system or if they are installed with Conan:

.. code-block:: python
   :caption: hook_example.py

    import requests
    from conan.tools.files import replace_in_file

    def post_export(conanfile):
        cmakelists_path = os.path.join(conanfile.export_source_folder, "CMakeLists.txt")
        replace_in_file(conanfile, cmakelists_path, "PROJECT(MyProject)", "PROJECT(MyProject LANGUAGES CXX)")
        r = requests.get('https://api.github.com/events')

You can also import functionalities from a relative module:

.. code-block:: text

    hooks
    ├── custom_module
    │   ├── custom.py
    │   └── __init__.py
    └── hook_printer.py

Inside the *custom.py* from my *custom_module* there is:

.. code-block:: python
   :caption: custom.py

    def my_printer(conanfile):
        conanfile.output.info("my_printer(): CUSTOM MODULE")

And it can be used in the hook importing the module, just like regular Python:

.. code-block:: python
   :caption: hook_printer.py

    from custom_module.custom import my_printer

    def pre_export(conanfile):
        my_printer(conanfile)


Storage, activation and sharing
-------------------------------

Hooks are Python files stored under *~/.conan2/extensions/hooks* folder and **their file name should start with hook_ and end with the
.py extension**.

The activation of the hooks is done automatically once the hook file is stored in the hook folder.
In case storing in subfolders, it works automatically too.

To deactivate a hook, its file should be removed from the hook folder. There is no configuration which can deactivate but keep the file stored in hooks folder.

Hooks are considered part of the Conan client configuration and can be shared as usual with the `reference_commands_config` command.
However, they can also be managed in isolated Git repositories cloned into the *~/.conan2/extensions/hooks* folder:

.. code-block:: bash

    $ cd ~/.conan2/extensions/hooks
    $ git clone https://github.com/myuser/my-conan-hooks.git my_hooks

This way you can easily change from one version to another.

Official Hooks
--------------

There are some officially maintained hooks in its own repository in `Conan hooks GitHub <https://github.com/conan-io/hooks>`_,
but mostly are only compatible with Conan 1.x, so please, check first the `README <https://github.com/conan-io/hooks/blob/master/README.md>`_
to have information which hooks are compatible with Conan v2.
