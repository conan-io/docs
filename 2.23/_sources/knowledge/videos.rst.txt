.. _videos:

Videos
======

.. warning::

    This section presents some conference talks and presentations regarding Conan.
    While they can be very informative and educational, please note that some of them might
    be outdated. Always use the documentation and reference as the source of truth, not the
    videos.

.. _accu2025:


ACCU 2025
---------
`Continuous Integration for Large Scale C/C++ Projects With Conan2` by Diego Rodriguez-Losada

    There are two main paradigms to develop large scale C, C++ projects: using mono-repos and package-based development, both have different pros and cons. Using package managers such as Conan allows easy retrieval of dependencies, including binaries, avoiding continuous and expensive rebuilds from source.
    While this works easily for third party dependencies, when dependencies are very stable, quick evolution in a large dependency graph when there are different developers working concurrently in different packages, can be more challenging.

    With Conan 2's new tools it is possible to implement an efficient Continuous Integration process for large scale projects, computing what packages need to be built, and in what specific order and parallelism.

    The concept of "products pipeline" will be introduced as an scalable approach that allows to focus on the business value while allowing efficiency. The dependency graph build order for every different product can be computed, for every different configuration (platform, compiler, build_type, etc). This is done efficiently, taking into account the versioning scheme and the package types (header-only, static library, shared library, application) with a explicit novel model of the dependencies effect in the packages binaries.

    Then all the different computed graph "build-orders" can be merged into a single one to avoid duplicated builds. The final graph merged "build-order" can be distributed efficiently to different build agents, as it also specifies which package builds can be done in parallel. For projects with concurrent changes, using lockfiles is very important in this stage to guarantee consistency and reproducibility of the dependencies.

    Finally, the concept of stages in the CI process using multiple server repositories and copying of packages across those repositories will be presented. This process is known as package promotions and is a known best practice in DevOps for other technologies, and is critical to avoid disruptions to developers and production systems that the CI builds could introduce.

    The talk will present both the theoretical foundations and a full real example with available source code to demonstrate the presented functionalities.


.. youtube:: A3X1MpvYTrM


.. _cppcon2024:

Using std::cpp 2024
-------------------
`Unlock the power of Conan 2 - 15 new features you didn’t know about! Luis Caro / Diego Rodriguez-Losada`

    | Conan 2.0 was released over a year ago with a large number of new features and improvements. Since its release, the team has continued to add improvements based on user feedback, releasing many more new features than in the previous years combined.
    | Join Diego and Luis from the Conan team for an overview of practical examples of what Conan 2 can do for your C and C++ package management development workflows. Some highlights include: transparent fall back to system-provided dependencies, managing metadata files, and the flexible and fully transparent CMake integrations, and more!

.. youtube:: yC3ERwB-Njc

.. _accu2022:

ACCU 2022
---------
`Advanced Dependencies Model in Conan 2.0 C, C++ Package Manager by Diego Rodriguez-Losada`

    Conan 2.0 introduces a new dependencies model with requirements "traits" like visibility,
    definition and propagation of headers and libraries independently, and more that allow modeling all these advanced use cases.
    This talk will present this new model, and apply it to solve different advanced use cases, with real life examples

.. youtube:: kKGglzm5ous

.. _cppcon2022:

CppCon 2022
-----------
`What's New in Conan 2.0 C/C++ Package Manager - Diego Rodriguez-Losada`

    During the years since Conan 1.0 was released, we have continued to learn from the C++ ecosystem as we watched it grow;
    learning many lessons, challenges and trends in the industry from the feedback from tens of thousands of conversations with users and customers,
    including many of the largest C++ related companies in the world. This talk summarizes some of these lessons
    and how they have been used to create the new major version of Conan.

.. youtube:: NM-xp3tob2Q

.. _meeting_cpp2023:

Meeting C++ 2023
----------------
`CMake and Conan: past, present and future - Diego Rodriguez-Losada`

    | This talk will quickly review the past approaches, their pitfalls, and how modern CMake and Conan integrations have improved over them:
    | From variables, to targets, to transparent targets integration with modern Conan generators
    | Better separation of concerns to align binary configurations using CMake toolchains
    | Improving the developer experience with CMake presets
    | The new CMake-Conan integration using CMake’s new dependency providers feature for transparent installation of dependencies

.. youtube:: s0q6s5XzIrA

.. _using_stdcpp2021:

Using std::cpp
--------------
`Why you shouldn’t write your own C++ package manager Luis Caro Campos JFrog`

    |  This talk will provide a quick overview of how Conan deals with intrinsic C++ complexities:
    |  Headers vs binary symbols
    |  Shared and static library
    |  Symbol visibility
    |  Binary compatibility: is there a one-size fits all approach to modeling it?
    |  Build-time dependency resolution is only half the battle, what about runtime dependencies?

.. youtube:: 8Go5g2jVJWo

.. _cpp_book_fair2023:

Meeting C++ online book & tool fair
-----------------------------------
`Conan 2.0 demo - Chris McArthur`

.. youtube:: 1q5oIOupwjg
