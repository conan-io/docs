.. _integrations_bazel:

|bazel_logo| Bazel
==================

Conan provides different tools to help manage your projects using Bazel. They can be
imported from ``conan.tools.google``. The most relevant tools are:

- ``BazelDeps``: the dependencies generator for Bazel, which generates a *[DEPENDENCY]/BUILD.bazel* file for each dependency
  and a *dependencies.bzl* file containing a Bazel function to load all those ones. That function must be loaded by your
  *WORKSPACE* file.

- ``BazelToolchain``: the toolchain generator for Bazel, which generates a ``conan_bzl.rc`` file that contains
  a build configuration ``conan-config`` to inject all the parameters into the :command:`bazel build` command.

- ``Bazel``: the Bazel build helper. It's simply a wrapper around the command line invocation of Bazel.

.. seealso::

    - Reference for :ref:`conan_tools_google_bazeldeps`.
    - Reference for :ref:`conan_tools_google_bazeltoolchain`.
    - Reference for :ref:`conan_tools_google_bazel`.
    - :ref:`examples_tools_bazel_toolchain_build_simple_bazel_project`


.. |bazel_logo| image:: ../images/integrations/conan-bazel-logo.png
