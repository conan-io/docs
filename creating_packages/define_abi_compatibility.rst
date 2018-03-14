.. _define_abi_compatibility:

Define package ABI compatibility
================================

Each package recipe can generate *N* binary packages from it, depending on three things:
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

The process will be:

1. Conan will get the user input settings and options, which can come from the command line, be
   default values defined in *~/.conan/profiles/default*, defined in a :ref:`profiles` file, or
   cached from the latest :command:`conan install` execution.
2. Conan will retrieve the ``MyLib/1.0@user/channel`` recipe, read the ``settings`` attribute, and
   assign the necessary values.
3. With the current package values for ``settings`` (also ``options`` and ``requires``), it will
   compute a SHA1 hash, that will be the binary package ID, e.g.
   ``c6d75a933080ca17eb7f076813e7fb21aaa740f2``.
4. Conan will try to find the ``c6d75...`` binary package. If it's present conan will retrieve it,
   if not, it can be built from sources with :command:`conan install --build`.

If the package is installed again with different settings, for example, for 32bits architecture:

.. code-block:: bash

    $ conan install MyLib/1.0@user/channel -s arch=x86 -s ...

The process will be repeated, but now generating a different package ID, because the ``arch``
setting will have a different value. The same applies for different compilers, compiler versions,
build type, etc., generating multiple binaries, one for each configuration.

When users of the package define the same settings as one of those binaries that have been uploaded,
the computed package ID will be the same, such binary will be retrieved, and they will be able
to reuse the binary without building it from sources.

The use case for ``options`` is very similar, the main difference is that options can be more easily
defined at the package level and they can be defaulted. Check the :ref:`conanfile_options`
reference.

Note the simple scenario of a **header-only** library. Such package does not need to be built, and
it will not have any ABI issues at all. The recipe of such package will have to generate exactly 1
binary package, no more. This is easily achieved, just by no declaring ``settings`` nor ``options``
in the recipe:

.. code-block:: python

    class MyLibConanPackage(ConanFile): 
        name = "MyLib"
        version = "1.0"
        # no settings defined!

Then, no matter what are the settings defined by the users, which compiler or version, the package
settings and options will always be the same (empty) and they will hash to the same binary package
ID, that will typically contain just the header files.

What happens if we have a library that we know we can build with gcc 4.8 and we know it will
remain ABI compatibility with gcc 4.9? This kind of compatibility is easier to achieve for example
for pure C libraries. Although it could be argued that it is worth rebuilding with 4.9 too, to
get fixes and performance improvements, lets suppose that we don't want to create 2 different
binaries, just one built with gcc 4.8 and be able to use it from gcc 4.9 installs.

.. _define_custom_package_id:

Defining a custom package_id()
------------------------------

The default ``package_id()`` uses the ``settings`` and ``options`` directly as defined, and assumes
semver behavior for dependencies ``requires``.

This ``package_id()`` recipe method can be overriden to control the package ID generation. Within
the ``package_id()`` method we have access to the ``self.info`` object, which is the actual object
being hashed for computing the binary ID:

 - **self.info.settings**: Contains all the declared settings, always as string values. We can
   access/alter the settings. E.g: ``self.info.settings.compiler.version``.

 - **self.info.options**: Contains all the declared options, always as string values. E.g:
   ``self.info.options.shared``.

Initially, this ``info`` object will contain the original settings and options, stored as strings.
They can be changed without constraints, to any other string value.

For example, if you are sure your package ABI compatibility is fine for GCC versions > 4.5 and <
5.0, (just an example, not a real case) you could do this:

.. code-block:: python

    from conans import ConanFile, CMake, tools
    from conans.model.version import Version

    class PkgConan(ConanFile):
        name = "Pkg"
        version = "0.1"
        settings = "compiler", "build_type"
    
        def package_id(self):
            v = Version(str(self.settings.compiler.version))
            if self.settings.compiler == "gcc" and (v >= "4.5" and v < "5.0"):
                self.info.settings.compiler.version = "GCC 4 between 4.5 and 5.0"

We have set the ``self.info.settings.compiler.version`` with an arbitrary string, it's not really
important, could be any string. The only important thing is that won't change for any GCC[4.5-5.0],
for those gcc versions, it will be always the same string, and then it will be always hashed to the
same ID.

Let's check that it works properly installing the package for gcc 4.5:

.. code-block:: bash

    $ conan export myuser/mychannel
    $ conan install Pkg/1.0@myuser/mychannel -s compiler=gcc -s compiler.version=4.5 ...

    Requirements
        Pkg/1.0@myuser/mychannel from local
    Packages
        Pkg/1.0@myuser/mychannel:mychannel:af044f9619574eceb8e1cca737a64bdad88246ad
    ...

