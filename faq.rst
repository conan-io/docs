.. _faq:

FAQ
===


Is Conan CMake based, or is CMake a requirement?
------------------------------------------------
No, it isn't. Conan is build-system agnostic. Package creators could very well use cmake to
create their packages, but you will only need it if you want to build packages from source, or
if there are no available precompiled packages for your system/settings. We use CMake extensively
in our examples and documentation, but only because it is very convenient and most C/C++ devs are
familiar with it. 


Is build-system XXXXX supported?
--------------------------------
Yes, it is. Conan makes no assumption about the build system. It just wraps any build commands
specified by the package creators. There are already some helper methods in code to ease the
use of cmake, but similar functions can be very easily added for your favourite build system,
so please send us your PRs!

Does it run offline?
--------------------
Yes, it runs offline very smoothly. Binary packages are stored in your machine, per user, so
you can start new projects that depend on the same libraries without any connection at all.
Packages can be fully createad and tested locally, prior to uploading them to the desired server.

How does conan compare to biicode dependency manager?
-----------------------------------------------------
A (probably not complete) list of differences:

- It is fully decentralized, git-like style. The provided on-premises server is very easy to run.
- It is build-system agnostic, and highly decoupled from builds. It uses cmake a lot and integrates well with it, but there are packages built with perl+nmake, autotools, etc. Consumers can use any available generator (visual studio, xcode, gcc, txt or cmake). They are not forced to use cmake.
- Consumers are not locked-in to the techonology. They are just provided with a file with include paths, lib paths, libs, etc, so they can use that info. System package managers can perfectly coexist with it.
- It hosts and manages pre-built binaries. You can decide to build from source or use existing binaries. Binaries are cached in your computer at the user-level, so there is no need to build the same large binary twice for different projects. Many versions of binaries can coexist, different projects can use different versions, and it is easy to switch between versions in the same project (without rebuilding).
- Python package recipes allow for very advanced configuration: static, dynamic, 32, 64 bits, conditional dependencies (depending on OS, version, compiler, settings, options...) in a more intuitive cycle: source-build-package
- It is not required to host the source code. It can be retrieved from any origin like github, sourceforge download+unzip, etc.
- Creating packages for existing libraries is much, much faster than with biicode, and practically zero-intrusive in the library project. The package itself can be an external repository with a URL to the existing library origin. You can fully create and test packages on your machine, prior to uploading them to any remote (including your own).

Is it possible to install 2 different versions of the same library?
-------------------------------------------------------------------
Yes, you can install as many different versions of the same library as you need, and easily
switch among them in the same project, or have different projects use different versions simultaneously,
and without having to install/uninstall or re-build any of them.

Package binaries are stored per user in ~/.conan/data/Boost/1.59/user/stable/package/{sha1, sha2, sha3...} 
with a different sha signature for every different configuration (debug, release, 32, 64, compiler...). 
Packages are managed per user, but additionally differentiated by version and channel, and also by their configuration.
So large packages, like Boost, don't have to be compiled or downloaded for every project.


Can I run the conan server behind a firewall (on-premises)?
-----------------------------------------------------------
Yes, conan does not require a connection to the conan repository at all for its operation. You can
install packages from the conan repository if you want, test them, and only after approval upload
them to your on-premises server and forget about the original repository. Or you can just get
the build scripts, re-build from source on your premises, and then upload the packages to your
server.

Can I create packages for third-party libraries?
------------------------------------------------
Of course, as long as their license allows it.

Can I upload closed source libraries?
-------------------------------------
Yes, as long as the resulting binary artifact can be distributed freely and free of charge, at least
for educational and research purposes, and you comply with all licenses and IP rights of the original
authors, as well as the Terms of Service.
If you want to distribute your libraries only for your paying customers, please contact us.

Do I always need to specify how to build the package from source?
-----------------------------------------------------------------
No, but it is highly recommended. If you want, you can just directly start with the binaries,
build elsewhere, and upload them directly. Maybe your get_code() step can download pre-compiled
binaries from another source and unzip them, with an empty build() step.

Does conan use semantic versioning (semver) for dependencies?
-------------------------------------------------------------
It uses a convention by which package dependencies follow semver by default, thus it is not necessary
to recompile new packages if you update upstream minor versions, but it will do so when you
update major versions. This behavior can be easily configured and changed in the ``conan_info()``
method of your conanfile, and any versioning scheme is supported.
