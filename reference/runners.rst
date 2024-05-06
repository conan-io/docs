.. _reference_runners:

Runners
=======

Runners are the way to run Conan remotely and transparently just by modifying the host profile. There are three requirements to be able to use the feature:

- Installing a version of conan with runner dependencies ``pip install conan[runners]``. 
- Install the tools to run each of the runners (``docker``).
- Add to the ``host profile`` the ``[runner]`` section defined in the documentation of each runner.

Runners:

.. toctree::
    :maxdepth: 1

    runners/docker
