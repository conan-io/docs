.. _conan_repositories:

Working with Conan repositories
===============================

We already :ref:`learned how to download and use packages <tutorial_consuming_packages>`
from `Conan Center <https://conan.io/center>`_ that is the official repository for open
source Conan packages. We also :ref:`learned how to create our own packages
<tutorial_creating_packages>` and store them in the Conan local cache for reusing later.
In this section we cover how you can use the Conan repositories to upload your
recipes and binaries and store them for later use on another machine, project, or for
sharing purposes.

First we will cover how you can setup a Conan repository locally (you can skip this part
if you already have a Conan remote configured). Then we will explain how to upload
packages to your own repositories and how to operate when you have multiple Conan remotes
configured. Finally, we will briefly cover how you can contribute to the Conan Center
central repository. 

Finally, we will explain the `local_recipes_index`, a special type of remote that allows
the use of a source folder with recipes as a Conan remote repository.

.. toctree::
   :maxdepth: 2
   :caption: Table of contents
   
   conan_repositories/setting_up_conan_remotes.rst
   conan_repositories/uploading_packages.rst
   conan_repositories/conan_center.rst
   conan_repositories/setup_local_recipes_index.rst
