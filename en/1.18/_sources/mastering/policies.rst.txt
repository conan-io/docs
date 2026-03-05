Build policies
==============

By default, :command:`conan install` command will search for a binary package (corresponding to our settings and defined options) in a remote.
If it's not present the install command will fail.

As previously demonstrated, we can use the :command:`--build` option to change the default :command:`conan install` behavior:

- :command:`--build some_package` will build only "some_package".
- :command:`--build missing` will build only the missing requires.
- :command:`--build` will build all requirements from sources.
- :command:`--build outdated` will try to build from code if the binary is not built with the current recipe or when missing binary package.
- :command:`--build cascade` will build from code all the nodes with some dependency being built (for any reason). Can be used together with any
  other build policy. Useful to make sure that any new change introduced in a dependency is incorporated by building again the package.
- :command:`--build pattern*` will build only the packages with the reference starting with "pattern".


With the ``build_policy`` attribute in the `conanfile.py` the package creator can change the default Conan's build behavior. The allowed build_policy values are:

- ``missing``: If no binary package is found, Conan will build it without the need to invoke Conan install with :command:`--build missing`
  option.
- ``always``: The package will be built always, **retrieving each time the source code** executing the "source" method.


.. code-block:: python
   :emphasize-lines: 6

    class PocoTimerConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        requires = "Poco/1.7.8p3@pocoproject/stable" # comma-separated list of requirements
        generators = "cmake", "gcc", "txt"
        default_options = {"Poco:shared": True, "OpenSSL:shared": True}
        build_policy = "always" # "missing"

These build policies are especially useful if the package creator doesn't want to provide binary package; for example, with header only
libraries.

The ``always`` policy will retrieve the sources each time the package is installed, so it can be useful for providing a "latest" mechanism
or ignoring the uploaded binary packages.

The package pattern can be referred as a case-sensitive fnmatch pattern of the package name or the full package reference.
e.g :command:`--build Poco`, :command:`--build Poc*`, :command:`--build zlib/*@conan/*`, :command:`--build *@conan/stable` or :command:`--build zlib/1.2.11@conan/stable`.
