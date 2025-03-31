.. _integration_vcs:


Version Control System
======================

Conan uses plain text files for the recipes and configuration files and they can be managed nicely
with any version control system. Also, with the :ref:`scm<scm_feature>` feature, your recipe can
capture automatically the ``commit/revision`` of the source code of your library so the recipe will
clone the correct sources automatically.

.. toctree::
   :maxdepth: 2

   vcs/git
   vcs/svn
