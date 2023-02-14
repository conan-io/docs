.. spelling::

  ing
  ver

.. _conan_conanfile_attributes:

Attributes
==========


name
----

The name of the package. A valid name is all lowercase and has:

- A minimum of 2 and a maximum of 101 characters (though shorter names are recommended).
- Matches the following regex ``^[a-z0-9_][a-z0-9_+.-]{1,100}$``: so starts with alphanumeric or ``_``,
    then from 1 to 100 characters between alphanumeric, ``_``, ``+``, ``.`` or ``-``.

The name is only necessary for ``export``-ing the recipe into the local cache (``export``, ``export-pkg``
 and ``create`` commands), if they are not defined in the command line with ``--name=<pkgname>``.


version
-------

The version of the package. A valid version follows the same rules than the ``name`` attribute.
In case the version follows semantic versioning in the form ``X.Y.Z-pre1+build2``, that value might be used for requiring
this package through version ranges instead of exact versions.

The version is only strictly necessary for ``export``-ing the recipe into the local cache (``export``, ``export-pkg`` 
and ``create`` commands), if they are not defined in the command line with ``--version=<pkgversion>``

The ``version`` can be dynamically defined in the command line, and also programmaticaly in the recipe with the
:ref:`set_version() method<reference_conanfile_methods_set_version>`.


user
----

A valid string for the ``user`` field follows the same rules than the ``name`` attribute.
This is an optional attribute. It can be used to identify your own packages with ``pkg/version@user/channel``,
where ``user`` could be the name of your team, org or company. ConanCenter recipes don't have ``user/channel``,
so they are in the form of ``pkg/version`` only. You can also name your packages without user and channel, or using
only the user as ``pkg/version@user``.

The user can be specified in the command line with ``--user=<myuser>``


channel
-------

A valid string for the ``channel`` field follows the same rules than the ``name`` attribute.
This is an optional attribute. It is sometimes used to identify a maturity of the package ("stable", "testing"...),
but in general this is not necessary, and the maturity of packages is better managed by putting them in different
server repositories.

The user can be specified in the command line with ``--channel=<mychannel>``


description
-----------

This is an optional, but recommended text field, containing the description of the package,
and any information that might be useful for the consumers. The first line might be used as a
short description of the package.

.. code-block:: python

    class HelloConan(ConanFile):
        name = "hello"
        version = "0.1"
        description = """This is a Hello World library.
                        A fully featured, portable, C++ library to say Hello World in the stdout,
                        with incredible iostreams performance"""


license
-------

License of the **target** source code and binaries, i.e. the code
that is being packaged, not the ``conanfile.py`` itself.
Can contain several, comma separated licenses. It is a text string, so it can
contain any text, but it is strongly recommended that recipes of Open Source projects use
`SPDX <https://spdx.dev>`_ identifiers from the `SPDX license list <https://spdx.dev/licenses>`_


This will help people wanting to automate license compatibility checks, like consumers of your
package, or you if your package has Open-Source dependencies.

.. code-block:: python

    class Pkg(ConanFile):
        license = "MIT"


author
------
Main maintainer/responsible for the package, any format. This is an optional attribute.

.. code-block:: python

    class HelloConan(ConanFile):
        author = "John J. Smith (john.smith@company.com)"

topics
------

Tags to group related packages together and describe what the code is about.
Used as a search filter in ConanCenter. Optional attribute. It should be a tuple of strings.

.. code-block:: python

    class ProtocInstallerConan(ConanFile):
        name = "protoc_installer"
        version = "0.1"
        topics = ("protocol-buffers", "protocol-compiler", "serialization", "rpc")

homepage
--------

The home web page of the library being packaged.

Used to link the recipe to further explanations of the library itself like an overview of its features, documentation, FAQ
as well as other related information.

.. code-block:: python

    class EigenConan(ConanFile):
        name = "eigen"
        version = "3.3.4"
        homepage = "http://eigen.tuxfamily.org"


url
---

