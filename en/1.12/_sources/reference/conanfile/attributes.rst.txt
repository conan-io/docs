.. spelling::

  ing
  ver


Attributes
==========

name
----
This is a string, with a minimum of 2 and a maximum of 50 characters (though shorter names are recommended), that defines the package name. It will be the ``<PkgName>/version@user/channel`` of the package reference.
It should match the following regex ``^[a-zA-Z0-9_][a-zA-Z0-9_\+\.-]$``, so start with alphanumeric or underscore, then alphanumeric, underscore, +, ., - characters.

The name is only necessary for ``export``-ing the recipe into the local cache (``export`` and ``create`` commands), if they are not defined in the command line.
It might take its value from an environment variable, or even any python code that defines it (e.g. a function that reads an environment variable, or a file from disk).
However, the most common and suggested approach would be to define it in plain text as a constant, or provide it as command line arguments.


version
-------
The version attribute will define the version part of the package reference: ``PkgName/<version>@user/channel``
It is a string, and can take any value, matching the same constraints as the ``name`` attribute.
In case the version follows semantic versioning in the form ``X.Y.Z-pre1+build2``, that value might be used for requiring this package through version ranges instead of exact versions.

The version is only strictly necessary for ``export``-ing the recipe into the local cache (``export`` and ``create`` commands), if they are not defined in the command line.
It might take its value from an environment variable, or even any python code that defines it (e.g. a function that reads an environment variable, or a file from disk).
Please note that this value might be used in the recipe in other places (as in ``source()`` method to retrieve code from elsewhere), making this value not constant means that it may evaluate differently in different contexts (e.g., on different machines or for different users) leading to unrepeatable or unpredictable results.
The most common and suggested approach would be to define it in plain text as a constant, or provide it as command line arguments.


description
-----------
This is an optional, but strongly recommended text field, containing the description of the package,
and any information that might be useful for the consumers. The first line might be used as a
short description of the package.

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        description = """This is a Hello World library.
                        A fully featured, portable, C++ library to say Hello World in the stdout,
                        with incredible iostreams performance"""

homepage
--------

Use this attribute to indicate the home web page of the library being packaged. This is useful to link
the recipe to further explanations of the library itself like an overview of its features, documentation, FAQ
as well as other related information.

.. code-block:: python

    class EigenConan(ConanFile):
        name = "eigen"
        version = "3.3.4"
        homepage = "http://eigen.tuxfamily.org"

.. _package_url:

url
---

It is possible, even typical, if you are packaging a third party lib, that you just develop
the packaging code. Such code is also subject to change, often via collaboration, so it should be stored
in a VCS like git, and probably put on GitHub or a similar service. If you do indeed maintain such a
repository, please indicate it in the ``url`` attribute, so that it can be easily found.

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        url = "https://github.com/memsharded/hellopack.git"

The ``url`` is the url **of the package** repository, i.e. not necessarily the original source code.
It is optional, but highly recommended, that it points to GitHub, Bitbucket or your preferred
code collaboration platform. Of course, if you have the conanfile inside your library source,
you can point to it, and afterwards use the ``url`` in your ``source()`` method.

This is a recommended, but not mandatory attribute.

license
-------

This field is intended for the license of the **target** source code and binaries, i.e. the code
that is being packaged, not the ``conanfile.py`` itself. This info is used to be displayed by
the :command:`conan info` command and possibly other search and report tools.

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        license = "MIT"

This attribute can contain several, comma separated licenses. It is a text string, so it can
contain any text, including hyperlinks to license files elsewhere.

