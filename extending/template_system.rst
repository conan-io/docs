
Template system
===============

The user can provide their own templates to override some of the files that Conan generates
in runtime. This can help to provide custom visualization for some outputs that satisfies
specific use-cases or more detailed inputs for companies that want some standarization
when creating new recipes for packages.

User provided templates to override Conan default ones, must be stored in the Conan cache
under a `templates` directory (`<conan_cache>/templates`). Use :ref:`conan_config` command
to distribute them among your developer team.

.. toctree::
   :maxdepth: 2

   template_system/search_table
   template_system/info_graph
   template_system/command_new