URL of the package repository, i.e. not necessarily of the original source code.
Recommended, but not mandatory attribute.

.. code-block:: python

    class HelloConan(ConanFile):
        name = "hello"
        version = "0.1"
        url = "https://github.com/conan-io/hello.git"



.. _reference_conanfile_attributes_package_type:

package_type
------------

Optional. Declaring the ``package_type`` will help Conan:

- To choose better the default ``package_id_mode`` for each dependency, that is, how a change
  in a dependency should affect the ``package_id`` to the current package.
- Which information from the dependencies should be propagated to the consumers, like
  headers, libraries, runtime information...

The valid values are:

- **application**: The package is an application.
- **library**: The package is a generic library. It will try to determine
  the type of library (from ``shared-library``, ``static-library``, ``header-library``)
  reading the ``self.options.shared`` (if declared) and the ``self.options.header_only``
- **shared-library**: The package is a shared library.
- **static-library**: The package is a static library.
- **header-library**: The package is a header only library.
- **build-scripts**: The package only contains build scripts.
- **python-require**: The package is a python require.
- **unknown**: The type of the package is unknown.


.. _conan_conanfile_properties_settings:

settings
--------

List of strings with the first level settings (from ``settings.yml``) that the recipe
need, because:
- They are read for building (e.g: `if self.settings.compiler == "gcc"`)
- They affect the ``package_id``. If a value of the declared setting changes, the ``package_id`` has to be different.

The most common is to declare:

.. code-block:: python

    settings = "os", "compiler", "build_type", "arch"

Once the recipe is loaded by Conan, the ``settings`` are processed and they can be read in the recipe, also
the sub-settings:

.. code-block:: python

    settings = "os", "arch"

    def build(self):
        if self.settings.compiler == "gcc":
            if self.settings.compiler.cppstd == "gnu20":
                # do some special build commands

If you try to access some setting that doesn't exist, like ``self.settings.compiler.libcxx``
for the ``msvc`` setting, Conan will fail telling that ``libcxx`` does not exist for that compiler.

If you want to do a safe check of settings values, you could use the ``get_safe()`` method:

.. code-block:: python

    def build(self):
        # Will be None if doesn't exist (not declared)
        arch = self.settings.get_safe("arch")
        # Will be None if doesn't exist (doesn't exist for the current compiler)
        compiler_version = self.settings.get_safe("compiler.version")
        # Will be the default version if the return is None
        build_type = self.settings.get_safe("build_type", default="Release")

The ``get_safe()`` method will return ``None`` if that setting or sub-setting doesn't
exist and there is no default value assigned.

If you want to do a safe deletion of settings, you could use the ``rm_safe()`` method.
For example, in the ``configure()`` method a typical pattern for a C library would be:

.. code-block:: python

    def configure(self):
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

.. seealso::

    - Removing settings in the ``package_id()`` method. <MISSING PAGE>


.. _conan_conanfile_properties_options:

options
-------

Dictionary with traits that affects only the current recipe, where the key is the
option name and the value is a list of different values that the option can take.
By default any value change in an option, changes the ``package_id``. Check the
``default_options`` field to define default values for the options.

Values for each option can be typed or plain strings (``"value"``, ``True``, ``42``,...).

There are two special values:

- ``None``: Allow the option to have a ``None`` value (not specified) without erroring.
- ``"ANY"``:  For options that can take any value, not restricted to a set.

.. code-block:: python

    class MyPkg(ConanFile):
        ...
        options = {
            "shared": [True, False],
            "option1": ["value1", "value2"],
            "option2": ["ANY"],
            "option3": [None, "value1", "value2"],
            "option4": [True, False, "value"],
    }

Once the recipe is loaded by Conan, the ``options`` are processed and they can be read in the recipe. You can also
use the method ``.get_safe()`` (see :ref:`settings attribute<conan_conanfile_properties_settings>`) to avoid Conan raising an Exception if the option
doesn't exist:

