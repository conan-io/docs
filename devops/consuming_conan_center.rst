.. _devops_consuming_conan_center:

Using ConanCenter packages in production
========================================

ConanCenter is a fantastic resource that contains a huge knowledge base and a reference implementation of recipes contributed by the community on how to create and build Conan packages for a lot of open source third party libraries and applications supporting multiple platforms.

It also provides pre-compiled binaries for a wide range of configurations: multiple OS, including Windows, Linux and OSX, a variety of compilers, compiler versions, static and shared libraries, etc. These precompiled packages can be very useful to do quick experiments, testing, onboarding, and they also serve as a proof that the recipes for those packages can work solidly for that wide range of configurations.

However, it is not advised to depend directly on ConanCenter for production environments, for several reasons:

- ConanCenter accepts contributions that require the most recently released versions of Conan. If you are in an environment where you are unable to keep Conan up-to-date across all your systems (developers, CI, etc) - depending directly on recipes from ConanCenter carries the risk of retrieving recipes that do not work with your older version of Conan.
- The changes in recipes might also unpexectedly cause bugs and other issues. Recipes and package updates might bump dependencies versions to use the latest, forcing a continuous update over all dependencies versions. That can cause version conflicts if your project doesn't bump dependencies versions at the same pace.
- Reviews in ConanCenter can take a while to be reviewed and merged, as there is usually a high volume of requests. Please consider this if you may find yourself in a situation where you may need proposed changes merged with urgency. Pull Requests are considered according to priorities and resources, and will only be accepted with positive peer reviews by the Conan team.
- Binary configurations can be discontinued in ConanCenter, when new compiler versions are released and ConanCenter starts to build them, it can drop some of the older versions.
- Outages, maintenance windows and other service interruptions can happen, ranging from a few minutes to days. The infrastructure to host central repositories is typically large and complex, and relies on cloud providers that sometimes have their own issues, networks, CDN, etc.
- Supply chain issues. Even if the best effort is made to make ConanCenter secure and the process to add packages to ConanCenter is one of the most strict ones with human reviews for every package and many automated checks and processes, eventually all systems and central repositories in every technology are subject to attempts of supply chain attacks.

Most of these reasons are not unique to Conan, but to every other package manager for other programming languages. 

.. important::
  
  The general devops known good practice is that you shouldn't rely on central repositories on production systems, but do consider the following approaches:

  - If your project is mostly a "consuming" project, i.e. you are not generating your own packages, but just consuming packages from ConanCenter, and the above issues are not a concern because your project does not need that kind of robustness or security, then you can use **lockfiles** to at least guarantee that your project build using the same dependencies over time. Check :ref:`the lockfile docs<tutorial_versioning_lockfiles>` for more information.
  - If you are creating your own packages for your own libraries or applications, or any of the above reasons is a concern for your production environment, then the recommended approach is **hosting your own copy of the packages you need for production** in your own private server.

We have seen many Conan users succesfully using the second approach, building and hosting their own binaries in their own repository, even for "consuming" cases. The process for doing that is not complicated (and we are working to further streamline it) and in practice it is advangeous in most cases. Let's see how this can be done:



Creating and hosting your own ConanCenter binaries
--------------------------------------------------

Hosting your own copy of the packages you need in your server could be done by just downloading binaries from ConanCenter and then uploading them to your own server. However, it is much better to fully own the complete supply chain and create the binaries in your own CI systems. So the recommended flow to use ConanCenter packages in production would be:

- Create a fork of the ConanCenter Github repository: https://github.com/conan-io/conan-center-index
- Create a list of the packages and versions you need for your projects. This list can be added to the fork too, and maintained there (packages can be added and removed with PRs when the teams need them).
- Create a script that first ``conan export`` all the packages in your list, then ``conan create --build=missing`` them. Do not add ``user/channel`` to these packages, it is way simpler to use them as ``zlib/1.2.13`` without user-channel. The ``user/channel`` part would be mostly recommended for your own proprietary packages, but not for open source ConanCenter packages.
- Upload your build packages to your own server, that you use in production, instead of ConanCenter.

This is the basic flow idea. We will be adding examples and tools to further automate this flow as soon as possible.


This flow is relatively straightforward, and has many advantages that mitigate the above risks:

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


.. note::

  **Best practices**

  - Do not use ConanCenter packages on production systems, store the packages you need in your own server and use them from there.
  - Create your own binaries from your fork to completely own the pipeline, remove all breakage risks, accelerate fixes and remove security supply chain attacks. The process is not complicated and really worth it.
  - You can drop the ``conancenter`` remote from your clients to make sure packages are not accidentally downloaded from there. Use ``conan config install`` with your own ``remotes.json`` file to remove ``conancenter`` default remote.
