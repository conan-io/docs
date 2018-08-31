.. _define_abi_compatibility:

Defining Package ABI Compatibility
==================================

Each package recipe can generate *N* binary packages from it, depending on these three items:
``settings``, ``options`` and ``requires``.

When any of the :ref:`settings_property` of a package recipe changes, it will reference a
different binary:

.. code-block:: python

    class MyLibConanPackage(ConanFile):	
        name = "MyLib"
        version = "1.0"
        settings = "os", "arch", "compiler", "build_type"

When this package is installed by a *conanfile.txt*, another package *conanfile.py*, or directly:

.. code-block:: bash

    $ conan install MyLib/1.0@user/channel -s arch=x86_64 -s ...

The process is:

1. Conan gets the user input settings and options. Those settings and options can come from the command line, profiles or from the values
   cached in the latest :command:`conan install` execution.
2. Conan retrieves the ``MyLib/1.0@user/channel`` recipe, reads the ``settings`` attribute, and assigns the necessary values.
3. With the current package values for ``settings`` (also ``options`` and ``requires``), it will compute a SHA1 hash that will serve as the binary
   package ID, e.g., ``c6d75a933080ca17eb7f076813e7fb21aaa740f2``.
4. Conan will try to find the ``c6d75...`` binary package. If it exists, it will be retrieved. If it cannot be found, it will fail and indicate that it
   can be built from sources using :command:`conan install --build`.

If the package is installed again using different settings, for example, on a 32-bit architecture:

.. code-block:: bash

    $ conan install MyLib/1.0@user/channel -s arch=x86 -s ...

The process will be repeated with a different generated package ID, because the ``arch``
setting will have a different value. The same applies to different compilers, compiler versions, build types. When generating multiple
binaries - a separate ID is generated for each configuration.

When developers using the package use the same settings as one of those uploaded binaries, the computed package ID will be
identical causing the binary to be retrieved and reused without the need of rebuilding it from the sources.

The ``options`` behavior is very similar. The main difference is that ``options`` can be more easily defined at the package level and they can
be defaulted. Check the :ref:`conanfile_options` reference.

Note this simple scenario of a **header-only** library. The package does not need to be built, and it will not have any ABI issues at all.
The recipe for such a package will be to generate a single binary package, no more. This is easily achieved by not declaring
``settings`` nor ``options`` in the recipe as follows:

.. code-block:: python

    class MyLibConanPackage(ConanFile): 
        name = "MyLib"
        version = "1.0"
        # no settings defined!

No matter the settings are defined by the users, including the compiler or version, the package settings and options will always be the same
(left empty) and they will hash to the same binary package ID. That package will typically contain just the header files.

What happens if we have a library that we can be built with GCC 4.8 and will preserve the ABI compatibility with GCC 4.9?
(This kind of compatibility is easier to achieve for example for pure C libraries).

Although it could be argued that it is worth rebuilding with 4.9 too -to get fixes and performance improvements-. Let's suppose
that we don't want to create 2 different binaries, but just a single built with GCC 4.8 which also needs to be compatible for GCC 4.9 installations.

.. _define_custom_package_id:

Defining a Custom package_id()
------------------------------

The default ``package_id()`` uses the ``settings`` and ``options`` directly as defined, and assumes the
`semantic versioning <https://semver.org/>`_ for dependencies is defined in ``requires``.

This ``package_id()`` method can be overridden to control the package ID generation. Within the ``package_id()``, we have access to the
``self.info`` object, which is hashed to compute the binary ID and contains:

- **self.info.settings**: Contains all the declared settings, always as string values. We can access/modify the settings, e.g.,
  ``self.info.settings.compiler.version``.

- **self.info.options**: Contains all the declared options, always as string values too, e.g., ``self.info.options.shared``.

Initially this ``info`` object contains the original settings and options, but they can be changed without constraints to any other
string value.

For example, if you are sure your package ABI compatibility is fine for GCC versions > 4.5 and < 5.0, you could do the following:

.. code-block:: python

    from conans import ConanFile, CMake, tools
    from conans.model.version import Version

    class PkgConan(ConanFile):
        name = "Pkg"
        version = "1.0"
        settings = "compiler", "build_type"

        def package_id(self):
            v = Version(str(self.settings.compiler.version))
            if self.settings.compiler == "gcc" and (v >= "4.5" and v < "5.0"):
                self.info.settings.compiler.version = "GCC version between 4.5 and 5.0"

We have set the ``self.info.settings.compiler.version`` with an arbitrary string, the value of which is not important (could be any string). The
only important thing is that it is the same for any GCC version between 4.5 and 5.0. For all those versions, the compiler version will
always be hashed to the same ID.