.. code-block:: python

    class MyPkg(ConanFile):
        options = {"shared": [True, False]}

        def build(self):
            if self.options.shared:
                # build the shared library
            if self.options.get_safe("foo", True):
                pass

In boolean expressions, like ``if self.options.shared``:

- equals ``True`` for the values ``True``, ``"True"`` and ``"true"``, and any other value that
  would be evaluated the same way in Python code.
- equals ``False`` for the values ``False``, ``"False"`` and ``"false"``, also for the empty
  string and for ``0`` and ``"0"`` as expected.

Notice that a comparison using ``is`` is always ``False`` because the types would be different as it is encapsulated
inside a Python class.

If you want to do a safe deletion of options, you could use the ``rm_safe()`` method.
For example, in the ``config_options()`` method a typical pattern for Windows library
would be:

.. code-block:: python

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

.. seealso::

    - Read the :ref:`Getting started, creating packages<creating_packages_create_your_first_conan_package>` to know how to declare and how to
      define a value to an option.
    - Removing options in the ``package_id()`` method. <MISSING PAGE>
    - About the package_type and how it plays when a ``shared`` option is declared. <MISSING PAGE>


.. _conan_conanfile_properties_default_options:

default_options
---------------

The attribute ``default_options`` defines the default values for the options, both for the
current recipe and for any requirement.
This attribute should be defined as a python dictionary.


.. code-block:: python

    class MyPkg(ConanFile):
        ...
        requires = "zlib/1.2.8", "zwave/2.0"
        options = {"build_tests": [True, False],
                    "option2": "ANY"}
        default_options = {"build_tests": True,
                            "option1": 42,
                            "z*: shared": True}


You can also assign default values for options of your requirements using "<reference_pattern>: option_name", being
a valid ``reference_pattern`` a ``name/version`` or any pattern with ``*`` like the example above.

You can also set the options conditionally to a final value with ``configure()`` instead of using ``default_options``:

.. code-block:: python

    class OtherPkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        options = {"some_option": [True, False]}
        # Do NOT declare 'default_options', use 'config_options()'

        def configure(self):
            if self.options.some_option == None:
                if self.settings.os == 'Android':
                    self.options.some_option = True
                else:
                    self.options.some_option = False

Take into account that if a value is assigned in the ``configure()`` method it cannot be overridden.

.. seealso::

    Read more about the <MISSING PAGE>method_configure_config_options method.


options_description
-------------------

TODO: Complete, https://github.com/conan-io/conan/pull/11295


requires
--------

List or tuple of strings for regular dependencies in the host context, like a library.



.. code-block:: python

    class MyLibConan(ConanFile):
        requires = "hello/1.0", "otherlib/2.1@otheruser/testing"


You can specify version ranges, the syntax is using brackets:

.. _version_ranges_reference:


..  code-block:: python

    class HelloConan(ConanFile):
        requires = "pkg/[>1.0 <1.8]"


Accepted expressions would be:

.. list-table::
    :widths: 25 25 50
    :header-rows: 1

    * - Expression
      - Versions in range
      - Versions outside of range
    * - [>=1.0 <2]
      - 1.0.0, 1.0.1, 1.1, 1.2.3
      - 0.2, 2.0, 2.1, 3.0
    * - [<3.2.1]
      - 0.1, 1.2, 2.4, 3.1.1
      - 3.2.2
    * - [>2.0]
      - 2.1, 2.2, 3.1, 14.2
      - 1.1, 1.2, 2.0


.. seealso::

    - Check <MISSING PAGE> version_ranges if you want to learn more about version ranges.
    - Check <MISSING PAGE> requires() conanfile.py method.


tool_requires
--------------

List or tuple of strings for dependencies. Represents a build tool like "cmake". If there is
an existing pre-compiled binary for the current package, the binaries for the tool_require
won't be retrieved. They cannot conflict.

.. code-block:: python

    class MyPkg(ConanFile):
        tool_requires = "tool_a/0.2", "tool_b/0.2@user/testing"


