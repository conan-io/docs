
Package information for consumers
+++++++++++++++++++++++++++++++++


cpp_info
--------

Same as using ``self.cpp.package`` in the ``layout()`` method. Use it if you need to read
the ``package_folder`` to locate the already located artifacts.

.. seealso::

    Read more about the :ref:`CppInfo<conan_conanfile_model_cppinfo>` model.


.. important::

    This attribute is only defined inside ``package_info()`` method being `None` elsewhere.


.. _conan_conanfile_attributes_buildenv_info:

buildenv_info
-------------

For the dependant recipes, the declared environment variables will be present during the
build process. Should be only filled in the ``package_info()`` method.


.. important::

    This attribute is only defined inside ``package_info()`` method being `None` elsewhere.

.. code-block:: python

    def package_info(self):
        self.buildenv_info.append_path("PATH", self.package_folder)


.. seealso::

    Check the reference of the :ref:`Environment<conan_tools_env_environment_model>` object to know how to fill
    the ``self.buildenv_info``.


.. _conan_conanfile_attributes_runenv_info:

runenv_info
-----------

For the dependant recipes, the declared environment variables will be present at runtime.
Should be only filled in the ``package_info()`` method.


.. important::

   This attribute is only defined inside ``package_info()`` method being `None` elsewhere.

.. code-block:: python

    def package_info(self):
        self.runenv_info.define_path("RUNTIME_VAR", "c:/path/to/exe")


.. seealso::

    Check the reference of the :ref:`Environment<conan_tools_env_environment_model>` object to know how to fill
    the ``self.runenv_info``.


.. _conan_conanfile_attributes_conf_info:

conf_info
---------

Configuration variables to be passed to the dependant recipes.
Should be only filled in the ``package_info()`` method.

.. code-block:: python

    class Pkg(ConanFile):
        name = "pkg"

        def package_info(self):
            self.conf_info.define("tools.microsoft.msbuild:verbosity", "Diagnostic")
            self.conf_info.get("tools.microsoft.msbuild:verbosity")  # == "Diagnostic"
            self.conf_info.append("user.myconf.build:ldflags", "--flag3")  # == ["--flag1", "--flag2", "--flag3"]
            self.conf_info.update("tools.microsoft.msbuildtoolchain:compile_options", {"ExpandAttributedSource": "false"})
            self.conf_info.unset("tools.microsoft.msbuildtoolchain:compile_options")
            self.conf_info.remove("user.myconf.build:ldflags", "--flag1")  # == ["--flag0", "--flag2", "--flag3"]
            self.conf_info.pop("tools.system.package_manager:sudo")

.. seealso::

      Read here :ref:`the complete reference of self.conf_info <conan_conanfile_model_conf_info>`.


deprecated
----------

This attribute declares that the recipe is deprecated, causing a user-friendly warning
message to be emitted whenever it is used

For example, the following code:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "cpp-taskflow"
        version = "1.0"
        deprecated = True

may emit a warning like:

.. code-block:: bash

    cpp-taskflow/1.0: WARN: Recipe 'cpp-taskflow/1.0' is deprecated. Please, consider changing your requirements.

Optionally, the attribute may specify the name of the suggested replacement:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "cpp-taskflow"
        version = "1.0"
        deprecated = "taskflow"

This will emit a warning like:

.. code-block:: bash

    cpp-taskflow/1.0: WARN: Recipe 'cpp-taskflow/1.0' is deprecated in favor of 'taskflow'. Please, consider changing your requirements.

If the value of the attribute evaluates to ``False``, no warning is printed.


provides
--------

This attribute declares that the recipe provides the same functionality as other recipe(s).
The attribute is usually needed if two or more libraries implement the same API to prevent
link-time and run-time conflicts (ODR violations). One typical situation is forked libraries.
Some examples are:
    
- `LibreSSL <https://www.libressl.org/>`__, `BoringSSL <https://boringssl.googlesource.com/boringssl/>`__ and `OpenSSL <https://www.openssl.org/>`__
- `libav <https://en.wikipedia.org/wiki/Libav>`__ and `ffmpeg <https://ffmpeg.org/>`__
- `MariaDB client <https://downloads.mariadb.org/client-native>`__ and `MySQL client <https://dev.mysql.com/downloads/c-api/>`__
 


If Conan encounters two or more libraries providing the same functionality within a single graph, it raises an error:

.. code-block:: bash

    At least two recipes provides the same functionality:
    - 'libjpeg' provided by 'libjpeg/9d', 'libjpeg-turbo/2.0.5'

The attribute value should be a string with a recipe name or a tuple of such recipe names.

For example, to declare that ``libjpeg-turbo`` recipe offers the same functionality as ``libjpeg`` recipe, the following code could be used:

.. code-block:: python

    from conan import ConanFile

    class LibJpegTurbo(ConanFile):
        name = "libjpeg-turbo"
        version = "1.0"
        provides = "libjpeg"


To declare that a recipe provides the functionality of several different recipes at the same time, the following code could be used:

.. code-block:: python

    from conan import ConanFile

    class OpenBLAS(ConanFile):
        name = "openblas"
        version = "1.0"
        provides = "cblas", "lapack"

If the attribute is omitted, the value of the attribute is assumed to be equal to the current package name. Thus, it's redundant for
``libjpeg`` recipe to declare that it provides ``libjpeg``, it's already implicitly assumed by Conan.
