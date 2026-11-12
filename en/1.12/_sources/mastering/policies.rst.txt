Build policies
==============

By default, :command:`conan install` command will search for a binary package (corresponding to our settings and defined options) in a remote,
if it's not present the install command will fail.

As previously demonstrated, we can use the :command:`--build` option to change the default :command:`conan install` behavior:

- :command:`--build some_package` will build only "some_package".
- :command:`--build missing` will build only the missing requires.
- :command:`--build` will build all requirements from sources.
- :command:`--build outdated` will try to build from code if the binary is not built with the current recipe or when missing binary package.

With the ``build_policy`` attribute the package creator can change the default conan's build behavior. The allowed build_policy values are:

- ``missing``: If no binary package is found, conan will build it without the need of invoke conan install with :command:`--build missing`
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

These build policies are especially useful if the package creator doesn't want to provide binary package, for example, with header only
libraries.

The ``always`` policy, will retrieve the sources each time the package is installed so it can be useful for providing a "latest" mechanism
or ignoring the uploaded binary packages.

The package pattern can be referred as the package name only or a full reference e.g :command:`--build Poco` or :command:`--build zlib/1.2.11@conan/stable`.
