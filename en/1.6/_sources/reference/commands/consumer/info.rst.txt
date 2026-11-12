
.. _conan_info:

conan info
==========

.. code-block:: bash

    $ conan info [-h] [--paths] [-bo BUILD_ORDER] [-g GRAPH]
                 [-if INSTALL_FOLDER] [-j [JSON]] [-n ONLY]
                 [--package-filter [PACKAGE_FILTER]] [-db [DRY_BUILD]]
                 [-b [BUILD]] [-e ENV] [-o OPTIONS] [-pr PROFILE] [-r REMOTE]
                 [-s SETTINGS] [-u]
                 path_or_reference

Gets information about the dependency graph of a recipe. It can be used with a
recipe or a reference for any existing package in your local cache.

.. code-block:: text

    positional arguments:
      path_or_reference     Path to a folder containing a recipe (conanfile.py or
                            conanfile.txt) or to a recipe file. e.g.,
                            ./my_project/conanfile.txt. It could also be a
                            reference

    optional arguments:
      -h, --help            show this help message and exit
      --paths               Show package paths in local cache
      -bo BUILD_ORDER, --build-order BUILD_ORDER
                            given a modified reference, return an ordered list to
                            build (CI)
      -g GRAPH, --graph GRAPH
                            Creates file with project dependencies graph. It will
                            generate a DOT or HTML file depending on the filename
                            extension
      -if INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            local folder containing the conaninfo.txt and
                            conanbuildinfo.txt files (from a previous conan
                            install execution). Defaulted to current folder,
                            unless --profile, -s or -o is specified. If you
                            specify both install-folder and any setting/option it
                            will raise an error.
      -j [JSON], --json [JSON]
                            Only with --build_order option, return the information
                            in a json. e.g --json=/path/to/filename.json or --json
                            to output the json
      -n ONLY, --only ONLY  Show only the specified fields: "id", "build_id",
                            "remote", "url", "license", "requires", "update",
                            "required", "date", "author", "None". '--paths'
                            information can also be filtered with options
                            "export_folder", "build_folder", "package_folder",
                            "source_folder". Use '--only None' to show only
                            references.
      --package-filter [PACKAGE_FILTER]
                            Print information only for packages that match the
                            filter pattern e.g., MyPackage/1.2@user/channel or
                            MyPackage*
      -db [DRY_BUILD], --dry-build [DRY_BUILD]
                            Apply the --build argument to output the information,
                            as it would be done by the install command
      -b [BUILD], --build [BUILD]
                            Given a build policy, return an ordered list of
                            packages that would be built from sources during the
                            install command
      -e ENV, --env ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      -o OPTIONS, --options OPTIONS
                            Define options values, e.g., -o Pkg:with_qt=true
      -pr PROFILE, --profile PROFILE
                            Apply the specified profile to the install command
      -r REMOTE, --remote REMOTE
                            Look in the specified remote server
      -s SETTINGS, --settings SETTINGS
                            Settings to build the package, overwriting the
                            defaults. e.g., -s compiler=gcc
      -u, --update          Check updates exist from upstream remotes


**Examples**:

.. code-block:: bash

    $ conan info .
    $ conan info myproject_folder
    $ conan info myproject_folder/conanfile.py
    $ conan info Hello/1.0@user/channel

The output will look like:

.. code-block:: bash

    Dependency/0.1@user/channel
     ID: 5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9
     BuildID: None
     Remote: None
     URL: http://...
     License: MIT
     Updates: Version not checked
     Creation date: 2017-10-31 14:45:34
     Required by:
        Hello/1.0@user/channel

    Hello/1.0@user/channel
     ID: 5ab84d6acfe1f23c4fa5ab84d6acfe1f23c4fa8
     BuildID: None
     Remote: None
     URL: http://...
     License: MIT
     Updates: Version not checked
     Required by:
        Project
     Requires:
        Hello0/0.1@user/channel

:command:`conan info` builds the complete dependency graph, like :command:`conan install` does. The main
difference is that it doesn't try to install or build the binaries, but the package recipes
will be retrieved from remotes if necessary.

It is very important to note, that the :command:`info` command outputs the dependency graph for a
given configuration (settings, options), as the dependency graph can be different for different
configurations. Then, the input to the :command:`conan info` commmand is the same as :command:`conan install`,
the configuration can be specified directly with settings and options, or using profiles.

Also, if you did a previous :command:`conan install` with a specific configuration, or maybe different
installs with different configurations, you can reuse that information with the :command:`--install-folder`
argument:

.. code-block:: bash

    $ # dir with a conanfile.txt
    $ mkdir build_release && cd build_release
    $ conan install .. --profile=gcc54release
    $ cd .. && mkdir build_debug && cd build_debug
    $ conan install .. --profile=gcc54debug
    $ cd ..
    $ conan info . --install-folder=build_release
    > info for the release dependency graph install
    $ conan info . --install-folder=build_debug
    > info for the debug dependency graph install

It is possible to use the :command:`conan info` command to extract useful information for Continuous
Integration systems. More precisely, it has the :command:`--build_order, -bo` option, that will produce
a machine-readable output with an ordered list of package references, in the order they should be
built. E.g., lets assume that we have a project that depends on Boost and Poco, which in turn
depends on OpenSSL and ZLib transitively. So we can query our project with a reference that has
changed (most likely due to a git push on that package):

.. code-block:: bash

    $ conan info . -bo zlib/1.2.11@conan/stable
    [zlib/1.2.11@conan/stable], [OpenSSL/1.0.2l@conan/stable], [Boost/1.60.0@lasote/stable, Poco/1.7.8p3@pocoproject/stable]

Note the result is a list of lists. When there is more than one element in one of the lists, it means
that they are decoupled projects and they can be built in parallel by the CI system.

You can also specify the ``ALL`` argument, if you want just to compute the whole dependency graph build order

.. code-block:: bash

    $ conan info . --build_order=ALL
    > [zlib/1.2.11@conan/stable], [OpenSSL/1.0.2l@conan/stable], [Boost/1.60.0@lasote/stable, Poco/1.7.8p3@pocoproject/stable]


Also you can get a list of nodes that would be built (simulation) in an install command specifying a build policy with the ``--build`` parameter:

e.g., If I try to install ``Boost/1.60.0@lasote/stable`` recipe with ``--build missing`` build policy and ``arch=x86``, which libraries will be built?

.. code-block:: bash

	$ conan info Boost/1.60.0@lasote/stable --build missing -s arch=x86
	bzip2/1.0.6@lasote/stable, zlib/1.2.8@lasote/stable, Boost/1.60.0@lasote/stable


You can generate a graph of your dependencies, in dot or html formats:

.. code-block:: bash

    $ conan info .. --graph=file.html
    $ file.html # or open the file, double-click

.. image:: /images/info_deps_html_graph.png
    :height: 250 px
    :width: 300 px
    :align: center