Let's try and check that it works properly when installing the package for GCC 4.5:

.. code-block:: bash

    $ conan export myuser/mychannel
    $ conan install Pkg/1.0@myuser/mychannel -s compiler=gcc -s compiler.version=4.5 ...

    Requirements
        Pkg/1.0@myuser/mychannel from local
    Packages
        Pkg/1.0@myuser/mychannel:mychannel:af044f9619574eceb8e1cca737a64bdad88246ad
    ...

We can see that the computed package ID is ``af04...46ad`` (not real). What happens if we specify GCC 4.6?

.. code-block:: bash

    $ conan install Pkg/1.0@myuser/mychannel -s compiler=gcc -s compiler.version=4.6 ...

    Requirements
        Pkg/1.0@myuser/mychannel from local
    Packages
        Pkg/1.0@myuser/mychannel:mychannel:af044f9619574eceb8e1cca737a64bdad88246ad

The required package has the same result again ``af04...46ad``. Now we can try using GCC 4.4 (< 4.5):

.. code-block:: bash

    $ conan install Pkg/1.0@myuser/mychannel -s compiler=gcc -s compiler.version=4.4 ...

    Requirements
        Pkg/1.0@myuser/mychannel from local
    Packages
        Pkg/1.0@myuser/mychannel:mychannel:7d02dc01581029782b59dcc8c9783a73ab3c22dd

The computed package ID is different which means that we need a different binary package for GCC 4.4.

The same way we have adjusted the ``self.info.settings``, we could set the ``self.info.options`` values if needed.

.. seealso::

    Check :ref:`method_package_id` to see the available helper methods and change its behavior for things like:

        - Recipes packaging **header only** libraries.
        - Adjusting **Visual Studio toolsets** compatibility.

.. _problem_of_dependencies:

Dependency Issues
-----------------

Let's define a simple scenario whereby there are two packages: ``MyOtherLib/2.0`` and ``MyLib/1.0`` which depends on
``MyOtherLib/2.0``. Let's assume that their recipes and binaries have already been created and uploaded to a Conan remote.

Now, a new release for ``MyOtherLib/2.1`` is released with an improved recipe and new binaries. The ``MyLib/1.0`` is modified and is required to be upgraded to ``MyOtherLib/2.1``.

.. note::

    This scenario will be the same in the case that a consuming project of ``MyLib/1.0`` defines a dependency to ``MyOtherLib/2.1``, which
    takes precedence over the existing project in ``MyLib/1.0``.

The question is: **Is it necessary to build new MyLib/1.0 binary packages?** or are the existing packages still valid?

The answer: **It depends**.

Let's assume that both packages are compiled as static libraries and that the API exposed by ``MyOtherLib`` to ``MyLib/1.0`` through the
public headers, has not changed at all. In this case, it is not required to build new binaries for ``MyLib/1.0`` because the final consumer will
link against both ``Mylib/1.0`` and ``MyOtherLib/2.1``.

On the other hand, it could happen that the API exposed by **MyOtherLib** in the public headers has changed, but without affecting the
``MyLib/1.0`` binary for any reason (like changes consisting on new functions not used by **MyLib**). The same reasoning would apply if **MyOtherLib** was only the header.

But what if a header file of ``MyOtherLib`` -named *myadd.h*- has changed from ``2.0`` to ``2.1``:

.. code-block:: cpp
   :caption: *myadd.h* header file in version 2.0

    int addition (int a, int b) { return a - b; }

.. code-block:: cpp
   :caption: *myadd.h* header file in version 2.1

    int addition (int a, int b) { return a + b; }

And the ``addition()`` function is called from the compiled *.cpp* files of ``MyLib/1.0``?

