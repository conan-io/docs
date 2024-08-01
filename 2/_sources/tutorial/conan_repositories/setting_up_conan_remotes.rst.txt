.. _setting_up_conan_remotes:

Setting up a Conan remote
=========================

There are several options to set-up a Conan repository:

**For private development:**

- :ref:`Artifactory Community Edition for C/C++ <artifactory_ce_cpp>`: Artifactory
  Community Edition (CE) for C/C++ is a completely free Artifactory server that implements 
  both Conan and generic repositories. It is the recommended server for companies and
  teams wanting to host their own private repository. It has a web UI, advanced
  authentication and permissions, very good performance and scalability, a REST API, and
  can host generic artifacts (tarballs, zips, etc). Check :ref:`artifactory_ce_cpp` for
  more information.

- :ref:`Conan server <conan_server>`: Simple, free and open source, MIT
  licensed server that is part of the `conan-io organization
  <https://github.com/conan-io>`_ project. Check
  :ref:`conan_server` for more information.


**Enterprise solutions:**

- **Artifactory Pro**: Artifactory is the binary repository manager for all major
  packaging formats. It is the recommended remote type for enterprise and professional
  package management. Check the `Artifactory Documentation
  <https://www.jfrog.com/confluence/display/JFROG/JFrog+Artifactory>`_ for more
  information. For a comparison between Artifactory editions, check the `Artifactory
  Comparison Matrix
  <https://www.jfrog.com/confluence/display/JFROG/Artifactory+Comparison+Matrix>`_.

.. toctree::
   :maxdepth: 2
   :hidden:
   
   setting_up_conan_remotes/artifactory/artifactory_ce_cpp.rst
   setting_up_conan_remotes/conan_server.rst
