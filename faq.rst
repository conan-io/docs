.. _faq:

FAQ
===


Is Conan CMake based, or is CMake a requirement?
------------------------------------------------
No, it isnt. Conan is build-system agnostic. Package creators could probably use it to create
their packages. You will only need CMake if you want to build packages from source, or you need
to, cause there are no available packages for your system/settings. We use CMake extensively
in our examples and documentation, but because it is very convenient and most C/C++ devs are
used to it. 


Is build-system XXXXX supported?
--------------------------------
Yes, it is. Conan makes no assumption about the build system, it just wraps any build commands,
as specified by the package creators. There are already some helper methods in code to ease the
use of cmake, but similar functions can be very easily added for your favourite build system, so
please send us your PRs!

Does it run offline?
--------------------
Yes, it runs offline very smoothly. Binary packages are stored in your machine, per user, so
you can start new projects that depends on the same libraries without any connection at all.
Packages can be fully createad and tested locally, prior uploading them to the desired server.

Can I run conan server behind the firewall (in-house)?
------------------------------------------------------
Yes, conan does not require connection to the conan repository at all for its operation. You can
install packages from the conan repository if you want, test them, and only after approval upload
them to your in-house server, then forget about the original repository. Or you can just get
the build scripts, and re-build from source in your premises, then upload the packages to your
server.

Can I create packages for third-party libraries?
------------------------------------------------
Of course, as long as their license allows it.

Can I upload closed source libraries?
-------------------------------------
Yes, as long as the resulting binary artifact can be distributed freely, and free of charge at least
for educational and research purposes, and you comply with all possible licenses and IP rights of
the original authors, and the Terms of Service.
If you want to distribute your libraries only for your paying customers, please contact us.


Do I always need to specify how to build the package from source?
-----------------------------------------------------------------
No, but it is highly recommended. If you want, you can just directly start with the binaries,
built elsewhere, and upload them directly. Maybe your get_code() step can download pre-compiled
binaries from other source, and unzip them, with an empty build() step.

Does conan use semantic versioning (semver) for dependencies?
-------------------------------------------------------------
It uses a convention that a package dependencies follow semver by default, thus it is not necessary
to recompile new packages if you update upstream minor versions, but it will do it when you
update to major versions. This behavior can be easily configured and changed in your conanfile ``conan_info()``
method, and any versioning scheme is supported.