This is the declarative way to add ``tool_requires``. Check the <MISSING PAGE> tool_requires()
conanfile.py method to learn a more flexible way to add them.


.. _reference_conanfile_attributes_build_requires:

build_requires
--------------

List or tuple of strings for dependencies. Generic type of build dependencies that are not
applications (nothing runs), like build scripts. If there is
an existing pre-compiled binary for the current package, the binaries for the build_require
won't be retrieved. They cannot conflict.

.. code-block:: python

    class MyPkg(ConanFile):
        build_requires = ["my_build_scripts/1.3",]

This is the declarative way to add ``build_requires``. Check the <MISSING PAGE> build_requires()
conanfile.py method to learn a more flexible way to add them.


test_requires
--------------

List or tuple of strings for dependencies in the host context only. Represents a test tool
like "gtest". Used when the current package is built from sources.
They don't propagate information to the downstream consumers. If there is
an existing pre-compiled binary for the current package, the binaries for the test_require
won't be retrieved. They cannot conflict.

.. code-block:: python

    class MyPkg(ConanFile):
        test_requires = "gtest/1.11.0", "other_test_tool/0.2@user/testing"


This is the declarative way to add ``test_requires``. Check the <MISSING PAGE> test_requires()
conanfile.py method to learn a more flexible way to add them.


.. _exports_attribute:

exports
-------


List or tuple of strings with `file names` or
`fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ patterns that should be exported
and stored side by side with the *conanfile.py* file to make the recipe work:
other python files that the recipe will import, some text file with data to read,...


For example, if we have some python code that we want the recipe to use in a ``helpers.py`` file,
and have some text file *info.txt* we want to read and display during the recipe evaluation
we would do something like:

.. code-block:: python

    exports = "helpers.py", "info.txt"

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

    exports = "*.py", "!*tmp.py"


.. seealso::

    - Check <MISSING PAGE> exports() conanfile.py method.


.. _exports_sources_attribute:

exports_sources
---------------

List or tuple of strings with file names or
`fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ patterns that should be exported
and will be available to generate the package. Unlike the ``exports`` attribute, these files
shouldn’t be used by the ``conanfile.py`` Python code, but to compile the library or generate
the final package. And, due to its purpose, these files will only be retrieved if requested
binaries are not available or the user forces Conan to compile from sources.

This is an alternative to getting the sources with the ``source()`` method. Used when we are not packaging a third party
library and we have together the recipe and the C/C++ project:

.. code-block:: python

    exports_sources = "include*", "src*"

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

    exports_sources = "include*", "src*", "!src/build/*"


Note, if the recipe defines the ``layout()`` method and specifies a ``self.folders.source = "src"`` it won't affect
where the files (from the ``exports_sources``) are copied. They will be copied to the base source folder. So, if you
want to replace some file that got into the ``source()`` method, you need to explicitly copy it from the parent folder
or even better, from ``self.export_sources_folder``.

.. code-block:: python

    import os, shutil
    from conan import ConanFile
    from conan.tools.files import save, load

    class Pkg(ConanFile):
        ...
        exports_sources = "CMakeLists.txt"

        def layout(self):
            self.folders.source = "src"
            self.folders.build = "build"

        def source(self):
            # emulate a download from web site
            save(self, "CMakeLists.txt", "MISTAKE: Very old CMakeLists to be replaced")
            # Now I fix it with one of the exported files
            shutil.copy("../CMakeLists.txt", ".")
            shutil.copy(os.path.join(self.export_sources_folder, "CMakeLists.txt", "."))


generators
----------

List or tuple of strings with names of generators.

.. code-block:: python

    class MyLibConan(ConanFile):
        generators = "CMakeDeps", "CMakeToolchain"


The generators can also be instantiated explicitly in the <MISSING PAGE> generate() method.


.. code-block:: python

    from conan.tools.cmake import CMakeToolchain

    class MyLibConan(ConanFile):
        ...

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()


build_policy
------------

Controls when the current package is built during a ``conan install``.
The allowed values are:
    
