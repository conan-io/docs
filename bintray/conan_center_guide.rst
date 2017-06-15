.. _conan_center_flow:

Contributing packages to conan-center
=====================================

As a moderated and curated repository, `conan-center`_ will not be populated automatically. Initially, it will be empty.
To have your recipe or binary package available on `conan-center`_, you need to submit an inclusion request to Bintray,
and the Bintray team will review your request.

- If you are the author of an open source library, your package will be approved.
  Keep in mind that it is your responsibility to maintain acceptable standards of quality for all packages you submit
  for inclusion in `conan-center`_.

- If you are packaging a third-party library you need to follow the guidelines below.


Inclusion guidelines for third party libraries
**********************************************

In the inclusion request process, the JFrog staff will perform a general review and will make suggestions for improvements or
better/cleaner ways to do implement the code.


Recipe quality
--------------

- **Github public repository**: The recipe needs to be hosted in a public Github repository.

- **Recipe fields**: `description`, `license` and `url` are required.

- **Linter:** Is important to have a reasonable clean Linter, ``conan export`` and  ``conan test_package`` will
  output some warnings and errors, keep it as clean as possible to guarantee a recipe less error prone and more understandable.

- **Updated:** Not using deprecated features and when possible, using latest conan features, build helpers etc.

- **Clean:** The code style will be reviewed to guarantee the readability of the recipe.

- **test_package:** The recipes must contain a :ref:`test_package<packaging_getting_started>`



CI Integration
--------------

- Unless your library doesn't support a concrete operating system or compiler you will need to provide a CI systems integration
  to support:

    - **Linux:** GCC, desirable latest version from each major (4.9, 5.4, 6.3)
    - **Linux:** Clang
    - **Windows:** Visual Studio 12, 14 and 15 (or newer)


- The easiest way to provide the CI integration (with Appveyor for Windows builds and Travis.ci for Linux and OSX) is to
  use the :ref:`conan new<conan_new>` command. Take a look to the options to generate a library layout with the needed appveyor/travis.

  You can also copy the following files from this `zlib Conan package repository`_ and adapt them:

    - ``.travis`` folder. Not needed to adjust anything.
    - ``.travis.yml`` file. Adjust your username, library reference etc
    - ``appveyor.yml`` file. Adjust your username, library reference etc

- Take a look to the :ref:`Travis CI<travis_integration>` and :ref:`Appveyor<appveyor_integration>` integration guides.



Bintray library page information
--------------------------------


In the bintray page of your package fill the following fields:

    - Description (description of the packaged library)
    - Licenses (license of the packaged library)
    - Tags
    - Maturity
    - Website: If any, website of the library
    - Issues tracker: URL of the issue tracker from your github repository e.j: https://github.com/lasote/conan-zlib/issues
    - Version control: URL of your recipe github repository. e.j: https://github.com/lasote/conan-zlib
    - GitHub repo (user/repo): e.j lasote/conan-zlib

In each version page (optional, but welcomed):

    - Select the README from github.
    - Select the Release Notes.


.. _`zlib Conan package repository`: https://github.com/lasote/conan-zlib
.. _`conan-center`: https://bintray.com/conan/conan-center