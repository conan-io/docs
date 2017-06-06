Build policies
=================

By default, ``conan install`` command will search for a binary package (corresponding to our settings and defined options) in a remote, if it's not present the install command will fail.

As we previously see, we can use the **--build** option to change the default ``conan install`` behaviour:

- **- -build some_package** will build only "some_package"
- **- -build missing** will build only the missing requires.
- **- -build** will build all requires from sources.
- **- -build outdated** will try to build from code if the binary is not built with the current recipe or when missing binary package 


With the ``build_policy`` attribute the package creator can change the default conan's build behavior.
The allowed build_policy values are:

- ``missing``: If no binary package is found, conan will build it without the need of invoke conan install with **--build missing** option.
- ``always``: The package will be built always, **retrieving each time the source code** executing the "source" method.


.. code-block:: python
   :emphasize-lines: 6

     class PocoTimerConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        requires = "Poco/1.7.3@lasote/stable" # comma separated list of requirements
        generators = "cmake", "gcc", "txt"
        default_options = "Poco:shared=True", "OpenSSL:shared=True"
        build_policy = "always" # "missing"

       
These build policies are specially useful if the package creator don't want to provide binary packages, for example with header only libraries.

The "always" policy, will retrieve the sources each time the package is installed so it can be useful for provide a "latest" mechanism or ignore the uploaded binary packages.