However, we strongly recommend packagers of Open-Source projects to use
[SPDX](https://spdx.org/) identifiers from the [SPDX license
list](https://spdx.org/licenses/) instead of free-formed text. This will help
people wanting to automate license compatibility checks, like consumers of your
package, or you if your package has Open-Source dependencies.

This is a recommended, but not mandatory attribute.

author
------

Intended to add information about the author, in case it is different from the Conan user. It is
possible that the Conan user is the name of an organization, project, company or group, and many
users have permissions over that account. In this case, the author information can explicitly
define who is the creator/maintainer of the package

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        author = "John J. Smith (john.smith@company.com)"

This is an optional attribute.

topics
------

Topics provide a useful way to group related tags together and to quickly tell developers what a
package is about. Topics also make it easier for customers to find your recipe. It could be useful
to filter packages by topics or to reuse them in Bintray package page.

The ``topics`` attribute should be a tuple with the needed topics inside.

.. code-block:: python

    class ProtocInstallerConan(ConanFile):
        name = "protoc_installer"
        version = "0.1"
        topics = ("protocol-buffers", "protocol-compiler", "serialization", "rpc")

This is an optional attribute.

.. _user_channel:

user, channel
-------------

The fields ``user`` and ``channel`` can be accessed from within a ``conanfile.py``.
Though their usage is usually not encouraged, it could be useful in different cases,
e.g. to define requirements with the same user and
channel than the current package, which could be achieved with something like:

.. code-block:: python

    from conans import ConanFile

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"

        def requirements(self):
            self.requires("Say/0.1@%s/%s" % (self.user, self.channel))

Only package recipes that are in the conan local cache (i.e. "exported") have a user/channel assigned.
For package recipes working in user space, there is no current user/channel by default. They can be
defined at ``conan install`` time with:

.. code-block:: bash

    $ conan install <path to conanfile.py> user/channel

If they are not defined via command line, the properties ``self.user`` and ``self.channel`` will then look 
for environment variables ``CONAN_USERNAME`` and ``CONAN_CHANNEL`` respectively. If they are not defined, 
an error will be raised unless ``default_user`` and ``default_channel`` are declared in the recipe.

.. seealso::

    FAQ: :ref:`faq_recommendation_user_channel`

default_user, default_channel
-----------------------------

For package recipes working in the user space, with local methods like :command:`conan install .` and :command:`conan build .`,
there is no current user/channel. If you are accessing to ``self.user`` or ``self.channel`` in your recipe,
you need to declare the environment variables ``CONAN_USERNAME`` and ``CONAN_CHANNEL`` or you can set the attributes
``default_user`` and ``default_channel``. You can also use python ``@properties``:

.. code-block:: python

    from conans import ConanFile

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        default_user = "myuser"

        @property
        def default_channel(self):
            return "mydefaultchannel"

        def requirements(self):
            self.requires("Pkg/0.1@%s/%s" % (self.user, self.channel))


.. _settings_property:

settings
--------

There are several things that can potentially affect a package being created, i.e. the final
package will be different (a different binary, for example), if some input is different.

Development project-wide variables, like the compiler, its version, or the OS
itself. These variables have to be defined, and they cannot have a default value listed in the
conanfile, as it would not make sense.

It is obvious that changing the OS produces a different binary in most cases. Changing the compiler
or compiler version changes the binary too, which might have a compatible ABI or not, but the
package will be different in any case.

For these reasons, the most common convention among Conan recipes is to distinguish binaries by the following four settings, which is reflected in the `conanfile.py` template used in the `conan new` command:

.. code-block:: python

    settings = "os", "compiler", "build_type", "arch"

When Conan generates a compiled binary for a package with a given combination of the settings above, it generates a unique ID for that binary by hashing the current values of these settings.

But what happens for example to **header only libraries**? The final package for such libraries is not
binary and, in most cases it will be identical, unless it is automatically generating code.
We can indicate that in the conanfile:

.. code-block:: python

   from conans import ConanFile

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        # We can just omit the settings attribute too
        settings = None

        def build(self):
            #empty too, nothing to build in header only

You can restrict existing settings and accepted values as well, by redeclaring the settings
attribute:

.. code-block:: python

    class HelloConan(ConanFile):
        settings = {"os": ["Windows"],
            "compiler": {"Visual Studio": {"version": [11, 12]}},
            "arch": None}

In this example we have just defined that this package only works in Windows, with VS 10 and 11.
Any attempt to build it in other platforms with other settings will throw an error saying so.
We have also defined that the runtime (the MD and MT flags of VS) is irrelevant for us
(maybe we using a universal one?). Using None as a value means, *maintain the original values* in order
to avoid re-typing them. Then, "arch": None is totally equivalent to "arch": ["x86", "x86_64", "arm"]
Check the reference or your ~/.conan/settings.yml file.

As re-defining the whole settings attribute can be tedious, it is sometimes much simpler to
remove or tune specific fields in the ``configure()`` method. For example, if our package is runtime
independent in VS, we can just remove that setting field:

.. code-block:: python

    settings = "os", "compiler", "build_type", "arch"

    def configure(self):
        self.settings.compiler["Visual Studio"].remove("runtime")

.. _conanfile_options:

options
-------

Conan packages recipes can generate different binary packages when different settings are used, but can also customize, per-package any other configuration that will produce a different binary.

A typical option would be being shared or static for a certain library. Note that this is optional, different packages can have this option, or not (like header-only packages), and different packages can have different values for this option, as opposed to settings, which typically have the same values for all packages being installed (though this can be controlled too, defining different settings for specific packages)

Options are defined in package recipes as dictionaries of name and allowed values:

.. code-block:: python

    class MyPkg(ConanFile):
        ...
        options = {"shared": [True, False]}

Options are defined as a python dictionary inside the ``ConanFile`` where each key must be a
string with the identifier of the option and the value be a list with all the possible option
values:

.. code-block:: python

    class MyPkg(ConanFile):
        ...
        options = {"shared": [True, False],
                   "option1": ["value1", "value2"],}

Values for each option can be typed or plain strings, and there is a special value, ``ANY``, for
options that can take any value.

The attribute ``default_options`` has the purpose of defining the default values for the options
if the consumer (consuming recipe, project, profile or the user through the command line) does
not define them. It is worth noticing that **an uninitialized option will get the value** ``None``
**and it will be a valid value if its contained in the list of valid values**. This attribute
should be defined as a python dictionary too, although other definitions could be valid for
legacy reasons.

.. code-block:: python

    class MyPkg(ConanFile):
        ...
        options = {"shared": [True, False],
                   "option1": ["value1", "value2"],
                   "option2": "ANY"}
        default_options = {"shared": True,
                           "option1": "value1",
                           "option2": 42}

        def build(self):
            shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
            cmake = CMake(self)
            self.run("cmake . %s %s" % (cmake.command_line, shared))
            ...

.. tip::

    - You can inspect available package options reading the package recipe, which can be
      done with the command :command:`conan inspect MyPkg/0.1@user/channel`.
    - Options ``"shared": [True, False]`` and ``"fPIC": [True, False]`` are automatically managed in :ref:`cmake_reference` and
      :ref:`autotools_reference` build helpers.

As we mentioned before, values for options in a recipe can be defined using different ways, let's
go over all of them for the example recipe ``MyPkg`` defined above:

- Using the attribute ``default_options`` in the recipe itself.
- In the ``default_options`` of a recipe that requires this one: the values defined here
  will override the default ones in the recipe.

  .. code-block:: python

      class OtherPkg(ConanFile):
          requires = "MyPkg/0.1@user/channel"
          default_options = {"MyPkg:shared": False}

  Of course, this will work in the same way working with a *conanfile.txt*:

  .. code-block:: text

      [requires]
      MyPkg/0.1@user/channel

      [options]
      MyPkg:shared=False

- It is also possible to define default values for the options of a recipe using
  :ref:`profiles<profiles>`. They will apply whenever that recipe is used:

  .. code-block:: text

      # file "myprofile"
      # use it as $ conan install -pr=myprofile
      [settings]
      setting=value

      [options]
      MyPkg:shared=False

- Last way of defining values for options, with the highest priority over them all, is to pass
  these values using the command argument :command:`-o` in the command line:

  .. code-block:: bash

    $ conan install . -o MyPkg:shared=True -o OtherPkg:option=value

Values for options can be also conditionally assigned (or even deleted) in the methods
``configure()`` and ``config_options()``, the
:ref:`corresponding section<method_configure_config_options>` has examples documenting these
use cases. However, conditionally assigning values to options can have it drawbacks as it is
explained in the :ref:`mastering section<conditional_settings_options_requirements>`.

One important notice is how these options values are evaluated and how the different conditionals
that we can implement in Python will behave. As seen before, values for options can be defined
in Python code (assigning a dictionary to ``default_options``) or through strings (using a
``conanfile.txt``, a profile file, or through the command line). In order to provide a
consistent implementation take into account these considerations:

- Evaluation for the typed value and the string one is the same, so all these inputs would
  behave the same:

    - ``default_options = {"shared": True, "option": None}``
    - ``default_options = {"shared": "True", "option": "None"}``
    - ``MyPkg:shared=True``, ``MyPkg:option=None`` on profiles, command line or *conanfile.txt*

- **Implicit conversion to boolean is case insensitive**, so the
  expression ``bool(self.options.option)``:

    - equals ``True`` for the values ``True``, ``"True"`` and ``"true"``, and any other value that
      would be evaluated the same way in Python code.
    - equals ``False`` for the values ``False``, ``"False"`` and ``"false"``, also for the empty
      string and for ``0`` and ``"0"`` as expected.

- Comparison using ``is`` is always equals to ``False`` because the types would be different as
  the option value is encapsulated inside a Conan class.

- Explicit comparisons with the ``==`` symbol **are case sensitive**, so:

    - ``self.options.option = "False"`` satisfies ``assert self.options.option == False``,
      ``assert self.options.option == "False"``, but ``assert self.options.option != "false"``.

- A different behavior has ``self.options.option = None``, because
  ``assert self.options.option != None``.


.. _conanfile_default_options:

default_options
---------------

As you have seen in the examples above, recipe's default options are declared as a dictionary with the initial desired value of the options.
However, you can also specify default option values of the required dependencies:

.. code-block:: python

    class OtherPkg(ConanFile):
        requires = "Pkg/0.1@user/channel"
        default_options = {"Pkg:pkg_option": "value"}

And it also works with default option values of conditional required dependencies:

.. code-block:: python

    class OtherPkg(ConanFile):
        default_options = {"Pkg:pkg_option": "value"}

        def requirements(self):
            if self.settings.os != "Windows":
                self.requires("Pkg/0.1@user/channel")

For this example running in Windows, the `default_options` for the `Pkg/0.1@user/channel` will be ignored, they will only be used on every
other OS.

You can also set the options conditionally to a final value with ``config_options()`` instead of using ``default_options``:

.. code-block:: python

    class OtherPkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        options = {"some_option": [True, False]}
        # Do NOT declare 'default_options', use 'config_options()'

        def config_options(self):
            if self.options.some_option == None:
                if self.settings.os == 'Android':
                    self.options.some_option = True
                else:
                    self.options.some_option = False

.. important::

    Setting options conditionally without a default value works only to define a default value if not defined in command line. However,
    doing it this way will assign a final value to the option and not an initial one, so those option values will not be overridable from
    downstream dependent packages.

.. important::

    Default options can be specified as a dictionary only for Conan version >= 1.8.

.. seealso::

    Read more about the :ref:`config_options()<method_configure_config_options>` method.

requires
--------

Specify package dependencies as a list of other packages:

.. code-block:: python

    class MyLibConan(ConanFile):
        requires = "Hello/1.0@user/stable", "OtherLib/2.1@otheruser/testing"

You can specify further information about the package requirements:

.. code-block:: python

    class MyLibConan(ConanFile):
        requires = (("Hello/0.1@user/testing"),
                    ("Say/0.2@dummy/stable", "override"),
                    ("Bye/2.1@coder/beta", "private"))

Requirements can be complemented by 2 different parameters:

**private**: a dependency can be declared as private if it is going to be fully embedded and hidden
from consumers of the package. Typical examples could be a header only library which is not exposed
through the public interface of the package, or the linking of a static library inside a dynamic
one, in which the functionality or the objects of the linked static library are not exposed through
the public interface of the dynamic library.

**override**: packages can define overrides of their dependencies, if they require the definition of
specific versions of the upstream required libraries, but not necessarily direct dependencies. For example,
a package can depend on A(v1.0), which in turn could conditionally depend on Zlib(v2), depending on whether
the compression is enabled or not. Now, if you want to force the usage of Zlib(v3) you can:

..  code-block:: python

    class HelloConan(ConanFile):
        requires = ("A/1.0@user/stable", ("Zlib/3.0@other/beta", "override"))

This **will not introduce a new dependency**, it will just change Zlib v2 to v3 if A actually
requires it. Otherwise Zlib will not be a dependency of your package.

.. _version_ranges_reference:

version ranges
++++++++++++++

The syntax is using brackets:

..  code-block:: python

    class HelloConan(ConanFile):
        requires = "Pkg/[>1.0 <1.8]@user/stable"

Expressions are those defined and implemented by [python node-semver](https://pypi.org/project/node-semver/). Accepted expressions would be:

..  code-block:: python

    >1.1 <2.1    # In such range
    2.8          # equivalent to =2.8
    ~=3.0        # compatible, according to semver
    >1.1 || 0.8  # conditions can be OR'ed


.. container:: out_reference_box

    Go to :ref:`Mastering/Version Ranges<version_ranges>` if you want to learn more about version ranges.

build_requires
--------------

Build requirements are requirements that are only installed and used when the package is built from sources. If there is an existing pre-compiled binary, then the build requirements for this package will not be retrieved.

They can be specified as a comma separated tuple in the package recipe:

.. code-block:: python

    class MyPkg(ConanFile):
        build_requires = "ToolA/0.2@user/testing", "ToolB/0.2@user/testing"

Read more: :ref:`Build requirements <build_requires>`

.. _exports_attribute:

exports
-------

If a package recipe ``conanfile.py`` requires other external files, like other python files that
it is importing (python importing), or maybe some text file with data it is reading, those files
must be exported with the ``exports`` field, so they are stored together, side by side with the
``conanfile.py`` recipe.

The ``exports`` field can be one single pattern, like ``exports="*"``, or several inclusion patterns.
For example, if we have some python code that we want the recipe to use in a ``helpers.py`` file,
and have some text file, ``info.txt``, we want to read and display during the recipe evaluation
we would do something like:

.. code-block:: python

    exports = "helpers.py", "info.txt"

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

    exports = "*.py", "!*tmp.py"

This is an optional attribute, only to be used if the package recipe requires these other files
for evaluation of the recipe.

.. _exports_sources_attribute:

exports_sources
---------------
There are 2 ways of getting source code to build a package. Using the ``source()`` recipe method
and using the ``exports_sources`` field. With ``exports_sources`` you specify which sources are required,
and they will be exported together with the **conanfile.py**, copying them from your folder to the
local conan cache. Using ``exports_sources``
the package recipe can be self-contained, containing the source code like in a snapshot, and then
not requiring downloading or retrieving the source code from other origins (git, download) with the
``source()`` method when it is necessary to build from sources.

The ``exports_sources`` field can be one single pattern, like ``exports_sources="*"``, or several inclusion patterns.
For example, if we have the source code inside "include" and "src" folders, and there are other folders
that are not necessary for the package recipe, we could do:

.. code-block:: python

    exports_sources = "include*", "src*"

Exclude patterns are also possible, with the ``!`` prefix:

.. code-block:: python

    exports_sources = "include*", "src*", "!src/build/*"

This is an optional attribute, used typically when ``source()`` is not specified. The main difference with
``exports`` is that ``exports`` files are always retrieved (even if pre-compiled packages exist),
while ``exports_sources`` files are only retrieved when it is necessary to build a package from sources.

generators
----------

Generators specify which is the output of the ``install`` command in your project folder. By default, a *conanbuildinfo.txt* file is
generated, but you can specify different generators and even use more than one.

.. code-block:: python

    class MyLibConan(ConanFile):
        generators = "cmake", "gcc"

Check the full :ref:`generators list<generators>`.

.. _attribute_build_stages:

should_configure, should_build, should_install, should_test
-----------------------------------------------------------

Read only variables defaulted to ``True``.

These variables allow you to control the build stages of a recipe during a :command:`conan build` command with the optional arguments
:command:`--configure`/:command:`--build`/:command:`--install`/:command:`--test`. For example, consider this ``build()`` method:

.. code-block:: python

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
        cmake.test()

If nothing is specified, all four methods will be called. But using command line arguments, this can be changed:

.. code-block:: bash

    $ conan build . --configure  # only run cmake.configure(). Other methods will do nothing
    $ conan build . --build      # only run cmake.build(). Other methods will do nothing
    $ conan build . --install    # only run cmake.install(). Other methods will do nothing
    $ conan build . --test       # only run cmake.test(). Other methods will do nothing
    # They can be combined
    $ conan build . -c -b # run cmake.configure() + cmake.build(), but not cmake.install() nor cmake.test()

Autotools and Meson helpers already implement the same functionality. For other build systems, you can use these variables in the
``build()`` method:

.. code-block:: python

    def build(self):
        if self.should_configure:
            # Run my configure stage
        if self.should_build:
            # Run my build stage
        if self.should_install: # If my build has install, otherwise use package()
            # Run my install stage
        if self.should_test:
            # Run my test stage

Note that the ``should_configure``, ``should_build``, ``should_install``, ``should_test`` variables will always be ``True`` while building in
the cache and can be only modified for the local flow with :command:`conan build`.

build_policy
------------

With the ``build_policy`` attribute the package creator can change the default conan's build behavior.
The allowed ``build_policy`` values are:

- ``missing``: If no binary package is found, Conan will build it without the need to invoke :command:`conan install --build missing` option.
- ``always``: The package will be built always, **retrieving each time the source code** executing the "source" method.

.. code-block:: python
   :emphasize-lines: 2

    class PocoTimerConan(ConanFile):
        build_policy = "always" # "missing"

.. _short_paths_reference:

short_paths
-----------

This attribute is specific to Windows, and ignored on other operating systems.
It tells Conan to workaround the limitation of 260 chars in Windows paths.

.. important::

    Since Windows 10 (ver. 10.0.14393), it is possible to `enable long paths at the system level
    <https://docs.microsoft.com/es-es/windows/desktop/FileIO/naming-a-file#maximum-path-length-limitation>`_.
    Latest python 2.x and 3.x installers enable this by default. With the path limit removed both on the OS
    and on Python, the ``short_paths`` functionality becomes unnecessary, and may be disabled explicitly
    through the ``CONAN_USER_HOME_SHORT`` environment variable.

Enabling short paths management will "link" the ``source`` and ``build`` directories of the package to the drive root, something like
``C:\.conan\tmpdir``. All the folder layout in the local cache is maintained.

Set ``short_paths=True`` in your *conanfile.py*:

..  code-block:: python

    from conans import ConanFile

    class ConanFileTest(ConanFile):
        ...
        short_paths = True

.. seealso::

    There is an :ref:`environment variable <env_vars>` ``CONAN_USE_ALWAYS_SHORT_PATHS`` to globally enable this behavior for all packages.

.. _no_copy_source:

no_copy_source
--------------

The attribute ``no_copy_source`` tells the recipe that the source code will not be copied from the ``source`` folder to the ``build`` folder.
This is mostly an optimization for packages with large source codebases, to avoid extra copies. It is **mandatory** that the source code must not be modified at all by the configure or build scripts, as the source code will be shared among all builds.

To be able to use it, the package recipe can access the ``self.source_folder`` attribute, which will point to the ``build`` folder when ``no_copy_source=False`` or not defined, and will point to the ``source`` folder when ``no_copy_source=True``

When this attribute is set to True, the ``package()`` method will be called twice, one copying from the ``source`` folder and the other copying from the ``build`` folder.

.. _folders_attributes_reference:

.. _attribute_source_folder:

source_folder
-------------

The folder in which the source code lives.

When a package is built in the Conan local cache its value is the same as the ``build`` folder by default. This is due to the fact that the
source code is copied from the ``source`` folder to the ``build`` folder to ensure isolation and avoiding modifications of shared common
source code among builds for different configurations. Only when ``no_copy_source=True`` this folder will actually point to the package
``source`` folder in the local cache.

When executing Conan commands in the :ref:`package_dev_flow` like :command:`conan source`, this attribute will be pointing to the folder
specified in the command line.

.. _attribute_install_folder:

install_folder
--------------

The folder in which the installation of packages outputs the generator files with the information of dependencies.
By default in the the local cache its value is the same as ``self.build_folder`` one.

When executing Conan commands in the :ref:`package_dev_flow` like :command:`conan install` or :command:`conan build`, this attribute will
be pointing to the folder specified in the command line.

.. _attribute_build_folder:

build_folder
------------

The folder used to build the source code. In the local cache a build folder is created with the name of the package ID that will be built.

When executing Conan commands in the :ref:`package_dev_flow` like :command:`conan build`, this attribute will be pointing to the folder
specified in the command line.

.. _attribute_package_folder:

package_folder
--------------

The folder to copy the final artifacts for the binary package. In the local cache a package folder is created for every different package
ID.

When executing Conan commands in the :ref:`package_dev_flow` like :command:`conan package`, this attribute will be pointing to the folder
specified in the command line.

.. _cpp_info_attributes_reference:

cpp_info
--------

.. important::

    This attribute is only defined inside ``package_info()`` method being `None` elsewhere.

The ``self.cpp_info`` is responsible for storing all the information needed by consumers of a package: include directories, library names,
library paths... There are some default values that will be applied automatically if not indicated otherwise.

This object should be filled in ``package_info()`` method.

+--------------------------------+---------------------------------------------------------------------------------------------------------+
| NAME                           | DESCRIPTION                                                                                             |
+================================+=========================================================================================================+
| self.cpp_info.includedirs      | Ordered list with include paths. Defaulted to ``["include"]``                                           |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.libdirs          | Ordered list with lib paths. Defaulted to ``["lib"]``                                                   |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.resdirs          | Ordered list of resource (data) paths. Defaulted to ``["res"]``                                         |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.bindirs          | Ordered list with include paths. Defaulted to ``["bin"]``                                               |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.builddirs        | | Ordered list with build scripts directory paths. Defaulted to ``[""]`` (Package folder directory)     |
|                                | | CMake generators will search in these dirs for files like *findXXX.cmake*                             |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.libs             | Ordered list with the library names, Defaulted to ``[]`` (empty)                                        |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.defines          | Preprocessor definitions. Defaulted to ``[]`` (empty)                                                   |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.cflags           | Ordered list with pure C flags. Defaulted to ``[]`` (empty)                                             |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.cppflags         | Ordered list with C++ flags. Defaulted to ``[]`` (empty)                                                |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.sharedlinkflags  | Ordered list with linker flags (shared libs). Defaulted to ``[]`` (empty)                               |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.exelinkflags     | Ordered list with linker flags (executables). Defaulted to ``[]`` (empty)                               |
+--------------------------------+---------------------------------------------------------------------------------------------------------+
| self.cpp_info.rootpath         | Filled with the root directory of the package, see ``deps_cpp_info``                                    |
+--------------------------------+---------------------------------------------------------------------------------------------------------+

The paths of the directories in the directory variables indicated above are relative to the
:ref:`self.package_folder<folders_attributes_reference>` directory.

.. seealso::

    Read :ref:`method_package_info` for more info.

.. _deps_cpp_info_attributes_reference:

deps_cpp_info
-------------

Contains the ``cpp_info`` object of the requirements of the recipe. In addition of the above fields, there are also properties to obtain the
absolute paths:

+-------------------------------------------+---------------------------------------------------------------------+
| NAME                                      | DESCRIPTION                                                         |
+===========================================+=====================================================================+
| self.cpp_info.include_paths               | Same as ``includedirs`` but transformed to absolute paths           |
+-------------------------------------------+---------------------------------------------------------------------+
| self.cpp_info.lib_paths                   | Same as ``libdirs`` but transformed to absolute paths               |
+-------------------------------------------+---------------------------------------------------------------------+
| self.cpp_info.bin_paths                   | Same as ``bindirs`` but transformed to absolute paths               |
+-------------------------------------------+---------------------------------------------------------------------+
| self.cpp_info.build_paths                 | Same as ``builddirs`` but transformed to absolute paths             |
+-------------------------------------------+---------------------------------------------------------------------+
| self.cpp_info.res_paths                   | Same as ``resdirs`` but transformed to absolute paths               |
+-------------------------------------------+---------------------------------------------------------------------+

To get a list of all the dependency names from ```deps_cpp_info```, you can call the `deps` member:

.. code-block:: python

    class PocoTimerConan(ConanFile):
        ...
        def build(self):
            # deps is a list of package names: ["Poco", "zlib", "OpenSSL"]
            deps = self.deps_cpp_info.deps

It can be used to get information about the dependencies, like used compilation flags or the
root folder of the package:

.. code-block:: python
   :emphasize-lines: 8, 11, 14

    class PocoTimerConan(ConanFile):
        ...
        requires = "zlib/1.2.11@conan/stable", "OpenSSL/1.0.2l@conan/stable"
        ...

        def build(self):
            # Get the directory where zlib package is installed
            self.deps_cpp_info["zlib"].rootpath

            # Get the absolute paths to zlib include directories (list)
            self.deps_cpp_info["zlib"].include_paths

            # Get the sharedlinkflags property from OpenSSL package
            self.deps_cpp_info["OpenSSL"].sharedlinkflags

env_info
--------

This attribute is only defined inside ``package_info()`` method, being None elsewhere, so please use it only inside this method.

The ``self.env_info`` object can be filled with the environment variables to be declared in the packages reusing the recipe.

.. seealso::

    Read :ref:`package_info() method docs <method_package_info>` for more info.



.. _deps_env_info_attributes_reference:

deps_env_info
-------------

You can access to the declared environment variables of the requirements of the recipe.

**Note:** The environment variables declared in the requirements of a recipe are automatically applied
and it can be accessed with the python ``os.environ`` dictionary. Nevertheless if
you want to access to the variable declared by some specific requirement you can use the ``self.deps_env_info`` object.

.. code-block:: python
   :emphasize-lines: 2

    import os

    class RecipeConan(ConanFile):
        ...
        requires = "package1/1.0@conan/stable", "package2/1.2@conan/stable"
        ...

        def build(self):
            # Get the SOMEVAR environment variable declared in the "package1"
            self.deps_env_info["package1"].SOMEVAR

            # Access to the environment variables globally
            os.environ["SOMEVAR"]



user_info
---------

This attribute is only defined inside ``package_info()`` method, being None elsewhere, so please use it only inside this method.

The ``self.user_info`` object can be filled with any custom variable to be accessed in the packages reusing the recipe.

.. seealso::

    Read :ref:`package_info() method docs <method_package_info>` for more info.

.. _deps_user_info_attributes_reference:

deps_user_info
--------------

You can access the declared ``user_info.XXX`` variables of the requirements through the ``self.deps_user_info`` object like this:


.. code-block:: python
   :emphasize-lines: 2

    import os

    class RecipeConan(ConanFile):
        ...
        requires = "package1/1.0@conan/stable"
        ...

        def build(self):
            self.deps_user_info["package1"].SOMEVAR


info
----

Object used to control the unique ID for a package. Check the :ref:`package_id() <method_package_id>` to see the details of the ``self.info``
object.


.. _apply_env:

apply_env
---------

When ``True`` (Default), the values from ``self.deps_env_info`` (corresponding to the declared ``env_info`` in the ``requires`` and ``build_requires``)
will be automatically applied to the ``os.environ``.

Disable it setting ``apply_env`` to False if you want to control by yourself the environment variables
applied to your recipes.

You can apply manually the environment variables from the requires and build_requires:

.. code-block:: python
   :emphasize-lines: 2

    import os
    from conans import tools

    class RecipeConan(ConanFile):
        apply_env = False

        def build(self):
            with tools.environment_append(self.env):
                # The same if we specified apply_env = True
                pass

.. _in_local_cache:

in_local_cache
--------------

A boolean attribute useful for conditional logic to apply in user folders local commands.
It will return `True` if the conanfile resides in the local cache ( we are installing the package)
and `False` if we are running the conanfile in a user folder (local Conan commands).

.. code-block:: python

    import os

    class RecipeConan(ConanFile):
        ...

        def build(self):
            if self.in_local_cache:
                # we are installing the package
            else:
                # we are building the package in a local directory


.. _develop_attribute:


develop
-------

A boolean attribute useful for conditional logic. It will be ``True`` if the package is created with :command:`conan create`, or if the
*conanfile.py* is in user space:

.. code-block:: python

    class RecipeConan(ConanFile):

        def build(self):
            if self.develop:
                self.output.info("Develop mode")

It can be used for conditional logic in other methods too, like ``requirements()``, ``package()``, etc.

This recipe will output "Develop mode" if:

.. code-block:: bash

    $ conan create . user/testing
    # or
    $ mkdir build && cd build && conan install ..
    $ conan build ..

But it will not output that when it is a transitive requirement or installed with :command:`conan install`.

.. _keep_imports:

keep_imports
------------

Just before the ``build()`` method is executed, if the conanfile has an ``imports()`` method, it is
executed into the build folder, to copy binaries from dependencies that might be necessary for
the ``build()`` method to work. After the method finishes, those copied (imported) files are removed,
so they are not later unnecessarily repackaged.

This behavior can be avoided declaring the ``keep_imports=True`` attribute. This can be useful, for example
to :ref:`repackage artifacts <repackage>`


.. _scm_attribute:

scm
---

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

Used to clone/checkout a repository. It is a dictionary with the following possible values:

.. code-block:: python

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
         scm = {
            "type": "git",
            "subfolder": "hello",
            "url": "https://github.com/memsharded/hello.git",
            "revision": "static_shared"
         }
        ...



- **type** (Required): Currently only ``git`` and ``svn`` are supported. Others can be added eventually.
- **url** (Required): URL of the remote or ``auto`` to capture the remote from the local working
  copy (credentials will be removed from it). When type is ``svn`` it can contain
  the `peg_revision <http://svnbook.red-bean.com/en/1.7/svn.advanced.pegrevs.html>`_.
- **revision** (Required): id of the revision or ``auto`` to capture the current working copy one.
  When type is ``git``, it can also be the branch name or a tag.
- **subfolder** (Optional, Defaulted to ``.``): A subfolder where the repository will be cloned.
- **username** (Optional, Defaulted to ``None``): When present, it will be used as the login to authenticate with the remote.
- **password** (Optional, Defaulted to ``None``): When present, it will be used as the password to authenticate with the remote.
- **verify_ssl** (Optional, Defaulted to ``True``): Verify SSL certificate of the specified **url**.
- **submodule** (Optional, Defaulted to ``None``):
   - ``shallow``: Will sync the git submodules using ``submodule sync``
   - ``recursive``: Will sync the git submodules using ``submodule sync --recursive``

SCM attributes are evaluated in the workspace context where the *conanfile.py* is located before
exporting it to the Conan cache, so these values can be returned from arbitrary functions that
depend on the workspace layout. Nevertheless, all the other code in the recipe must be able to
run in the export folder inside the cache, where it has access only to the files exported (see
attribute :ref:`exports <exports_attribute>`) and to any other functionality
from a :ref:`python_requires <python_requires>`.

To know more about the usage of ``scm`` check:

- :ref:`Creating packages/Recipe and sources in a different repo <external_repo>`
- :ref:`Creating packages/Recipe and sources in the same repo <package_repo>`