Then, **a new binary for MyLib/1.0 is required to be built for the new dependency version**. Otherwise it will maintain the old, buggy
``addition()`` version. Even in the case that ``MyLib/1.0`` doesn't have any change in its code lines neither in the recipe, the resulting
binary rebuilding ``MyLib`` requires `MyOtherLib/2.1`` and the package to be different.

Using package_id() for Package Dependencies
-------------------------------------------

The ``self.info`` object has also a ``requires`` object. It is a dictionary containing the necessary information for each requirement, all direct
and transitive dependencies. For example, ``self.info.requires["MyOtherLib"]`` is a ``RequirementInfo`` object.

- Each ``RequirementInfo`` has the following `read only` reference fields:

    - ``full_name``: Full require's name, e.g., **MyOtherLib**
    - ``full_version``: Full require's version, e.g., **1.2**
    - ``full_user``: Full require's user, e.g., **my_user**
    - ``full_channel``: Full require's channel, e.g., **stable**
    - ``full_package_id``: Full require's package ID, e.g., **c6d75a...**

- The following fields are used in the ``package_id()`` evaluation:

    - ``name``: By default same value as full_name, e.g., **MyOtherLib**.
    - ``version``: By default the major version representation of the ``full_version``.
      E.g., **1.Y** for a **1.2** ``full_version`` field and **1.Y.Z** for a **1.2.3**
      ``full_version`` field.
    - ``user``: By default ``None`` (doesn't affect the package ID).
    - ``channel``: By default ``None`` (doesn't affect the package ID).
    - ``package_id``: By default ``None`` (doesn't affect the package ID).

When defining a package ID for model dependencies, it is necessary to take into account two factors:

- The versioning schema followed by our requirements (semver?, custom?).
- The type of library being built or reused (shared (*.so*, *.dll*, *.dylib*), static).

Versioning Schema
+++++++++++++++++

By default Conan assumes `semver <https://semver.org/>`_ compatibility. For example, if a version changes from minor **2.0** to **2.1**, Conan will
assume that the API is compatible (headers not changing), and that it is not necessary to build a new binary for it. This also applies to
patches, whereby changing from **2.1.10** to **2.1.11** doesn't require a re-build.

If it is necessary to change the default behavior, the applied versioning schema can be customized within the ``package_id()`` method:

.. code-block:: python

    from conans import ConanFile, CMake, tools
    from conans.model.version import Version

    class PkgConan(ConanFile):
        name = "Mylib"
        version = "1.0"
        settings = "os", "compiler", "build_type", "arch"
        requires = "MyOtherLib/2.0@lasote/stable"

        def package_id(self):
            myotherlib = self.info.requires["MyOtherLib"]

            # Any change in the MyOtherLib version will change current Package ID
            myotherlib.version = myotherlib.full_version

            # Changes in major and minor versions will change the Package ID but
            # only a MyOtherLib patch won't. E.g., from 1.2.3 to 1.2.89 won't change.
            myotherlib.version = myotherlib.full_version.minor()

Besides ``version``, there are additional helpers that can be used to determine whether the **channel** and **user** of one dependency also
affects the binary package, or even the required package ID can change your own package ID.

You can determine if the following variables within any requirement change the ID of your binary package using the following modes:

+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| **Modes / Variables**   | ``name`` | ``version``                             | ``user`` | ``channel`` | ``package_id`` |
+=========================+==========+=========================================+==========+=============+================+
| ``semver_mode()``       | Yes      | Yes, only > 1.0.0 (e.g., **1**.2.Z+b102)| No       | No          | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``major_mode()``        | Yes      | Yes (e.g., **1**.2.Z+b102)              | No       | No          | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``minor_mode()``        | Yes      | Yes (e.g., **1.2**.Z+b102)              | No       | No          | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``patch_mode()``        | Yes      | Yes (e.g., **1.2.3**\+b102)             | No       | No          | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``base_mode()``         | Yes      | Yes (e.g., **1.7**\+b102)               | No       | No          | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``full_version_mode()`` | Yes      | Yes (e.g., **1.2.3+b102**)              | No       | No          | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``full_recipe_mode()``  | Yes      | Yes (e.g., **1.2.3+b102**)              | Yes      | Yes         | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``full_package_mode()`` | Yes      | Yes (e.g., **1.2.3+b102**)              | Yes      | Yes         | Yes            |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+
| ``unrelated_mode()``    | No       | No                                      | No       | No          | No             |
+-------------------------+----------+-----------------------------------------+----------+-------------+----------------+

- ``semver_mode()``: This is the default mode. In this mode, only a major release version (starting from **1.0.0**) changes the package ID.
  Every version change prior to 1.0.0 changes the package ID, but only major changes after 1.0.0 will be applied.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].semver_mode()

- ``major_mode()``: Any change in the major release version (starting from **0.0.0**) changes the package ID.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].major_mode()

- ``minor_mode()``: Any change in major or minor (not patch nor build) version of the required dependency changes the package ID.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].patch_mode()

- ``patch_mode()``: Any changes to major, minor or patch (not build) versions of the required dependency change the package ID.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].patch_mode()

- ``base_mode()``: Any changes to the base of the version (not build) of the required dependency changes the package ID. Note that in the
  case of semver notation this may produce the same result as ``patch_mode()``, but it is actually intended to dismiss the build part of the
  version even without strict semver.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].base_mode()

- ``full_version_mode()``: Any changes to the version of the required dependency changes the package ID.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].full_version_mode()

- ``full_recipe_mode()``: Any change in the reference of the requirement (user & channel too) changes the package ID.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].full_recipe_mode()

