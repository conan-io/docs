.. _remote_repositories:

Working with Conan remote repositories
======================================

We already :ref:`learned how to download and use packages <tutorial_consuming_packages>`
from `Conan Center <https://conan.io/center>`_ that is the official repository for open
source Conan packages. We also :ref:`learned how to create our own packages
<tutorial_creating_packages>` and store them in the Conan local cache for reusing later.
In this section we cover how you can use the Conan remote repositories to upload your
recipes and binaries and store them for consuming them later.

First we will cover how you can setup a Conan remote repository locally or cloud-hosted
(you can skip this part if you already have a Conan remote configured). Then we will cover
the process of uploading the packages to our own repositories and how to operate when you
have multiple Conan remotes configured. Finally, we will briefly cover how you can
contribute to the Conan Center central repository. 

.. toctree::
   :maxdepth: 2
   :caption: Table of contents
   
   remote_repositories/build_simple_cmake_project
   remote_repositories/use_tools_as_conan_packages
   remote_repositories/different_configurations
   remote_repositories/the_flexibility_of_conanfile_py
   remote_repositories/cross_building_with_conan.rst
   remote_repositories/intro_to_versioning
