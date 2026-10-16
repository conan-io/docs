Using Conan
===========

How to package header-only libraries?
--------------------------------------

Packaging header-only libraries is similar to other packages. Be sure to start by reading and understanding the
:ref:`packaging getting started guide<packaging_getting_started>`. The main difference is that a package recipe is typically much simpler.
There are different approaches depending on if you want Conan to run the library unit tests while creating the package or not. Full details are described
:ref:`in this how-to guide<header_only>`.

When to use settings or options?
--------------------------------

While creating a package, you may want to add different configurations and variants of the package. There are two main inputs that define
packages: settings and options. Read more about them in :ref:`this section<settings_vs_options>`.

How to obtain the dependents of a given package?
------------------------------------------------

The search model for Conan in commands such as :command:`conan install` and :command:`conan info` is done from the downstream or "consumer"
package as the starting node of the dependency graph and upstream.

.. code-block:: bash

    $ conan info poco/1.9.4@

.. image:: /images/conan-info_graph.png
   :align: center

The inverse model (from upstream to downstream) is not simple to obtain for Conan packages. This is because the dependency graph is not unique, it
changes for every configuration. The graph can be different for different operating systems or just by changing some package options. So you
cannot query which packages are dependent on ``my_lib/0.1@user/channel``, but which packages are dependent on
``my_lib/0.1@user/channel:63da998e3642b50bee33`` binary package. Also, the response can contain many different binary packages for the same
recipe, like ``my_dependent/0.1@user/channel:packageID1... ID2... my_dependent/0.1@user/channel:packageIDN``. That is the reason why
:command:`conan info` and :command:`conan install` need a profile (default profile or one given with ``--profile```) or installation files
``conanbuildinfo.txt`` to look for settings and options.

In order to show the inverse graph model, the bottom node is needed to build the graph upstream and an additional node too to get the inverse
list. This is usually done to get the build order in case a package is updated. For example, if we want to know the build order of the Poco
dependency graph in case OpenSSL is changed we could type:

.. code-block:: bash

    $ conan info poco/1.9.4@ -bo openssl/1.0.2t
    WARN: Usage of `--build-order` argument is deprecated and can return wrong results. Use `conan graph build-order ...` instead.
    [openssl/1.0.2t], [poco/1.9.4]

If OpenSSL is changed, we would need to rebuild it (of course) and rebuild Poco.

Packages got outdated when uploading an unchanged recipe from a different machine
---------------------------------------------------------------------------------

Usually this is caused due to different line endings in Windows and Linux/macOS. Normally this happens when Windows uploads it with CRLF
while Linux/macOS do it with only LF. Conan does not change the line endings to not interfere with user. We suggest always using LF line
endings. If this issue is caused by git, it could be solved with :command:`git config --system core.autocrlf input`.

The *outdated* status is computed from the recipe hash, comparing the hash of the recipe used to create a binary package and the
current recipe. The recipe hash is the hash of all the files included in the *conanmanifest.txt* file (you can inspect this file in
your cache with :command:`conan get <ref> conanmanifest.txt`). The first value in the manifest file is a timestamp and is not taken
into account to compute the hash. Checking and comparing the contents of the different *conanmanifest.txt* files in the different
machines can give an idea of what is changing.

If you want to make the solution self-contained, you can add a *.git/config* file in your project that sets the ``core.autocrlf`` property
(for the whole repo), or if you need a per-file configuration, you could use the *.gitattributes* file to set the ``text eol=lf`` for every
file you want.

.. _faq_recommendation_user_channel:

Is there any recommendation regarding which ``<user>`` or ``<channel>`` to use in a reference?
----------------------------------------------------------------------------------------------

A Conan reference is defined by the following template: ``<library-name>/<library-version>@<user>/<channel>``

The ``<user>`` term in a Conan reference is basically a namespace to avoid collisions of libraries with the same name and version in the
local cache and in the same remote. This field is usually populated with the author's name of the package recipe (which could be different
from the author of the library itself) or with the name of the organization creating it. Here are some examples from Conan Center:

.. code-block:: text

    OpenSSL/1.1.1@conan/stable
    CLI11/1.6.1@cliutils/stable
    CTRE/2.1@ctre/stable
    Expat/2.2.5@pix4d/stable
    FakeIt/2.0.5@gasuketsu/stable
    Poco/1.9.0@pocoproject/stable
    c-blosc/v1.14.4@francescalted/stable

In the case of the ``<channel>`` term, normally OSS package creators use ``testing`` when developing a recipe (e.g. it compiles
only in few configurations) and ``stable`` when the recipe is ready enough to be used (e.g. it is built and tested in a wide range of
configurations).

From the perspective of a library developer, channels could be used to create different scopes of your library. For example, use ``rc``
channel for release candidates, maybe ``experimental`` for those kind of features, or even ``qa``/``testing`` before the library is checked
by QA department or testers.

What does "outdated from recipe" mean exactly?
----------------------------------------------

In some output or commands there are references to "outdated" or "outdated from recipe". For example, there is a flag :command:`--outdated`
in :command:`conan search` and :command:`conan remove` to filter by outdated packages.

When packages are created, Conan stores some metadata of the package such as the settings, the final resolution of the dependencies... and
it also saves the recipe hash of the recipe contents they were generated with. This way Conan is able to know the real relation between a
recipe and a package.

Basically outdated packages appear when you modify a recipe and export and/or upload it, without re-building binary packages with it. This
information is displayed in yellow with:

.. code-block:: bash

    $ conan search pkg/0.1@user/channel --table=file.html
    # open file.html
    # It will show outdated binaries in yellow.

This information is important to know if the packages are up to date with the recipe or even if the packages are still "accessible" from the
recipe. That means: if the recipe has completely removed an option (it could be a setting or a requirement) but there are old packages
that were generated previously with that option, those packages will be impossible to install as their package ID are calculated from the
recipe file (and that option does not exist anymore).

How to configure the remotes priority order
-------------------------------------------

The lookup remote order is defined by the command :command:`conan remote`:

.. code-block:: bash

    $ conan remote list
    conan-center: https://conan.bintray.com [Verify SSL: True]
    conan-community: https://api.bintray.com/conan/conan-community/conan [Verify SSL: True]

As you can see, the remote ``conan-center`` is listed on index **0**, which means it has the highest priority when searching or installing a package,
followed by ``conan-community``, on index **1**. To update the index order, the argument ``--insert`` can be added to the command :command:`conan remote update`:

.. code-block:: bash

    $ conan remote update conan-community https://api.bintray.com/conan/conan-community/conan --insert
    $ conan remote list
    conan-community: https://api.bintray.com/conan/conan-community/conan [Verify SSL: True]
    conan-center: https://conan.bintray.com [Verify SSL: True]


The ``--insert`` argument means *index 0*, the highest priority, thus the ``conan-community`` remote will be updated as the first remote to be used.

It's also possible to define a specific index when adding a remote to the list:

.. code-block:: bash

    $ conan remote add bincrafters https://api.bintray.com/conan/bincracters/public-conan --insert 1
    $ conan remote list
    conan-community: https://api.bintray.com/conan/conan-community/conan [Verify SSL: True]
    bincrafters: https://api.bintray.com/conan/bincrafters/public-conan [Verify SSL: True]
    conan-center: https://conan.bintray.com [Verify SSL: True]


The ``bincrafters`` remote needs to be added after ``conan-community``, so we need to set the remote index as **1**.
