.. spelling::

  ing
  ver

.. currentmodule:: conan

.. _conan_conanfile_attributes:

Attributes
==========


name
----

.. autoattribute:: ConanFile.name


   A valid name has:

    - A minimum of 2 and a maximum of 101 characters (though shorter names are recommended).
    - Matches the following regex ``^[a-z0-9_][a-z0-9_+.-]{1,100}$``: so starts with alphanumeric or ``_``,
      then from 1 to 100 characters between alphanumeric, ``_``, ``+``, ``.`` or ``-``.

   The name is only necessary for ``export``-ing the recipe into the local cache (``export`` and ``create`` commands),
   if they are not defined in the command line.


version
-------

.. autoattribute:: ConanFile.version

   A valid version follows the same rules than the ``name`` attribute.
   In case the version follows semantic versioning in the form ``X.Y.Z-pre1+build2``, that value might be used for requiring
   this package through version ranges instead of exact versions.

   The version is only strictly necessary for ``export``-ing the recipe into the local cache (``export`` and ``create`` commands),
   if they are not defined in the command line.

.. _reference_conanfile_attributes_package_type:

package_type
------------

.. autoattribute:: ConanFile.package_type



description
-----------

.. autoattribute:: ConanFile.description


   This is an optional, but strongly recommended text field, containing the description of the package,
   and any information that might be useful for the consumers. The first line might be used as a
   short description of the package.

   .. code-block:: python

       class HelloConan(ConanFile):
           name = "hello"
           version = "0.1"
           description = """This is a Hello World library.
                           A fully featured, portable, C++ library to say Hello World in the stdout,
                           with incredible iostreams performance"""

homepage
--------

.. autoattribute:: ConanFile.homepage

   Used to link the recipe to further explanations of the library itself like an overview of its features, documentation, FAQ
   as well as other related information.

   .. code-block:: python

       class EigenConan(ConanFile):
           name = "eigen"
           version = "3.3.4"
           homepage = "http://eigen.tuxfamily.org"


url
---

.. autoattribute:: ConanFile.url

   .. code-block:: python

       class HelloConan(ConanFile):
           name = "hello"
           version = "0.1"
           url = "https://github.com/conan-io/hello.git"


license
-------

.. autoattribute:: ConanFile.license

   This will help people wanting to automate license compatibility checks, like consumers of your
   package, or you if your package has Open-Source dependencies.

   .. code-block:: python

       class HelloConan(ConanFile):
           name = "hello"
           version = "0.1"
           license = "MIT"



author
------

.. autoattribute:: ConanFile.author


   .. code-block:: python

       class HelloConan(ConanFile):
           name = "hello"
           version = "0.1"
           author = "John J. Smith (john.smith@company.com)"



topics
------

.. autoattribute:: ConanFile.topics

   .. code-block:: python

       class ProtocInstallerConan(ConanFile):
           name = "protoc_installer"
           version = "0.1"
           topics = ("protocol-buffers", "protocol-compiler", "serialization", "rpc")



user, channel
-------------

.. autoattribute:: ConanFile.user

    A valid string for the ``user`` field follows the same rules than the ``name`` attribute.
    This is an optional attribute. It is sometimes used to identify a forked recipe, giving a different namespace
    to the recipe reference.

.. autoattribute:: ConanFile.channel

   A valid string for the ``channel`` field follows the same rules than the ``name`` attribute.
   This is an optional attribute. It is sometimes used to identify a maturity of the package (stable, testing...).


   The value of these fields can be accessed from within a ``conanfile.py``:

   .. code-block:: python

       from conans import ConanFile

       class HelloConan(ConanFile):
           name = "hello"
           version = "0.1"

           def requirements(self):
               self.requires("common-lib/version")
               if self.user and self.channel:
                   # If the recipe is using them, I want to consume my fork.
                   self.requires("say/0.1@%s/%s" % (self.user, self.channel))
               else:
                   # otherwise, I'll consume the community one
                   self.requires("say/0.1")

   Only packages that have already been exported (packages in the local cache or in a remote server)
   can have a user/channel assigned. For package recipes working in the user space, there is no
   current user/channel by default, although they can be defined at :command:`conan install` time with:

   .. code-block:: bash

       $ conan install <path to conanfile.py> --user my_user --channel my_channel


.. _conan_conanfile_properties_settings:

settings
--------

.. autoattribute:: ConanFile.settings


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

   The ``get_safe()`` method will return ``None`` if that setting or sub-setting doesn't exist and there is no default
   value assigned.

   .. seealso::

      - Removing settings in the ``package_id()`` method. <MISSING PAGE>


.. _conan_conanfile_properties_options:

options
-------

