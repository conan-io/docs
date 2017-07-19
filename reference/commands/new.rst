
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
     name           Package name, e.g.: Poco/1.7.8p3@pocoproject/stable

   optional arguments:
     -h, --help     show this help message and exit
     -t, --test     Create test_package skeleton to test package
     -i, --header   Create a headers only package template
     -c, --pure_c   Create a C language package only package, deleting
                    "self.settings.compiler.libcxx" setting in the configure
                    method
     -s, --sources  Create a package with embedded sources in "hello" folder,
                    using "exports_sources" instead of retrieving external code
                    with the "source()" method
     -b, --bare     Create the minimum package recipe, without build() or
                    package()methods. Useful in combination with "package_files"
                    command
     -cis, --ci_shared           Package will have a "shared" option to be used in CI
     -cilg, --ci_travis_gcc      Generate travis-ci files for linux gcc
     -cilc, --ci_travis_clang    Generate travis-ci files for linux clang
     -cio, --ci_travis_osx       Generate travis-ci files for OSX apple-clang
     -ciw, --ci_appveyor_win     Generate appveyor files for Appveyor Visual Studio
     -ciglg, --ci_gitlab_gcc     Generate GitLab files for linux gcc
     -ciglc, --ci_gitlab_clang   Generate GitLab files for linux clang
     -gi, --gitignore            Generate a .gitignore with the known patterns to
                                 excluded
     -ciu CI_UPLOAD_URL, --ci_upload_url CI_UPLOAD_URL Define URL of the repository to upload

**Examples**:


- Create a new ``conanfile.py`` for a new package **mypackage/1.0@myuser/stable**

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable


- Create also a ``test_package`` folder skeleton:

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable -t


- Create files for travis (both Linux and OSX) and appveyor Continuous Integration:

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable -t -cilg -cio -ciw

- Create files for gitlab (linux) Continuous integration and set upload conan server:

.. code-block:: bash

  $ conan new mypackage/1.0@myuser/stable -t -ciglg -ciglc -ciu https://api.bintray.com/conan/myuser/myrepo