- ``full_package_mode()``: Any change in the required version, user, channel or package ID changes the package ID.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].full_package_mode()

- ``unrelated_mode()``: Requirements do not change the package ID.

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].unrelated_mode()

You can also adjust the individual properties manually:

.. code-block:: python

    def package_id(self):
        myotherlib = self.info.requires["MyOtherLib"]

        # Same as myotherlib.semver_mode()
        myotherlib.name = myotherlib.full_name
        myotherlib.version = myotherlib.full_version.stable()  # major(), minor(), patch(), base, build
        myotherlib.user = myotherlib.channel = myotherlib.package_id = None

        # Only the channel (and the name) matters
        myotherlib.name = myotherlib.full_name
        myotherlib.user = myotherlib.package_id = myotherlib.version = None
        myotherlib.channel = myotherlib.full_channel

The result of the ``package_id()`` is the package ID hash, but the details can be checked in the
generated *conaninfo.txt* file. The ``[requires]``, ``[options]`` and ``[settings]`` are taken
into account when generating the SHA1 hash for the package ID, while the ``[full_xxxx]`` fields show the
complete reference information.

The default behavior produces a *conaninfo.txt* that looks like:

.. code-block:: text

    [requires]
      MyOtherLib/2.Y.Z

    [full_requires]
      MyOtherLib/2.2@demo/testing:73bce3fd7eb82b2eabc19fe11317d37da81afa56

Library Types: Shared, Static, Header-only
++++++++++++++++++++++++++++++++++++++++++

Let's see some examples, corresponding to common scenarios:

- ``MyLib/1.0`` is a shared library that links with a static library ``MyOtherLib/2.0`` package.
  When a new ``MyOtherLib/2.1`` version is released: Do I need to create a new binary for
  ``MyLib/1.0`` to link with it?

  Yes, always, as the implementation is embedded in the ``MyLib/1.0`` shared library. If we
  always want to rebuild our library, even if the channel changes (we assume a channel change could
  mean a source code change):

  .. code-block:: python

      def package_id(self):
          # Any change in the MyOtherLib version, user or
          # channel or Package ID will affect our package ID
          self.info.requires["MyOtherLib"].full_package_mode()

- ``MyLib/1.0`` is a shared library, requiring another shared library ``MyOtherLib/2.0`` package.
  When a new ``MyOtherLib/2.1`` version is released: Do I need to create a new binary for
  ``MyLib/1.0`` to link with it?

  It depends. If the public headers have not changed at all, it is not necessary. Actually it might
  be necessary to consider transitive dependencies that are shared among the public headers, how
  they are linked and if they cross the frontiers of the API, it might also lead to
  incompatibilities. If the public headers have changed, it would depend on what changes and how are
  they used in ``MyLib/1.0``. Adding new methods to the public headers will have no impact, but
  changing the implementation of some functions that will be inlined when compiled from
  ``MyLib/1.0`` will definitely require re-building. For this case, it could make sense to have this configuration:

  .. code-block:: python

      def package_id(self):
          # Any change in the MyOtherLib version, user or channel
          # or Package ID will affect our package ID
          self.info.requires["MyOtherLib"].full_package_mode()

          # Or any change in the MyOtherLib version, user or
          # channel will affect our package ID
          self.info.requires["MyOtherLib"].full_recipe_mode()

- ``MyLib/1.0`` is a header-only library, linking with any kind (header, static, shared) of library
  in ``MyOtherLib/2.0`` package. When a new ``MyOtherLib/2.1`` version is released: Do I need to
  create a new binary for ``MyLib/1.0`` to link with it?

  Never. The package should always be the same as there are no settings, no options, and in any way a
  dependency can affect a binary, because there is no such binary. The default behavior should be
  changed to:

  .. code-block:: python

      def package_id(self):
          self.info.requires.clear()

- ``MyLib/1.0`` is a static library linking to a header only library in ``MyOtherLib/2.0``
  package. When a new ``MyOtherLib/2.1`` version is released: Do I need to create a new binary for
  ``MyLib/1.0`` to link with it? It could happen that the ``MyOtherLib`` headers are strictly used
  in some ``MyLib`` headers, which are not compiled, but transitively included. But in general,
  it is more likely that ``MyOtherLib`` headers are used in ``MyLib`` implementation files, so every
  change in them should imply a new binary to be built. If we know that changes in the channel never
  imply a source code change, as set in our workflow/lifecycle, we could
  write:

  .. code-block:: python

      def package_id(self):
          self.info.requires["MyOtherLib"].full_package()
          self.info.requires["MyOtherLib"].channel = None # Channel doesn't change out package ID
