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


Can Conan use git repositories as package servers?
--------------------------------------------------

Or put it with other words, can a conan recipe define requirements something like ``requires="git://github.com/someuser/somerepo.git#sometag"``?

No, it is not possible. There are several technical reasons for this, mainly around the dependency resolution algorithm, but also about performance:

- Conan manages dependency versions conflicts. These can be efficiently handled from the abstract reference quickly, while a git repo reference would require cloning contents even before deciding.
- The version overriding mechanism from downstream consumers to resolve conflicts cannot be implemented either with git repos, as both the name and the version of the package is not defined.
- Conan support version-ranges, like depending on ``boost/[>1.60 <1.70]``. This is basically impossible to implement in git repos.
- Conan has an “update” concept, that allows to query servers for latest modifications, latest versions, or even latest revisions, which would not work at all with git repos either.
- Binary management is one of the biggest advantages of Conan. Obviously, it is not possible to manage binaries for this case either.

In summary, whatever could be done would be an extremely limited solution, very likely inefficient and much slower, with a lot of corner cases and rough edges around those said limitations. It would require a big development effort, and the compounded complexity it would induce in the codebase is a liability that will slow down future development, maintenance and support efforts.

Besides the impossibility on the technical side, there are also other reasons like well known best practices around package management and modern devops in other languages that show evidence that even if this approach looks like convenient, it should be discouraged in practice:

- Packages should be fully relocatable to a different location. Users should be able to retrieve their dependencies and upload a copy to their own private server, and fully disconnect from the external world. This is critical for robust and secure production environments, and avoid problems that other ecosystems like NPM have had in the past. As a consequence, all recipes dependencies should not be coupled to any location, and be abstract as conan "requires" are.
- Other languages, like Java (which would be the closest one regarding enterprise-ness), never provided this feature. Languages like golang, that based its dependency management on this feature, has also evolved away from it and towards abstract "module" concepts that can be hosted in different servers

So there are no plans to support this approach, and the client-server architecture will continue to be the proposed solution. There are several alternatives for the servers from different vendors, for public open source packages `ConanCenter <https://conan.io/center>`_ is the recommended one, and for private packages, the free `ArtifactoryCE <https://conan.io/downloads>`_ is a simple and powerful solution.


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
    WARN: Usage of `--build-order` argument is deprecated and can return wrong results. Use `conan lock build-order ...` instead.
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

It is strongly recommended that packages are considered immutable. Once a package has been created with a user/channel, it shouldn't be
changed. Instead, a new package with a new user/channel should be created.


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

When using "revisions" (it is opt-in in Conan 1.X, but it will be always enabled in Conan 2.0), this should never happen, as doing any change
to a recipe or source should create a new revision that will contain its own binaries.

How to configure the remotes priority order
-------------------------------------------

The lookup remote order is defined by the command :command:`conan remote`:

.. code-block:: bash

    $ conan remote list
    conan-center: https://conan.bintray.com [Verify SSL: True]
    myremote: https://MyTeamServerIP:8081/artifactory/api/conan/myremote [Verify SSL: True]

As you can see, the remote ``conan-center`` is listed on index **0**, which means it has the highest priority when searching or installing a package,
followed by ``myremote``, on index **1**. To update the index order, the argument ``--insert`` can be added to the command :command:`conan remote update`:

.. code-block:: bash

    $ conan remote update myremote https://MyTeamServerIP:8081/artifactory/api/conan/myremote --insert
    $ conan remote list
    myremote: https://MyTeamServerIP:8081/artifactory/api/conan/myremote [Verify SSL: True]
    conan-center: https://conan.bintray.com [Verify SSL: True]


The ``--insert`` argument means *index 0*, the highest priority, thus the ``myremote`` remote will be updated as the first remote to be used.

It's also possible to define a specific index when adding a remote to the list:

.. code-block:: bash

    $ conan remote add otherremote https://MyCompanyOtherIP:8081/artifactory/api/conan/otherremote --insert 1
    $ conan remote list
    myremote: https://MyTeamServerIP:8081/artifactory/api/conan/myremote [Verify SSL: True]
    otherremote: https://MyCompanyOtherIP:8081/artifactory/api/conan/otherremote [Verify SSL: True]
    conan-center: https://conan.bintray.com [Verify SSL: True]


The ``otherremote`` remote needs to be added after ``myremote``, so we need to set the remote index as **1**.
