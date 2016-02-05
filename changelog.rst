.. _changelog:


Changelog
=========

Check https://github.com/conan-io/conan for issues and more details about development, contributors, etc.

0.7 (5-Feb-2016)
----------------

- Custom conanfile names are allowed for developing. With ``--file`` option you can define
  the file you want to use, allowing for ``.conaninfo.txt`` or having multiple ``conanfile_dev.py``,
  ``conanfile_test.py`` besides the standard ``conanfile.py`` which is used for sharing the package.
  Inheritance is allowed, e.g. ``conanfile_dev.py`` might extend/inherit from ``conanfile.py``.
- New ``conan copy`` command that can be used to copy/rename packages, promote them between channels,
  forking other users packages.
- New ``--all`` and ``--package`` options for ``conan install`` that allows to download one, several,
  or all package configurations for a given reference.
- Added ``patch()`` tool to easily patch sources if necessary.
- New **qmake** and **qbs** generators
- Upload of conanfile **exported** files is also **tgz'd**, allowing fast upload/downloads of
  full sources if desired, avoiding retrieval of sources from externals sources.
- ``conan info`` command improved showing info of current project too
- Output of ``run()`` can be redirected to buffer string for processing, or even removed.
- Added **proxy** configuration to conan.conf for users behinds proxies.
- Large improvements in commands output, prefixed with package reference, and much clear.
- Updated settings for more versions of gcc and new arm architectures
- Treat dependencies includes as SYSTEM in cmake, so no warnings are raised
- Deleting source folder after ``conan export`` so no manual removal is needed
- Normalizing to CRLF generated user files in Win
- Better detection and checks for compilers as VS, apple-clang
- Fixed CMAKE_SHARED_LINKER_FLAGS typo in cmake files
- Large internal refactor in generators


0.6 (11-Jan-2016)
-----------------

- New cmake variables in cmake generator to make FindPackage work better thanks to the underlaying FindLibrary. Now many FindXXX.cmake work "as-is" and the package creator does not have to create a custom override, and consumers can use packages transparently with the originals FindXXX.cmakes
- New "conan info" command that shows the full dependency graph and details (license, author, url, dependants, dependencies) for each dependency.
- New environment helper with a ConfigureEnvironment class, that is able to translate conan information to autotools configure environment definition
- Relative importing from conanfiles now is possible. So if you have common functionality between different packages, you can reuse those python files by importing them from the conanfile.py. Note that export="..." might be necessary, as packages as to be self-contained.
- Added YouCompleteMe generator for vim auto-completion of dependencies.
- New "conanfile_directory" property that points to the file in which the conanfile.py is located. This helps if using the conanfile.py "build" method to build your own project as a project, not a package, to be able to use any workflow, out-of-source builds, etc.
- Many edits and improvements in help, docs, output messages for many commands.
- All cmake syntax in modern lowercase
- Fixed several minor bugs: gcc detection failure when gcc not installed, missing import, copying source->build failing when symlinks


0.5 (18-Dec-2015)
-----------------

- New cmake functionality allows package creators to provide cmake finders, so that package consumers
  can use their CMakeLists.txt with typical FindXXX.cmake files, without any change to them. CMake CONAN_CMAKE_MODULES_PATH
  added, so that package creators can provide any additional cmake scripts for consumers.
- Now it is possible to generate out-of-source and multiple configuration installations for the
  same project, so you can switch between them without having to ``conan install`` again. Check :ref:`the new workflows<workflows>`
- New qmake generator (thanks @dragly)
- Improved removal/deletion of folders with shutil.rmtree, so ``conan remove`` commands and other
  processes requiring deletion of folders do not fail due to permissions and require manual deletion.
  This is an improvement, especially in Win.
- Created ``pip`` package, so conan can be installed via: ``pip install conan``
- Released ``pyinstaller`` code for the creation of binaries from conan python source code. Distros package creators can
  create packages for the conan apps easily from those binaries.
- Added md5, sha1, sha256 helpers in ``tools``, so external downloads from ``conanfile.py`` files ``source()``
  can be checked.
- Added latest gcc versions to default ``settings.yml``
- Added CI support for conan development: travis-ci, appveyor
- Improved human-readability for download progress, help messages.
- Minor bug fixes
  


