.. _setup_local_recipes_index:

Local Recipes Index Repository
==============================

The `local_recipes_index` repository is a special type of repository to which you cannot
upload packages or store binaries. The purpose of this remote is:

- Enable contributors to share package recipes with the community, particularly for
  libraries that might not be suitable for ConanCenter.

- It also simplifies the process of building binaries from a private `conan-center-index`
  fork, allowing absolute control over recipes, customization, and maintaining a stable
  repository snapshot. This ensures robustness against upstream changes in ConanCenter.
  For detailed setup and usage instructions, see the dedicated section in the Conan DevOps
  Guide :ref:`devops_local_recipes_index`.

Setup
-----

To set up a local recipes index repository to share your own recipes, you need to organize
your recipes in a folder structure that mimics that of `conan-center-index`. To start you
can use the `local_recipes_index` template for the `conan new` command. For demonstration
purposes, let's create a `local-recipes-index` repository for a hypothetical `hello`
library, with a license incompatible with Conan Center, using the `local_recipes_index`
template for the `conan new` command:

.. code-block:: bash

    $ mkdir repo && cd repo $ conan new local_recipes_index -d name=hello -d version=0.1 \
        -d url=https://github.com/conan-io/libhello/archive/refs/tags/0.0.1.zip \ -d
        sha256=1dfb66cfd1e2fb7640c88cc4798fe25853a51b628ed9372ffc0ca285fe5be16b
    $ cd ..

The `conan new local_recipes_index` command creates a template that assumes CMake as the
build system alongside other heavy assumptions. In practice, it will require customizing
it, but for this demo, it works as-is. It will create a folder layout equal to the
`conan-center-index` GitHub repository:

.. code-block:: bash

    .
    └── repo
        └── recipes
            └── hello
                ├── all
                │   ├── conandata.yml
                │   ├── conanfile.py
                │   └── test_package
                │       ├── CMakeLists.txt
                │       ├── conanfile.py
                │       └── src
                │           └── example.cpp
                └── config.yml

After setting up the repository, we add it as a local remote to Conan:

.. code-block:: bash

    $ conan remote add mylocalrepo ./repo --allowed-packages="hello/*"

Please pay special attention to the `--allowed-packages` argument. This argument ensures
that all packages other than `hello` are discarded by Conan. This can be used to minimize
the surface area for a potential supply chain attack.

Now you can list and install packages from this new repository:

.. code-block:: bash

    $ conan list "*" -r=mylocalrepo
    $ conan install --requires=hello/0.1 -r=mylocalrepo --build=missing

At this point, you could push this repository to your GitHub account and share it with the
community. Now, users simply need to clone the GitHub repository and add the cloned folder
as a local repository themselves.

.. note::

    Please be aware that, as we commented earlier, this feature is specifically tailored
    for scenarios where certain libraries are not suitable for ConanCenter. Remember, a
    "local-recipes-index" repository has limitations: it is not fully reproducible as it
    models only versions and not revisions, and it does not provide binaries. Therefore,
    outside of these cases, it is advised to use a remote package server such as
    :ref:`Artifactory <artifactory_ce_cpp>`.

.. seealso::

    - :ref:`DevOps guide <devops>`
    - `Introducing the Local-Recipes-Index Post <https://blog.conan.io/2024/04/23/Introducing-local-recipes-index-remote.html>`_
