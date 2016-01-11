.. _changelog:


Changelog
=========

Check https://github.com/conan-io/conan for issues and more details about development, contributors, etc.

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
  


