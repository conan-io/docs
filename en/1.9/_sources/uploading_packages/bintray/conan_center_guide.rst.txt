.. _conan_center_flow:

Contributing Packages to Conan-Center
=====================================

The `conan-center` is a moderated and curated repository that is not populated automatically.
Initially, it is empty. To have your recipe or binary packages available on `conan-center`_,
submit an inclusion request to Bintray and the Bintray team will review your request.

Your request is dealt with differently depending on the submitted package type:

- If you are the **author of an open source library**, your package will be approved. Keep in mind
  that it is your responsibility to maintain acceptable standards of quality for all packages you
  submit for inclusion in `conan-center`_.

- If you are packaging a third-party library, follow these guidelines:

Contributing a library to Conan-Center is really straightforward when you know how to
:ref:`upload your packages to your own Bintray repository<uploading_to_bintray>`. All you have to do is to navigate to the main page of the
package in Bintray and click the **"Add to Conan Center"** button to start the inclusion request process.

.. image:: /images/add_to_conan-center.png
    :align: center

Inclusion Guidelines for Third-Party libraries
**********************************************

During the inclusion request process, the JFrog staff will perform a general review and will make
suggestions for improvements or better ways to implement the package.

A Single Conan Package Per OSS Library
--------------------------------------

Before creating packages for third-party libraries, please read these general guidelines.

- Ensure that there is no additional Conan package for the same library. If you are planning to support a
  new version of a library that already exists in the ``conan-center`` repository, please contact
  the package author and collaborate. All the versions of the same library have to be on the same
  Bintray Conan package.

- It is recommended to contact the **library author** and suggest to maintain the Conan package.
  When possible, open a pull request to the original repository of the library with the required Conan
  files or suggest to open a new repository with the recipe.

- If you are going to collaborate with different users to maintain the Conan package, open a Bintray organization.

Recipe Quality
--------------

- **Git public repository**: The recipe needs to be hosted in a public Git repository that supports
  collaboration.

- **Recipe fields**: `description`, `license` and `url` are required. The `license` field refers to
  the library being packaged.

- **Linter:** Is important to have a reasonably clean Linter, :command:`conan export` and  :command:`conan create`
  otherwise it will generate warnings and errors. Keep it as clean as possible to guarantee a recipe less
  prone to error and more coherent.

- **Updated:** Don't use deprecated features and when possible use the latest Conan features, build
  helpers, etc.

- **Clean:** The code style will be reviewed to guarantee the readability of the recipe.

- **test_package:** The recipes must contain a :ref:`test_package<packaging_getting_started>`.

- **Maintenance commitment:** You are responsible for keeping the recipe updated, fix issues
  etc., so be aware that a minimal commitment is required. The Conan organization reserves the right to unlink a
  poorly maintained package or replace it with better alternatives.

- **Raise errors on invalid configurations:** If the library doesn't work for a specific
  configuration, e.g., requires **gcc>7**, the recipe must contain a ``configure(self)`` method  that
  raises an exception in case of invalid settings/options.

  .. code-block:: python

    def configure():
        if self.settings.compiler == "gcc" and self.settings.compiler.version < "7.0":
            raise ConanException("GCC > 7.0 is required")
        if self.settings.os == "Windows":
            raise ConanException("Windows not supported")

- **Without version ranges**: Due to the fact that many libraries do not follow semantic versioning, and that dependency resolution of version ranges is not
  always clear, recipes in the Conan center should fix the version of their dependencies and not use version ranges.

- **LICENSE of the recipe:** The public repository must contain a ``LICENSE`` file with an OSS
  license.

- **LICENSE of the library:** Every built binary package must contain one or more ``license*``
  file(s), so make sure that in the ``package()`` method of your recipe, you include the library
  licenses in the ``licenses`` subfolder.

  .. code-block:: python

    def package():
        self.copy("license*", dst="licenses",  ignore_case=True, keep_path=False)

  Sometimes there is no ``license`` file, and you will need to extract the license from a header file, as in the following example:

  .. code-block:: python

    def package():
        # Extract the License/s from the header to a file
        tmp = tools.load("header.h")
        license_contents = tmp[2:tmp.find("*/", 1)] # The license begins with a C comment /* and ends with */
        tools.save("LICENSE", license_contents)

        # Package it
        self.copy("license*", dst="licenses",  ignore_case=True, keep_path=False)

- **Invalid configurations:** There is a special exception, ``conans.errors.ConanInvalidConfiguration`` to be launched
  from ``configure()`` function in a recipe if the given configuration/options is known not to work. This way the recipe
  owner can declare an invalid configuration and consumers (e.g. CI tools like ``conan-package-tools``) will be able to
  handle it.


CI Integration
--------------

- If you are packaging a header-only library, you will only need to provide one CI configuration
  (e.g., Travis with gcc 6.1) to validate that the package is built correctly (use :command:`conan create`).

- Unless your library is a header-only library or doesn't support a concrete operating system or
  compiler, you will need to provide a CI systems integration to support:

    - **Linux:** GCC, latest version recommended from each major (4.9, 5.4, 6.3)
    - **Linux:** Clang, latest version recommended from each major (3.9, 4.0)
    - **Mac OSX:** Two latest versions of apple-clang, e.g., (8.0, 8.1) or newer.
    - **Windows:** Visual Studio 12, 14 and 15 (or newer)

- The easiest way to provide the CI integration (with Appveyor for Windows builds, Travis.ci for
  Linux and OSX, and Gitlab for Linux) is to use the :ref:`conan new<conan_new>` command. Take a
  look at the options to generate a library layout with the required appveyor/travis/gitlab.

  You can also copy the following files from this `zlib Conan package repository`_ and modify them:

    - ``.travis`` folder. No need to adjust anything.
    - ``.travis.yml`` file. Adjust your username, library reference, etc.
    - ``appveyor.yml`` file. Adjust your username, library reference, etc.

- Take a look at the :ref:`Travis CI<travis_integration>`, :ref:`Appveyor<appveyor_ci>` and
  :ref:`GitLab CI<gitlab_integration>` integration guides.

Bintray Package Data
--------------------

In the Bintray page of your package, fill in the following fields:

    - Description (description of the packaged library)
    - Licenses (license of the packaged library)
    - Tags
    - Maturity
    - Website: If any, website of the library
    - Issues tracker: URL of the issue tracker from your github repository e.g.,
      https://github.com/conan-community/conan-zlib/issues
    - Version control: URL of your recipe github repository, e.g.,
      https://github.com/conan-community/conan-zlib
    - GitHub repo (user/repo): e.g., conan-community/conan-zlib

For each version page (optional, but recommended):

    - Select the README from github.
    - Select the Release Notes.

.. _`zlib Conan package repository`: https://github.com/conan-community/conan-zlib
.. _`conan-center`: https://bintray.com/conan/conan-center
