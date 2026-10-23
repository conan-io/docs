.. _integrations_bazel:

|bazel_logo| Bazel
==================

Conan provides different tools to help manage your projects using Bazel. They can be
imported from ``conan.tools.google``. The most relevant tools are:

- ``BazelDeps``: the dependencies generator for Bazel, which generates a *[DEPENDENCY]/BUILD.bazel* file for each dependency
  and a *conan_deps.MODULE.bazel* file that loads all of them. Include it from your *MODULE.bazel* file (Bazel >= 7.2).
  The Bazel 6.x *dependencies.bzl* file loaded from a *WORKSPACE* is still generated, but it is deprecated since Conan 2.34.

- ``BazelToolchain``: the toolchain generator for Bazel, which generates a ``conan_bzl.rc`` file that contains
  a build configuration ``conan-config`` to inject all the parameters into the :command:`bazel build` command.

- ``Bazel``: the Bazel build helper. It's simply a wrapper around the command line invocation of Bazel.

.. seealso::

    - Reference for :ref:`conan_tools_google_bazeldeps`.
    - Reference for :ref:`conan_tools_google_bazeltoolchain`.
    - Reference for :ref:`conan_tools_google_bazel`.
    - :ref:`examples_tools_bazel_toolchain_build_simple_bazel_project`
    - :ref:`examples_tools_bazel_7x_toolchain_build_simple_bazel_project`


.. |bazel_logo| image:: ../images/integrations/conan-bazel-logo.png
