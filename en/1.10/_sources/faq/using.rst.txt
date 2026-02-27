Using conan
===========

How to package header-only libraries?
--------------------------------------

Packaging header-only libraries is similar to other packages, make sure to first read and understand the
:ref:`packaging getting started guide<packaging_getting_started>`. The main difference is that the package recipe is typically much simpler.
There are different approaches depending if you want Conan to run the library unit tests while creating the package or not. Full details
:ref:`in this how-to<header_only>`.

When to use settings or options?
--------------------------------

While creating a package you might want to add different configurations and variants of the package. There are 2 main inputs that define
packages: settings and options. Read about them in :ref:`this section<settings_vs_options>`

How to obtain the dependents of a given package?
------------------------------------------------

The search model for Conan in commands such as :command:`conan install` and :command:`conan info` is done from the downstream or "consumer"
package as the starting node of the dependency graph and upstream.

.. code-block:: bash

    $ conan info Poco/1.8.1@pocoproject/stable

.. image:: /images/conan_info_graph.png
   :align: center

The inverse model (from upstream to downstream) is not simple to obtain for Conan packages, because the dependency graph is not unique: It
changes for every configuration. The graph can be different for different operating systems or just by changing some package options. So you
cannot query which packages are dependent on ``MyLib/0.1@user/channel``, but which packages are dependent on
``MyLib/0.1@user/channel:63da998e3642b50bee33`` binary package, and the response can contain many different binary packages for the same
recipe, like ``MyDependent/0.1@user/channel:packageID1... ID2... MyDependent/0.1@user/channel:packageIDN``. That is the reason why
:command:`conan info` and :command:`conan install` need a profile (default profile or one given with ``--profile```) or installation files
``conanbuildinfo.txt`` to look for settings and options.

In order to show the inverse graph model, the bottom node is needed to build the graph upstream and an additional node too to get the inverse
list. This is usually done to get the build order in case a package is updated. For example, if we want to know the build order of the Poco
dependency graph in case OpenSSL is changed we could type:

.. code-block:: bash

    $ conan info Poco/1.8.1@pocoproject/stable -bo OpenSSL/1.0.2m@conan/stable
    [OpenSSL/1.0.2m@conan/stable], [Poco/1.8.1@pocoproject/stable]

So, if OpenSSL is changed, we would need to rebuild it (of course) and rebuild Poco.

Packages got outdated when uploading an unchanged recipe from a different machine
---------------------------------------------------------------------------------

Usually this is caused due to different line endings in Windows and Linux/macOS. Normally this happens when Windows uploads it with CRLF
while Linux/macOS do it with only LF. Conan does not change the line endings to not interfere with user. We suggest going with LF line
endings always. If this is being caused by git, it could be solved with :command:`git config --system core.autocrlf input`.

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

In the case of the ``<channel>`` term, normally OSS package creators use ``testing`` when they are developing a recipe (e.g., It compiles
only in few configurations) and ``stable`` when the recipe is ready enough to be used (e.g., It is built and tested in a wide range of
configurations).

From the perspective of a library developer, channels could be used to create different scopes of your library. For example, use ``rc``
channel for release candidates, maybe ``experimental`` for those kind of features, or even ``qa``/``testing`` before the library is checked
by QA department or testers.
