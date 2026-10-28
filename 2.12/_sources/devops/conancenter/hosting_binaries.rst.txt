.. _devops_conancenter_hosting_your_own_conancenter_fork:

Creating and hosting your own ConanCenter binaries
==================================================


Hosting your own copy of the packages you need in your server could be done by just downloading binaries from ConanCenter and then uploading them to your own server. However, it is much better to fully own the complete supply chain and create the binaries in your own CI systems. So the recommended flow to use ConanCenter packages in production would be:

- Create a fork of the ConanCenter Github repository: https://github.com/conan-io/conan-center-index
- Create a list of the packages and versions you need for your projects. This list can be added to the fork too, and maintained there (packages can be added and removed with PRs when the teams need them).
- Create a script that first ``conan export`` all the packages in your list, then ``conan create --build=missing`` them. Do not add ``user/channel`` to these packages, it is way simpler to use them as ``zlib/1.2.13`` without user-channel. The ``user/channel`` part would be mostly recommended for your own proprietary packages, but not for open source ConanCenter packages.
- Upload your build packages to your own server, that you use in production, instead of ConanCenter.

This is the basic flow idea. We will be adding examples and tools to further automate this flow as soon as possible.


This flow is relatively straightforward, and has many advantages that mitigate the risks described before:

- No central repository outage can affect your builds.
- No changes in the central repository can break your projects, you are in full control when and how those changes are updated in your packages (as explained below).
- You can customize, adapt, fix and perfectly control what versions are used, and release fixes in minutes, not weeks. You can apply customizations that wouldn't be accepted in the central repository.
- You fully control the binaries supply chain, from the source (recipes) to the binaries, eliminating in practice the majority of potential supply chain attacks of central repositories.


Updating from upstream
++++++++++++++++++++++

Updating from the upstream ``conan-center-index`` Github repo is still possible, and it can be done in a fully controlled way:

- Merge the latest changes in the upstream main fork of ``conan-center-index`` into your fork.
- You can check and audit those changes if you want to, analyzing the diffs (some automation that trims the diffs of recipes that you don't use could be useful)
- Firing the above process will efficiently rebuild the new binaries that are needed. If your recipes are not affected by changes, the process will avoid rebuilding binaries (thanks to ``--build=missing``).
- You can upload the packages to a secondary "test" server repository. Then test your project against that test server, to check that your project is not broken by the new ConanCenter packages.
- Once you verify that everything is good with the new packages, you can copy them from the secondary "test" repository to your main production repository to start using them.