- ``"missing"``: Conan builds it from source if there is no binary available.
- ``"never"``: This package cannot be built from sources, it is always created with
  ``conan export-pkg``
- ``None`` (default value): This package won't be build unless the policy is specified
  in the command line (e.g ``--build=foo*``)

   .. code-block:: python
      :emphasize-lines: 2

       class PocoTimerConan(ConanFile):
           build_policy = "missing"


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

.. _conan_conanfile_properties_no_copy_source:

no_copy_source
--------------

The attribute ``no_copy_source`` tells the recipe that the source code will not be copied from
the ``source_folder`` to the ``build_folder``. This is mostly an optimization for packages
with large source codebases or header-only, to avoid extra copies.


If you activate it (``no_copy_source=True``), is **mandatory** that the source code must not be modified at all by
the configure or build scripts, as the source code will be shared among all builds.

The recipes should always use ``self.source_folder`` attribute, which will point to the ``build``
folder when ``no_copy_source=False`` and will point to the ``source`` folder when ``no_copy_source=True``.

.. seealso::

    Read  <MISSING PAGE> header-only section for an example using ``no_copy_source`` attribute.


.. _conan_conanfile_properties_folders:

.. _conan_conanfile_properties_source_folder:

source_folder
-------------

The folder in which the source code lives. The path is built joining the base directory
(a cache directory when running in the cache or the ``output folder`` when running locally)
with the value of ``folders.source`` if declared in the ``layout()`` method.

Note that the base directory for the ``source_folder`` when running in the cache will point to the base folder of the
build unless :ref:`no_copy_source<conan_conanfile_properties_no_copy_source>` is set to ``True``. But anyway it will
always point to the correct folder where the source code is.


export_sources_folder
---------------------

The value depends on the method you access it:

- At ``source(self)``: Points to the base source folder (that means self.source_folder but
  without taking into account the ``folders.source`` declared in the ``layout()`` method).
  The declared `exports_sources` are copied to that base source folder always.
- At ``exports_sources(self)``: Points to the folder in the cache where the export sources
  have to be copied.

.. seealso::

    - Read  <MISSING PAGE> ``export_sources`` method.
    - Read  <MISSING PAGE> ``source`` method.

.. _attribute_build_folder:

build_folder
------------

The folder used to build the source code. The path is built joining the base directory (a cache
directory when running in the cache or the ``output folder`` when running locally) with
the value of ``folders.build`` if declared in the ``layout()`` method.

.. _conan_conanfile_properties_package_folder:

package_folder
--------------

The folder to copy the final artifacts for the binary package. In the local cache a package
folder is created for every different package ID.

The most common usage of ``self.package_folder`` is to ``copy`` the files at the <MISSING PAGE> package() method:

.. code-block:: python

   import os
   from conan import ConanFile
   from conan.tools.files import copy

   class MyRecipe(ConanFile):
       ...

       def package(self):
           copy(self, "*.so", self.build_folder, os.path.join(self.package_folder, "lib"))
           ...


recipe_folder
-------------

The folder where the recipe *conanfile.py* is stored, either in the local folder or in
the cache. This is useful in order to access files that are exported along with the recipe,
or the origin folder when exporting files in ``export(self)`` and ``export_sources(self)``
methods.

The most common usage of ``self.recipe_folder`` is in the ``export(self)`` and ``export_sources(self)`` methods,
as the folder from where we copy the files:

.. code-block:: python

   from conan import ConanFile
   from conan.tools.files import copy

   class MethodConan(ConanFile):
       exports = "file.txt"
       def export(self):
           copy(self, "LICENSE.md", self.recipe_folder, self.export_folder)


.. _conan_conanfile_attributes_folders:

folders
-------

The ``folders`` attribute has to be set only in the ``layout()`` method. Please check the
:ref:`layout() method documentation<layout_folders_reference>` to learn more about this
attribute.


.. _conan_conanfile_attributes_cpp:

cpp
---

