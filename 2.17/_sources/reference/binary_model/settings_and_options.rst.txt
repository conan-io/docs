.. _reference_binary_model_settings_options:

How settings and options of a recipe influence its package ID
=============================================================

In Conan, a package ID is a unique identifier for a package binary that takes into account all the factors that affect its binary compatibility.
These factors include recipe options and settings as well as requirements or tool requirements.

Let's see how settings and options affect the package ID and some examples where they should not.

How settings influence the package ID
-------------------------------------

Settings are development project-wide variables, like the compiler, its version, or the OS itself.
These variable values have to be defined, they should match the values of our development environment, and they cannot have a default value like options do.

For example, let's define a recipe that generates packages that are only OS dependent:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0.0"
        settings = "os"  # Only OS setting affects the package ID

If we generate a package from this recipe for Linux we will get the following package ID:

.. code-block:: bash
   :emphasize-lines: 3, 12

    $ conan create . --settings os=Linux
    ...
    pkg/1.0.0: Package '9a4eb3c8701508aa9458b1a73d0633783ecc2270' created

    $ conan list pkg/1.0.0:*
    Local Cache
      pkg
        pkg/1.0.0
          revisions
              476929a74c859bb5f646363a4900f7cf (2024-03-07 09:13:43 UTC)
                packages
                  9a4eb3c8701508aa9458b1a73d0633783ecc2270
                    info
                      settings
                        os: Linux

If we do the same thing with Windows, now the package ID will be diffent:

.. code-block:: bash
   :emphasize-lines: 3, 12, 16

    $ conan create . --settings os=Windows
    ...
    pkg/1.0.0: Package 'ebec3dc6d7f6b907b3ada0c3d3cdc83613a2b715' created

    $ conan list pkg/1.0.0:*
    Local Cache
      pkg
        pkg/1.0.0
          revisions
              476929a74c859bb5f646363a4900f7cf (2024-03-07 09:13:43 UTC)
                packages
                  9a4eb3c8701508aa9458b1a73d0633783ecc2270
                    info
                      settings
                        os: Linux
                  ebec3dc6d7f6b907b3ada0c3d3cdc83613a2b715
                    info
                      settings
                        os: Windows

Whenever a value of the settings or subsettings changes, the package ID will be different to reflect that.

The most common usage for settings is to model the different project-wide aspects that might influence the package ID.
A recipe that does that will be:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0.0"
        settings = "os", "arch", "compiler", "build_type"

Now, compiling a package with different compiler versions will result into different package IDs:

.. code-block:: bash
   :emphasize-lines: 3, 7, 16, 27

    $ conan create . --settings compiler.version=192
    ...
    pkg/1.0.0: Package '4f267380690f99b3ef385199826c268f63147457' created

    $ conan create . --settings compiler.version=193
    ...
    pkg/1.0.0: Package 'c13a22a41ecd72caf9e556f68b406569547e0861' created

    $ conan list pkg/1.0.0:*
    Local Cache
      pkg
        pkg/1.0.0
          revisions
            f1f48830ecb04f3b328429b390fc5de8 (2024-03-07 09:21:07 UTC)
              packages
                4f267380690f99b3ef385199826c268f63147457
                  info
                    settings
                      arch: x86_64
                      build_type: Release
                      compiler: msvc
                      compiler.cppstd: 14
                      compiler.runtime: dynamic
                      compiler.runtime_type: Release
                      compiler.version: 192
                      os: Windows
                c13a22a41ecd72caf9e556f68b406569547e0861
                  info
                    settings
                      arch: x86_64
                      build_type: Release
                      compiler: msvc
                      compiler.cppstd: 14
                      compiler.runtime: dynamic
                      compiler.runtime_type: Release
                      compiler.version: 193
                      os: Windows

Removing settings for a package used as a tool_require
++++++++++++++++++++++++++++++++++++++++++++++++++++++

There could be cases when a setting should not influence the resulting package ID.
An example of this could be when a recipe packages a tool that would be used to build other packages via ``tool_requires``

In that case, the value of the compiler used is needed for the compilation of the tool but not that relevant for consumers, as we only want to execute the tool to build other projects.
So we could eventually remove the influence of the compiler from the pacakge ID:

.. code-block:: python

    from conan import ConanFile

    class CMake(ConanFile):
        name = "cmake"
        version = "1.0.0"
        settings = "os", "arch", "compiler", "build_type"  # Only OS and architecture influence the resulting package

        def build(self):
            # self.settings.compiler value will be used here to compile cmake

        def package_id(self):
            # Remove compiler setting from package ID
            del self.info.settings.compiler

Why not removing the setting from the `settings` attribute? Because the compiler value is still needed in the `build()` method to perform the compilation of the executable.

.. note::

    In the case we are generating our own executables (our own apps, not a ``tool_require``), **removing the compiler setting from package ID is not recommended**, as we would always want to know
    that the package was generated with a specific compiler.

However, in case we are packaging a tool that does not even require a compiler input for building (a python script for example), we could also directly remove the settings attribute:

.. code-block:: python

    from conan import ConanFile

    class MyPythonScripts(ConanFile):
        name = "my-python-scripts"
        version = "1.0.0"
        # No settings this time

Or, if the tool is platform specific we can just keep the OS and architecture information:

.. code-block:: python

    from conan import ConanFile

    class MyScripts(ConanFile):
        name = "my-scripts"
        version = "1.0.0"
        settings = "os", "arch"

How options influence the package ID
------------------------------------

Options are used to specify characteristics that are particular to a single recipe, contrasting with settings that generally remain consistent across recipes within a project.
They are usually a set of particular characteristics of a library executable or conan package may have.

For example, a `shared` option is a very common option used in recipes that can produce shared libraries. However, it could not be a setting as not all recipes produce shared libraries.

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "1.0.0"
        options = {"shared": [True, False]}
        default_options = {"shared": True}

As in the previous case with settings, the different values of an option will influence the package ID and therefore, generate different packages depending on it.

.. code-block:: bash
   :emphasize-lines: 3, 7

    $ conan create . --options shared=True
    ...
    pkg/1.0.0: Package '1744785cb24e3bdca70e27041dc5abd20476f947' created

    $ conan create . --options shared=False
    ...
    pkg/1.0.0: Package '55c609fe8808aa5308134cb5989d23d3caffccf2' created

In the same way, there might be "options" that are needed as input in a recipe to generate a package which shouldn't be taken into account in the package ID.
An example of this could be an option to control something that during the build phase but that does not influence the package result, like the *verbosity* of a compilation.
In that case, the recipe should remove the option in the :ref:`package_id() method <reference_conanfile_methods_package_id>`:

However, the general advice is that **options should always affect the package ID**, and in case we would like to have an input to the recipe that should **not** affect it,
it should be done via the :ref:`conf section <reference_config_files_profiles_conf>` of your profile. Then in the recipe we should just add:

.. code-block:: python

    from conan import ConanFile

    class MyPkg(ConanFile):
        name = "my-pkg"
        version = "1.0.0"

        def build(self):
            verbosity = self.conf.get("user.my-pkg:verbosity")
            self.output.info(f"Using verbosity level: {verbosity})
            ...

.. code-block:: text
    :caption: *myprofile*

    [conf]
    user.my-pkg:verbosity=silent

That way the package ID will be not affected, the recipe will be cleaner (without irrelevant options for package ID) and the input is easily managed via the profile's conf section.


.. seealso::

    - :ref:`reference_binary_model_package_id`
    - :ref:`tutorial_creating_configure`
