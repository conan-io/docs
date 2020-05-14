
.. _conan_new:

conan new
=========

.. code-block:: bash

    $ conan new [-h] [-t] [-i] [-c] [-s] [-b] [-cis] [-cilg] [-cilc] [-cio]
                [-ciw] [-ciglg] [-ciglc] [-gi] [-ciu CI_UPLOAD_URL]
                name

Creates a new package recipe template with a ``conanfile.py`` and optionally, ``test_package``
package testing files.

.. code-block:: bash

    positional arguments:
      name                  Package name, e.g.: "Poco/1.7.3" or complete reference
                            for CI scripts: "Poco/1.7.3@conan/stable"

    optional arguments:
      -h, --help            show this help message and exit
      -t, --test            Create test_package skeleton to test package
      -i, --header          Create a headers only package template
      -c, --pure-c          Create a C language package only package, deleting
                            "self.settings.compiler.libcxx" setting in the
                            configure method
      -s, --sources         Create a package with embedded sources in "src"
                            folder, using "exports_sources" instead of retrieving
                            external code with the "source()" method
      -b, --bare            Create the minimum package recipe, without build()
                            methodUseful in combination with "export-pkg" command
      -cis, --ci-shared     Package will have a "shared" option to be used in CI
      -cilg, --ci-travis-gcc
                            Generate travis-ci files for linux gcc
      -cilc, --ci-travis-clang
                            Generate travis-ci files for linux clang
      -cio, --ci-travis-osx
                            Generate travis-ci files for OSX apple-clang
      -ciw, --ci-appveyor-win
                            Generate appveyor files for Appveyor Visual Studio
      -ciglg, --ci-gitlab-gcc
                            Generate GitLab files for linux gcc
      -ciglc, --ci-gitlab-clang
                            Generate GitLab files for linux clang
      -gi, --gitignore      Generate a .gitignore with the known patterns to
                            excluded
      -ciu CI_UPLOAD_URL, --ci-upload-url CI_UPLOAD_URL
                            Define URL of the repository to upload

**Examples**:

- Create a new ``conanfile.py`` for a new package **mypackage/1.0@myuser/stable**

  .. code-block:: bash

      $ conan new mypackage/1.0

- Create also a ``test_package`` folder skeleton:

  .. code-block:: bash

      $ conan new mypackage/1.0 -t

- Create files for travis (both Linux and OSX) and appveyor Continuous Integration:

  .. code-block:: bash

      $ conan new mypackage/1.0@myuser/stable -t -cilg -cio -ciw

- Create files for gitlab (linux) Continuous integration and set upload conan server:

  .. code-block:: bash

      $ conan new mypackage/1.0@myuser/stable -t -ciglg -ciglc -ciu https://api.bintray.com/conan/myuser/myrepo
