.. _reference_extensions_hooks:

Hooks
-----

The Conan hooks is a feature intended to extend the Conan functionalities to perform certain orthogonal operations,
like some quality checks, in different stages of a package creation process, like pre-build and post-build.

Hook structure
^^^^^^^^^^^^^^

A hook is a Python function that will be executed at certain points of Conan workflow
to customize the client behavior without modifying the client sources or the recipe ones.

Here is an example of a simple hook:

.. code-block:: python
   :caption: *hook_example.py*

    from conan.tools.files import load

    def pre_export(conanfile):
        for field in ["url", "license", "description"]:
            field_value = getattr(conanfile, field, None)
            if not field_value:
                conanfile.output.error(f"[REQUIRED ATTRIBUTES] Conanfile doesn't have '{field}'.
                                          It is recommended to add it as attribute.")

This hook checks the recipe content prior to it being exported. Basically the
``pre_export()`` function checks the attributes of the ``conanfile`` object to see if there is an URL, a license and a description and if missing,
warns the user with a message through the ``conanfile.output``. This is done **before** the recipe is exported to the local cache.

Any kind of Python script can be executed. You can create global functions and call them from different hook functions, import from a
relative module and warn, error or even raise to abort the Conan client execution.


Importing from a module
^^^^^^^^^^^^^^^^^^^^^^^

The hook interface should always be placed inside a Python file with the name of the hook starting by *hook_* and with the extension *.py*.
It also should be stored in the *<conan_home>/extensions/hooks* folder. However, you can use functionalities from imported modules if you have
them installed in your system or if they are installed with Conan:

.. code-block:: python
   :caption: hook_example.py

    import requests
    from conan.tools.files import replace_in_file

    def post_package(conanfile):
        if not os.path.isdir(os.path.join(conanfile.package_folder, "licenses")):
            response = requests.get('https://api.github.com/repos/company/repository/contents/LICENSE')

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

Hook interface
^^^^^^^^^^^^^^

Here you can see a complete example of all the hook functions available:

.. code-block:: python
   :caption: *hook_full.py*

    def pre_export(conanfile):
        conanfile.output.info("Running before to execute export() method.")

    def post_export(conanfile):
        conanfile.output.info("Running after of executing export() method.")

    def pre_source(conanfile):
        conanfile.output.info("Running before to execute source() method.")

    def post_source(conanfile):
        conanfile.output.info("Running after of executing source() method.")

    def pre_generate(conanfile):
        conanfile.output.info("Running before to execute generate() method.")

    def post_generate(conanfile):
        conanfile.output.info("Running after of executing generate() method.")

    def pre_build(conanfile):
        conanfile.output.info("Running before to execute build() method.")

    def post_build(conanfile):
        conanfile.output.info("Running after of executing build() method.")

    def pre_package(conanfile):
        conanfile.output.info("Running before to execute package() method.")

    def post_package(conanfile):
        conanfile.output.info("Running after of executing package() method.")

    def pre_package_info(conanfile):
        conanfile.output.info("Running before to execute package_info() method.")

    def post_package_info(conanfile):
        conanfile.output.info("Running after of executing package_info() method.")

Functions of the hooks are intended to be self-descriptive regarding to the execution of them. For example, the ``pre_package()`` function
is called just before the ``package()`` method of the recipe is executed.



All hook methods are filled only with the same single object:

- **conanfile**: It is a regular ``ConanFile`` object loaded from the recipe that received the Conan command. It has its normal attributes
  and dynamic objects such as ``build_folder``, ``package_folder``, ``output``, ``dependencies``,  ``options`` ...

Storage, activation and sharing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hooks are Python files stored under *<conan_home>/extensions/hooks* folder and **their file name should start with hook_ and end with the
.py extension**.

The activation of the hooks is done automatically once the hook file is stored in the hook folder.
In case storing in subfolders, it works automatically too.

To deactivate a hook, its file should be removed from the hook folder. There is no configuration which can deactivate but keep the file stored in hooks folder.

Official Hooks
^^^^^^^^^^^^^^

There are some officially maintained hooks in its own repository in `Conan hooks GitHub <https://github.com/conan-io/hooks>`_,
but mostly are only compatible with Conan 1.x, so please, check first the `README <https://github.com/conan-io/hooks/blob/master/README.md>`_
to have information which hooks are compatible with Conan v2.
