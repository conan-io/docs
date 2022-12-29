.. _hooks_reference:

Hooks
=====

The Conan hooks are Python functions that are intended to extend the Conan functionalities and let users customize the client behavior at
determined execution points. Check the :ref:`hooks section in extending Conan <reference_extensions_hooks>` to see
some examples of how to use them and already available ones providing useful functionality.

Hook interface
--------------

Here you can see a complete example of all the hook functions available and the different parameters for each of them depending on the
context:

.. code-block:: python
   :caption: *hook_example.py*

    import os
    import fnmatch
    from conan.tools.files import collect_libs, save, load

    def pre_export(conanfile):
        description = getattr(conanfile, "description", None)
        max_length = 72
        if not description:
            conanfile.output.error("The attribute 'description' is missing.")
        elif len(description) > max_length:
            conanfile.output.error(f"The attribute 'description' content is too long. Please, keep it {max_length} characters long.")

    def post_export(conanfile):
        if str(conanfile.license).lower() in ["public domain", "public-domain", "public_domain"]:
            conanfile.output.error("Public Domain is not a SPDX license. Please, use 'Unlicense' instead.")

    def pre_source(conanfile):
        conandata_source = os.path.join(conanfile.export_source_folder, "conandata.yml")
        if not os.path.exists(conandata_source):
            conanfile.output.error("Add source url to 'conandata.yml' file to be downloaded.")

    def post_source(conanfile):
        license_files = ["LICENSE", "COPYRIGHT", "LICENSE.md", "LICENSE.txt"]
        for license_file in license_files:
            if os.path.isfile(os.path.join(conanfile.source_folder, license_file)):
                return
        conanfile.output.warning("Could not find any license file in the source folder.")

    def pre_generate(conanfile):
        if "CMakeToolchain" in coananfile.generators and conanfile.requires and not "CMakeDeps" in coananfile.generators:
            conanfile.output.warning("Found 'CMakeToolchain' and requirements usage in the recipe, but 'CMakeDeps' looks missing.")

    def post_generate(conanfile):
        cmake_folder = os.path.join(conanfile.build_folder, "cmake")
        if os.path.isdir(cmake_folder):
            for filename in cmake_folder:
                if os.path.isfile(filename) and filename.endswith(".cmake"):
                    conanfile.output.warning(f"Found extra CMake files in {cmake_folder}! Please, check it to avoid inconsistent builds.")

    def pre_build(conanfile):
        if conanfile.options.get_safe("fPIC") and conanfile.settings.get_safe("os") == "Windows":
            conanfile.output.error("'fPIC' option not managed correctly. Please remove it for Windows.")

    def post_build(conanfile):
        if conanfiles.options.get_safe("shared"):
            for filename in os.listdir(conanfile.build_folder):
                if os.path.isfile(filename) and fnmatch.fnmatch(filename, ["*.so", "*.dylib", "*.dll"]):
                    return
            conanfile.output.error("Building with the option 'shared=True' did not generate any dynamic library.")

    def pre_package(conanfile):
        save(conanfile, os.path.join(conanfile.package_folder, "company.sig"), os.getenv("COMPANY_CONAN_PKG_SIGNATURE"))

    def post_package(conanfile):
        licenses_folder = os.path.join(os.path.join(conanfile.package_folder, "licenses"))
        if not os.path.exists(licenses_folder):
            conanfile.output.error(f"No 'licenses' folder found in package: '{conanfile.package_folder}'")

    def pre_package_info(conanfile):
        if conanfiles.options.get_safe("shared"):
            for filename in os.listdir(conanfile.build_folder):
                if os.path.isfile(filename) and fnmatch.fnmatch(filename, ["*.so", "*.dylib", "*.dll"]):
                    return
            conanfile.output.error("Building with the option 'shared=True' did not generate any dynamic library.")

    def post_package_info(conanfile):
        collected_libs = collect_libs(conanfile)
        for library in conanfile.cpp_info.libs:
            if library not in collected_libs:
                self.output.error(f"The library '{library}' has been detected in the package folder, but is not listed in cpp_info.libs")


Functions of the hooks are intended to be self-descriptive regarding to the execution of them. For example, the ``pre_package()`` function
is called just before the ``package()`` method of the recipe is executed.

Function parameters
-------------------

Here you can find the description for each parameter:

- **conanfile**: It is a regular ``ConanFile`` object loaded from the recipe that received the Conan command. It has its normal attributes
  and dynamic objects such as ``build_folder``, ``package_folder``, ``output``, ``dependencies``,  ``options`` ...
