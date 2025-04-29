.. _reference_runners:

Runners
=======

.. include:: ../common/experimental_warning.inc

Runners provide a seamless method to execute Conan on remote build environments like Docker ones, directly from your local setup by simply configuring your host profile.

- Installing a version of Conan with runner dependencies ``pip install conan[runners]``. 
- Install the tools to run each of the runners (``docker``).
- Add the ``[runner]`` section defined in the documentation of each runner to the host profile.

Runners:

.. toctree::
    :maxdepth: 1

    runners/docker