.. autoattribute:: ConanFile.options

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

   .. seealso::

      - Read the :ref:`Getting started, creating packages<creating_packages_create_your_first_conan_package>` to know how to declare and how to
        define a value to an option.
      - Removing options in the ``package_id()`` method. <MISSING PAGE>
      - About the package_type and how it plays when a ``shared`` option is declared. <MISSING PAGE>



.. _conan_conanfile_properties_default_options:

default_options
---------------

.. autoattribute:: ConanFile.default_options


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

.. autoattribute:: ConanFile.requires


    .. code-block:: python

        class MyLibConan(ConanFile):
            requires = "hello/1.0", "OtherLib/2.1@otheruser/testing"


  You can specify version ranges, the syntax is using brackets:

    .. _version_ranges_reference:


    ..  code-block:: python

        class HelloConan(ConanFile):
            requires = "pkg/[>1.0 <1.8]"


  Accepted expressions would be:

    ..  code-block:: python

          >1.1 <2.1    # In such range
          2.8          # equivalent to =2.8
          ~=3.0        # compatible, according to semver
          >1.1 || 0.8  # conditions can be OR'ed


  .. seealso::

       - Check <MISSING PAGE> version_ranges if you want to learn more about version ranges.
       - Check <MISSING PAGE> requires() conanfile.py method.

tool_requires
--------------

.. autoattribute:: ConanFile.tool_requires


  .. code-block:: python

     class MyPkg(ConanFile):
         tool_requires = "tool_a/0.2", "tool_b/0.2@user/testing"


  This is the declarative way to add ``tool_requires``. Check the <MISSING PAGE> tool_requires()
  conanfile.py method to learn a more flexible way to add them.


build_requires
--------------

.. autoattribute:: ConanFile.build_requires


  .. code-block:: python

    class MyPkg(ConanFile):
        build_requires = ["my_build_scripts/1.3",]




  This is the declarative way to add ``build_requires``. Check the <MISSING PAGE> build_requires()
  conanfile.py method to learn a more flexible way to add them.


test_requires
--------------

.. autoattribute:: ConanFile.test_requires


  .. code-block:: python

     class MyPkg(ConanFile):
        test_requires = "gtest/1.11.0", "other_test_tool/0.2@user/testing"


  This is the declarative way to add ``test_requires``. Check the <MISSING PAGE> test_requires()
  conanfile.py method to learn a more flexible way to add them.


.. _exports_attribute:

exports
-------


.. autoattribute:: ConanFile.exports


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

.. autoattribute:: ConanFile.exports_sources

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

.. autoattribute:: ConanFile.generators

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



   .. warning::

      Do not specify the same generator in the ``generators`` attribute and at the ``generate()`` method at the same
      recipe, Conan will use both and unexpected results might happen.

build_policy
------------

.. autoattribute:: ConanFile.build_policy

   .. code-block:: python
      :emphasize-lines: 2

       class PocoTimerConan(ConanFile):
           build_policy = "always" # "missing"


.. _conan_conanfile_properties_no_copy_source:

no_copy_source
--------------

.. autoattribute:: ConanFile.no_copy_source


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

.. autoattribute:: ConanFile.source_folder

   Note that the base directory for the ``source_folder`` when running in the cache will point to the base folder of the
   build unless :ref:`no_copy_source<conan_conanfile_properties_no_copy_source>` is set to ``True``. But anyway it will
   always point to the correct folder where the source code is.


export_sources_folder
---------------------

.. autoattribute:: ConanFile.export_sources_folder

   .. seealso::

      - Read  <MISSING PAGE> ``export_sources`` method.
      - Read  <MISSING PAGE> ``source`` method.

.. _attribute_build_folder:

build_folder
------------

.. autoattribute:: ConanFile.build_folder


.. _conan_conanfile_properties_package_folder:

package_folder
--------------

.. autoattribute:: ConanFile.package_folder

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

.. autoattribute:: ConanFile.recipe_folder

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

<MISSING REFERENCE>

The ``folders`` attribute has to be set only in the ``layout()`` method.

   - **self.folders.source**: To specify a folder where your sources are.
   - **self.folders.build**: To specify a subfolder where the files from the build are (or will be).
   - **self.folders.generators**: To specify a subfolder where to write the files from the generators and the toolchains
     (e.g. the `xx-config.cmake` files from the ``CMakeDeps`` generator).
   - **self.folders.imports**: To specify a subfolder where to write the files copied when using the ``imports(self)``
     method in a ``conanfile.py``.
   - **self.folders.root**: To specify the relative path from the ``conanfile.py`` to the root of the project, in case
     the ``conanfile.py`` is in a subfolder and not in the project root. If defined, all the other paths will be relative to
     the project root, not to the location of the ``conanfile.py``.

   .. seealso::

       Read more about the usage of the ``layout()`` in :ref:`this tutorial<consuming_packages_flexibility_of_conanfile_py_use_layout>`.