We can see that the computed package ID is ``af04...46ad`` (not real). What would happen if we
specify GCC 4.6?

.. code-block:: bash

    $ conan install Pkg/1.0@myuser/mychannel -s compiler=gcc -s compiler.version=4.6 ...

    Requirements
        Pkg/1.0@myuser/mychannel from local
    Packages
        Pkg/1.0@myuser/mychannel:mychannel:af044f9619574eceb8e1cca737a64bdad88246ad

Same result, the required package is again ``af04...46ad``. Now we can try with GCC 4.4 (<4.5).

.. code-block:: bash

    $ conan install Pkg/1.0@myuser/mychannel -s compiler=gcc -s compiler.version=4.4 ...

    Requirements
        Pkg/1.0@myuser/mychannel from local
    Packages
        Pkg/1.0@myuser/mychannel:mychannel:7d02dc01581029782b59dcc8c9783a73ab3c22dd

Now the computed package ID is different, that means that we need a different binary package for GCC
4.4.

The same way we have adjusted the ``self.info.settings`` we could set the ``self.info.options``
values if necessary.


.. seealso::

    Check the :ref:`package_id() method reference<method_package_id>` too see the available helper methods
    to change the package_id() behavior, for example to:

        - Adjust our package recipe as a **header only**
        - Adjust **Visual Studio toolsets** compatibility


.. _problem_of_dependencies:

The problem of dependencies
---------------------------

Let's define a simple scenario in which there are two packages, one for ``MyLib/1.0`` which depends
on (requires) ``MyOtherLib/2.0``. The recipes and binaries for them have been created and uploaded
to a conan server.

A new release for ``MyOtherLib/2.1`` comes out, with improved recipe and new binaries. The
``MyLib/1.0`` is modified to upgrade the requires to ``MyOtherLib/2.1``. (Note that this is not
strictly necessary, we would face the same problem if the downstream, consuming project defines a
dependency to ``MyOtherLib/2.1``, which would have precedence over the existing one in MyLib).

The question is: **Is it necessary to build new MyLib/1.0 packages binaries?** Or the existing
packages are still valid?

The answer: **It depends**.

Let's suppose that both are being compiled as static libraries, and that the API exposed by
``MyOtherLib`` to ``MyLib/1.0`` through the public headers has not changed at all. Then, it is not
necessary to build new binaries for ``MyLib/1.0``, because the final consumer will link against both
``Mylib/1.0`` and ``MyOtherLib/2.1``.

It could happen that the API exposed by **MyOtherLib** in public headers has changed, but without
affecting the ``MyLib/1.0`` binary, for whatever reasons, like changes consisting on new functions,
not used by **MyLib**. The same reasoning would still be valid if **MyOtherLib** was header only.

But what if one header file of ``MyOtherLib``, named *myadd.h* has changed from ``2.0``:

.. code-block:: cpp

    int addition (int a, int b) { return a - b; }

To the *myadd.h* file in ``2.1``:

.. code-block:: cpp

    int addition (int a, int b) { return a + b; }

And the ``addition()`` function is being called from compiled ``.cpp`` files of ``MyLib/1.0``?

Then, in this case, **MyLib/0.1 has to build a new binary for the new dependency version**.
Otherwise, it will maintain the old, buggy ``addition()`` version. Even if ``MyLib/0.1`` hasn't
change a line, not the code, neither the recipe, still the resulting binary would be different.

Using package_id() for package dependencies
-------------------------------------------

The ``self.info`` object also have a ``requires`` object. It is a dictionary with the necessary
information for each requirement, all direct and transitive dependencies. E.g.
``self.info.requires["MyOtherLib"]`` is a ``RequirementInfo`` object.
    
- Each ``RequirementInfo`` has the following `read only` reference fields:

    - ``full_name``: Full require's name. E.g **MyOtherLib**
    - ``full_version``: Full require's version. E.g **1.2**
    - ``full_user``: Full require's user. E.g **my_user**
    - ``full_channel``: Full require's channel. E.g **stable**
    - ``full_package_id``: Full require's package ID. E.g **c6d75a...**

