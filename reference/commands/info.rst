

conan info
==========

.. code-block:: bash

   $ usage: conan info [-h] [--file FILE] [--only [ONLY]]
                  [--build_order BUILD_ORDER] [--update] [--scope SCOPE]
                  [--profile PROFILE] [-r REMOTE] [--options OPTIONS]
                  [--settings SETTINGS] [--env ENV]
                  [--build [BUILD [BUILD ...]]]
                  [reference]

Prints information about a package recipe's dependency graph.
You can use it for your current project (just point to the path of your conanfile if you want), or for any
existing package in your local cache.


The ``--update`` option will check if there is any new recipe/package available in remotes. Use ``conan install -u``
to update them.


.. code-block:: bash

    positional arguments:
      reference             reference name or path to conanfile file, e.g.,
                            MyPackage/1.2@user/channel or ./my_project/

    optional arguments:
      --file FILE, -f FILE  specify conanfile filename
      --only [ONLY], -n [ONLY]
                            show fields only
      --build_order BUILD_ORDER, -bo BUILD_ORDER
                            given a modified reference, return an ordered list to
                            build (CI)
      --update, -u          check updates exist from upstream remotes
      --scope SCOPE, -sc SCOPE
                            Use the specified scope in the install command
      --profile PROFILE, -pr PROFILE
                            Apply the specified profile to the install command
      -r REMOTE, --remote REMOTE
                            look in the specified remote server
      --options OPTIONS, -o OPTIONS
                            Options to build the package, overwriting the
                            defaults. e.g., -o with_qt=true
      --settings SETTINGS, -s SETTINGS
                            Settings to build the package, overwriting the
                            defaults. e.g., -s compiler=gcc
      --env ENV, -e ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]
                            given a build policy (same install command "build"
                            parameter), return an ordered list of packages that
                            would be built from sources in install command
                            (simulation)


**Examples**:

.. code-block:: bash

   $ conan info
   $ conan info myproject_path
   $ conan info Hello/1.0@user/channel

The output will look like:

.. code-block:: bash

   Dependency/0.1@user/channel
    URL: http://...
    License: MIT
    Updates: Version not checked
    Required by:
        Hello/1.0@user/channel

   Hello/1.0@user/channel
       URL: http://...
       License: MIT
       Updates: Version not checked
       Required by:
           Project
       Requires:
           Hello0/0.1@user/channel


It is possible to use the ``conan info`` command to extract useful information for Continuous
Integration systems. More precisely, it has the ``--build_order, -bo`` option, that will produce
a machine-readable output with an ordered list of package references, in the order they should be
built. E.g., lets assume that we have a project that depends on Boost and Poco, which in turn
depends on OpenSSL and ZLib transitively. So we can query our project with a reference that has
changed (most likely due to a git push on that package):

.. code-block:: bash

    $ conan info -bo zlib/1.2.8@lasote/stable
    [zlib/1.2.8@lasote/stable], [OpenSSL/1.0.2g@lasote/stable], [Boost/1.60.0@lasote/stable, Poco/1.7.2@lasote/stable]

Note the result is a list of lists. When there is more than one element in one of the lists, it means
that they are decoupled projects and they can be built in parallel by the CI system.

Also you can get a list of nodes that would be built (simulation) in an install command specifying a build policy with the ``--build`` parameter:

e.g., If I try to install ``Boost/1.60.0@lasote/stable`` recipe with ``--build missing`` build policy and ``arch=x86``, which libraries will be build?

.. code-block:: bash

	$ conan info Boost/1.60.0@lasote/stable --build missing -s arch=x86
	bzip2/1.0.6@lasote/stable, zlib/1.2.8@lasote/stable, Boost/1.60.0@lasote/stable