.. _conan_conanfile_attributes_cpp:

cpp
---

.. autoattribute:: ConanFile.cpp

   .. seealso::

       Read more about the :ref:`CppInfo<conan_conanfile_model_cppinfo>` model.


   .. important::

       This attribute should be only filled in the <MISSING METHOD> ``layout()`` method.


cpp_info
--------

.. autoattribute:: ConanFile.cpp_info


   .. seealso::

       Read more about the :ref:`CppInfo<conan_conanfile_model_cppinfo>` model.


   .. important::

       This attribute is only defined inside ``package_info()`` method being `None` elsewhere.



buildenv_info
-------------

.. autoattribute:: ConanFile.buildenv_info


  .. important::

   This attribute is only defined inside ``package_info()`` method being `None` elsewhere.

  .. code-block:: python

        def package_info(self):
            self.buildenv_info.append_path("PATH", self.package_folder)


  .. seealso::

    Check the reference of the :ref:`Environment<conan_tools_env_environment_model>` object to know how to fill
    the ``self.buildenv_info``.


runenv_info
-----------

.. autoattribute:: ConanFile.runenv_info


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

.. autoattribute:: ConanFile.conf_info


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

Object used in:

- The <MISSING PAGE> ``validate(self)`` method to check if a current configuration of the package is correct or not:

    .. code-block:: python

        def validate(self):
            if self.info.settings.os == "Windows":
                raise ConanInvalidConfiguration("Package does not work in Windows!")

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

    from conans import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel"  # recipe to reuse code from

        def build(self):
            self.python_requires["pyreq"].module # access to the whole conanfile.py module
            self.python_requires["pyreq"].module.myvar  # access to a variable
            self.python_requires["pyreq"].module.myfunct()  # access to a global function
            self.python_requires["pyreq"].path # access to the folder where the reused file is


Read more about this attribute in <MISSING PAGE>


python_requires_extend
----------------------

This class attribute defines one or more classes that will be injected in runtime as base classes of
the recipe class. Syntax for each of these classes should be a string like ``pyreq.MyConanfileBase``
where the ``pyreq`` is the name of a ``python_requires`` and ``MyConanfileBase`` is the name of the class
to use.

.. code-block:: python

    from conans import ConanFile

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

.. autoattribute:: ConanFile.deprecated

      For example, the following code:

      .. code-block:: python

          from conans import ConanFile

          class Pkg(ConanFile):
              name = "cpp-taskflow"
              version = "1.0"
              deprecated = True

      may emit a warning like:

      .. code-block:: bash

          cpp-taskflow/1.0: WARN: Recipe 'cpp-taskflow/1.0' is deprecated. Please, consider changing your requirements.

      Optionally, the attribute may specify the name of the suggested replacement:

      .. code-block:: python

          from conans import ConanFile

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

.. autoattribute:: ConanFile.provides


      If Conan encounters two or more libraries providing the same functionality within a single graph, it raises an error:

      .. code-block:: bash

          At least two recipes provides the same functionality:
           - 'libjpeg' provided by 'libjpeg/9d', 'libjpeg-turbo/2.0.5'

      The attribute value should be a string with a recipe name or a tuple of such recipe names.

      For example, to declare that ``libjpeg-turbo`` recipe offers the same functionality as ``libjpeg`` recipe, the following code could be used:

      .. code-block:: python

          from conans import ConanFile

          class LibJpegTurbo(ConanFile):
              name = "libjpeg-turbo"
              version = "1.0"
              provides = "libjpeg"


      To declare that a recipe provides the functionality of several different recipes at the same time, the following code could be used:

      .. code-block:: python

          from conans import ConanFile

          class OpenBLAS(ConanFile):
              name = "openblas"
              version = "1.0"
              provides = "cblas", "lapack"

      If the attribute is omitted, the value of the attribute is assumed to be equal to the current package name. Thus, it's redundant for
      ``libjpeg`` recipe to declare that it provides ``libjpeg``, it's already implicitly assumed by Conan.


win_bash
--------

.. autoattribute:: ConanFile.win_bash



      .. code-block:: python

          from conans import ConanFile

          class FooRecipe(ConanFile):
              ...
              win_bash = True


      It can also be declared as a ``property`` based on any condition:

      .. code-block:: python

          from conans import ConanFile

          class FooRecipe(ConanFile):
              ...


              @property
              def win_bash(self):
                  return self.settings.arch == "armv8"


