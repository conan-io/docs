Using conan
===========

How to package header-only libraries?
--------------------------------------
Packaging header-only libraries is similar to other packages, make sure to first read and understand the
:ref:`packaging getting started guide<packaging_getting_started>`. The main difference is that the package recipe is typically much simpler.
There are different approaches depending if you want conan to run the library unit tests while creating the package or not. Full details
:ref:`in this how-to<header_only>`.

When to use settings or options?
--------------------------------
While creating a package you might want to add different configurations and variants of the package. There are 2 main inputs that define
packages: settings and options. Read about them in :ref:`this section<settings_vs_options>`

How to obtain the dependents of a given package?
------------------------------------------------

The search model for conan in commands such as :command:`conan install` and :command:`conan info` is done from the downstream or "consumer" package as
the starting node of the dependency graph and upstream.

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

In order to show the inverse graph model, the bottom node is neeed to build the graph upstream and an additonal node too to get the inverse
list. This is usually done to get the build order in case a package is updated. For example, if we want to know the build order of the Poco
dependecy graph in case OpenSSL is changed we could type:

.. code-block:: bash

    $ conan info Poco/1.8.1@pocoproject/stable -bo OpenSSL/1.0.2m@conan/stable
    [OpenSSL/1.0.2m@conan/stable], [Poco/1.8.1@pocoproject/stable]

So, if OpenSSL is changed, we would need to rebuild it (of course) and rebuild Poco.

Packages got outdated when uploading an unchanged recipe from a different machine
---------------------------------------------------------------------------------

Usually this is caused due to different line endings in Windows and Linux/MacOS. Normally this happens when Windows uploads it with CRLF
while Linux/MacOS do it with only LF. Conan does not change the line endings to not interfere with user. We suggest going with LF line
endings always. If this is being caused by git, it could be solved with :command:`git config --system core.autocrlf input`.