Object storing all the information needed by the consumers
of a package: include directories, library names, library paths... Both for editable
and regular packages in the cache. It is only available at the ``layout()`` method.

- ``self.cpp.package``: For a regular package being used from the Conan cache. Same as
  declaring ``self.cpp_info`` at the ``package_info()`` method.
- ``self.cpp.source``: For "editable" packages, to describe the artifacts under
  ``self.source_folder``
- ``self.cpp.build``: For "editable" packages, to describe the artifacts under
  ``self.build_folder``.


The ``cpp`` attribute has to be set only in the ``layout()`` method. Please check the
:ref:`layout() method documentation<layout_cpp_reference>` to learn more about this
attribute.


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

info
----

Object used exclusively in ``package_id()`` method:

- The <MISSING PAGE> ``package(self)`` method to control the unique ID for a package:

     .. code-block:: python

        def package_id(self):
            self.info.clear()


.. _revision_mode_attribute:

revision_mode
-------------

This attribute allow each recipe to declare how the revision for the recipe itself should
be computed. It can take two different values:

- ``"hash"`` (by default): Conan will use the checksum hash of the recipe manifest to
  compute the revision for the recipe.
- ``"scm"``: the commit ID will be used as the recipe revision if it belongs to a known
  repository system (Git or SVN). If there is no repository it will raise an error.

python_requires
---------------

This class attribute allows to define a dependency to another Conan recipe and reuse its code.
Its basic syntax is:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel"  # recipe to reuse code from

        def build(self):
            self.python_requires["pyreq"].module # access to the whole conanfile.py module
            self.python_requires["pyreq"].module.myvar  # access to a variable
            self.python_requires["pyreq"].module.myfunct()  # access to a global function
            self.python_requires["pyreq"].path # access to the folder where the reused file is


Read more about this attribute in :ref:`reference_extensions_python_requires`


python_requires_extend
----------------------

This class attribute defines one or more classes that will be injected in runtime as base classes of
the recipe class. Syntax for each of these classes should be a string like ``pyreq.MyConanfileBase``
where the ``pyreq`` is the name of a ``python_requires`` and ``MyConanfileBase`` is the name of the class
to use.

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel", "utils/0.1@user/channel"
        python_requires_extend = "pyreq.MyConanfileBase", "utils.UtilsBase"  # class/es to inject



.. _conan_conanfile_properties_conandata:

conan_data
----------

Read only attribute with a dictionary with the keys and values provided in a <MISSING PAGE> conandata_yml file format placed
next to the *conanfile.py*. This YAML file is automatically exported with the recipe and automatically loaded with it too.

You can declare information in the *conandata.yml* file and then access it inside any of the methods of the recipe.
For example, a *conandata.yml* with information about sources that looks like this:

.. code-block:: YAML

    sources:
      "1.1.0":
        url: "https://www.url.org/source/mylib-1.0.0.tar.gz"
        sha256: "8c48baf3babe0d505d16cfc0cf272589c66d3624264098213db0fb00034728e9"
      "1.1.1":
        url: "https://www.url.org/source/mylib-1.0.1.tar.gz"
        sha256: "15b6393c20030aab02c8e2fe0243cb1d1d18062f6c095d67bca91871dc7f324a"

.. code-block:: python

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])


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


win_bash
--------

When ``True`` it enables the new run in a subsystem bash in Windows mechanism.

.. code-block:: python

    from conan import ConanFile

    class FooRecipe(ConanFile):
        ...
        win_bash = True


It can also be declared as a ``property`` based on any condition:

.. code-block:: python

    from conan import ConanFile

    class FooRecipe(ConanFile):
        ...


        @property
        def win_bash(self):
            return self.settings.arch == "armv8"

win_bash_run
------------

When ``True`` it enables running commands in the ``"run"`` scope, to run them inside a bash shell.

.. code-block:: python

    from conan import ConanFile

    class FooRecipe(ConanFile):

        ...

        win_bash_run = True
        def build(self):
            self.run(cmd, scope="run")  # will run <cmd> inside bash
