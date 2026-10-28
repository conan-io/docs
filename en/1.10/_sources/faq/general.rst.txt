General
............

Is Conan CMake based, or is CMake a requirement?
------------------------------------------------
No. It isn't. Conan is build-system agnostic. Package creators could very well use cmake to
create their packages, but you will only need it if you want to build packages from source, or
if there are no available precompiled packages for your system/settings. We use CMake extensively
in our examples and documentation, but only because it is very convenient and most C/C++ devs are
familiar with it.

Is build-system XXXXX supported?
--------------------------------
Yes. It is. Conan makes no assumption about the build system. It just wraps any build commands
specified by the package creators. There are already some helper methods in code to ease the
use of CMake, but similar functions can be very easily added for your favorite build system.
Please check out the alternatives explained in :ref:`generator packages <dyn_generators>`

Is my compiler, version, architecture, or setting supported?
---------------------------------------------------------------
Yes. Conan is very general, and does not restrict any configuration at all.
However, conan comes with some compilers, versions, architectures, ..., etc. pre-configured in the
``~/.conan/settings.yml`` file, and you can get an error if using settings not present in that file.
Go to :ref:`invalid settings<error_invalid_setting>` to learn more about it.

Does it run offline?
--------------------
Yes. It runs offline very well. Package recipes and binary packages are stored in your machine, per user, and so
you can start new projects that depend on the same libraries without any Internet connection at all.
Packages can be fully created, tested and consumed locally, without needing to upload them anywhere.

Is it possible to install 2 different versions of the same library?
-------------------------------------------------------------------
Yes. You can install as many different versions of the same library as you need, and easily
switch among them in the same project, or have different projects use different versions simultaneously,
and without having to install/uninstall or re-build any of them.

Package binaries are stored per user in (e.g.) ``~/.conan/data/Boost/1.59/user/stable/package/{sha_0, sha_1, sha_2...}``
with a different SHA signature for every different configuration (debug, release, 32-bit, 64-bit, compiler...).
Packages are managed per user, but additionally differentiated by version and channel, and also by their configuration.
So large packages, like Boost, don't have to be compiled or downloaded for every project.

Can I run multiple conan isolated instances (virtual environments) on the same machine?
----------------------------------------------------------------------------------------
Yes, conan supports the concept of virtual environments; so it manages all the information (packages, remotes, user credentials, ..., etc.) in different, isolated environments.
Check :ref:`virtual environments<custom_cache>` for more details.


Can I run the conan_server behind a firewall (on-premises)?
-----------------------------------------------------------
Yes. Conan does not require a connection to conan.io site or any other external service at all for its operation. You can
install packages from the bintray conan-center repository if you want, test them, and only after approval, upload
them to your on-premises server and forget about the original repository. Or you can just get
the package recipes, re-build from source on your premises, and then upload the packages to your
server.

Can I connect to conan remote servers through a corporate proxy?
---------------------------------------------------------------------
Yes, it can be configured in your **~/.conan/conan.conf** configuration file or with some
environment variables. Check :ref:`proxy configuration <proxys>` for more details.


Can I create packages for third-party libraries?
------------------------------------------------
Of course, as long as their license allows it.

Can I upload closed source libraries?
-------------------------------------
Yes. As long as the resulting binary artifact can be distributed freely and free of charge, at least
for educational and research purposes, and as long as you comply with all licenses and IP rights of the original
authors, as well as the Terms of Service.
If you want to distribute your libraries only for your paying customers, please contact us.

Do I always need to specify how to build the package from source?
-----------------------------------------------------------------
No. But it is highly recommended. If you want, you can just directly start with the binaries,
build elsewhere, and upload them directly. Maybe your ``build()`` step can download pre-compiled
binaries from another source and unzip them, instead of actually compiling from sources.

Does conan use semantic versioning (semver) for dependencies?
-------------------------------------------------------------
It uses a convention by which package dependencies follow semver by default; thus it intelligently
avoids recompilation/repackaging if you update upstream minor versions, but will correctly do so if you
update major versions upstream. This behavior can be easily configured and changed in the ``package_id()``
method of your conanfile, and any versioning scheme you desire is supported.