- The following fields are the ones used in the ``package_id()`` evaluation:

    - ``name``: By default same value as full_name. E.g **MyOtherLib**.
    - ``version``: By default the major version representation of the ``full_version``.
      E.g **1.Y** for a **1.2** ``full_version`` field and **1.Y.Z** for a **1.2.3**
      ``full_version`` field.
    - ``user``: By default ``None`` (doesn't affect the package ID).
    - ``channel``: By default ``None`` (doesn't affect the package ID).
    - ``package_id``: By default ``None`` (doesn't affect the package ID).

When defining a package ID to model dependencies, it is necessary to take into account two factors:

- The versioning schema followed by our requirements (semver?, custom?)
- Type of library being built and type of library being reused (shared: so, dll, dylib, static).

Versioning schema
+++++++++++++++++

By default conan assumes **semver** compatibility, i.e, if a version changes from minor **2.0** to
**2.1** conan will assume that the API is compatible (headers not changing), and that it is not
necessary to build a new binary for it. Exactly the same for patches, changing from **2.1.10** to
**2.1.11** doesn't require a re-build. Those rules are defined by `semver <http://semver.org/>`_.

If it is necessary to change the default behavior, the applied versioning schema can be customized
within the ``package_id()`` method:

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

            # Changes in major and stable versions will change the Package ID but
            # only a MyOtherLib revision won't. E.j: From 1.2.3 to 1.2.89 won't change.
            myotherlib.version = myotherlib.full_version.minor()

Besides the ``version``, there are some other helpers that can be used, to decide whether the
**channel** and **user** of one dependency also affects the binary package, or even the required
package ID can change your own package ID:

.. code-block:: python

    def package_id(self):
        # Default behavior, only major release changes the package ID
        self.info.requires["MyOtherLib"].semver_mode()

        # Any change in the require version will change the package ID
        self.info.requires["MyOtherLib"].full_version_mode()

        # Any change in the MyOtherLib version, user or channel will affect our package ID
        self.info.requires["MyOtherLib"].full_recipe_mode()

        # Any change in the MyOtherLib version, user or channel or Package ID will affect our package ID
        self.info.requires["MyOtherLib"].full_package_mode()

        # The requires won't affect at all to the package ID
        self.info.requires["MyOtherLib"].unrelated_mode()

You can also adjust the individual properties manually:

.. code-block:: python

    def package_id(self):
        myotherlib = self.info.requires["MyOtherLib"]

        # Same as myotherlib.semver_mode()
        myotherlib.name = myotherlib.full_name
        myotherlib.version = myotherlib.full_version.stable()
        myotherlib.user = myotherlib.channel = myotherlib.package_id = None

        # Only the channel (and the name) matters
        myotherlib.name = myotherlib.full_name
        myotherlib.user = myotherlib.package_id = myotherlib.version = None
        myotherlib.channel = myotherlib.full_channel

The result of the ``package_id()`` is the package ID hash, but the details can be checked in the
generated *conaninfo.txt* file. The ``[requires]``, ``[options]`` and ``[settings]`` are those taken
into account to generate the SHA1 hash for the package ID, while the [full_xxxx] fields show the
complete reference information.

The default behavior produces a *conaninfo.txt* that looks like:

.. code-block:: text

    [requires]
      MyOtherLib/2.Y.Z

    [full_requires]
      MyOtherLib/2.2@demo/testing:73bce3fd7eb82b2eabc19fe11317d37da81afa56

Library types: Shared, static, header only
++++++++++++++++++++++++++++++++++++++++++

Let's see some examples, corresponding to common scenarios:

- ``MyLib/1.0`` is a shared library that links with a static library ``MyOtherLib/2.0`` package.
  When a new ``MyOtherLib/2.1`` version is released: Do I need to create a new binary for
  ``MyLib/1.0`` to link with it?

  Yes, always, because the implementation is embedded in the ``MyLib/1.0`` shared library. If we
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

  It depends, if the public headers have not changed at all, it is not necessary. Actually it might
  be necessary to consider transitive dependencies that are shared among the public headers, how
  they are linked and if they cross the frontiers of the API, it might also lead to
  incompatibilities. If public headers have changed, it would depend on what changes and how are
  they used in ``MyLib/1.0``. Adding new methods to the public headers will have no impact, but
  changing the implementation of some functions that will be inlined when compiled from
  ``MyLib/1.0`` will definitely require re-building. For this case, it could make sense:

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

  Never, the package should always be the same, there are no settings, no options, and in any way a
  dependency can affect a binary, because there is no such binary. The default behavior should be
  changed to:

  .. code-block:: python

      def package_id(self):
          self.info.requires.clear()

- ``MyLib/1.0`` is a static library, linking with a header only library in ``MyOtherLib/2.0``
  package. When a new ``MyOtherLib/2.1`` version is released: Do I need to create a new binary for
  ``MyLib/1.0`` to link with it? It could happen that the ``MyOtherLib`` headers are strictly used
  in some ``MyLib`` headers, which are not compiled, but transitively #included. But in the general
  case it is likely that ``MyOtherLib`` headers are used in ``MyLib`` implementation files, so every
  change in them should imply a new binary to be built. If we know that changes in the channel never
  imply a source code change, because it is the way we have defined our workflow/lifecycle, we could
  write:

  .. code-block:: python

      def package_id(self):

          self.info.requires["MyOtherLib"].full_package()
          self.info.requires["MyOtherLib"].channel = None # Channel doesn't change out package ID
