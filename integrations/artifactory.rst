.. _integrations_artifactory:

Artifactory
============

`JFrog's Artifactory <https://jfrog.com/artifactory/>`_ is used to power `ConanCenter`_ and it is the single solution
for housing and managing all the binaries, packages, and files for use throughout your software supply chain. Artifactory
is the binary repository manager for all major packaging formats. It is the recommended for enterprise and professional
teams a like who need a single package management solution.

This pairs nicely with Conan whose strength comes from binary management for C/C++. These artifacts need to be stored
and shared with all the developers on a project. For `artifact management <https://jfrog.com/artifact-management/>`_
some possible solutions include a shared drive or source control management tool, these other options have limitations
when dealing with binary packages that evolved through the software development life cycle.

.. _using_artifactory:

Using Artifactory
-----------------

In Artifactory, you can create and manage as many Conan repositories as you like using :ref:`Artifactory CE
<integrations_artifactory_ce>` hosted locally in your network or with :ref:`Artifactory Pro or Enterprise
<integrations_artifactory_pro_e>`.

.. important::

    Conan 2.0 support in Artifactory starting around v6.9 with recipe revisions however it is **strongly recommended**
    to have a version above 7.41 which was in use by ConanCenter during the final development and is known to work in
    the majority of use cases.

    Complete support for Conan 2.0 was introduced with 7.52. Please refer to the
    `Artifactory Changelog <https://www.jfrog.com/confluence/display/JFROG/Artifactory+Release+Notes>`_ to ensure no
    bugfixes appear in more recent versions.

By creating different repositories you can control the way binaries enter, advance, and are leveraged throughout the
software supply chain. Using a promote (not rebuild) workflow for binaries as they advance through the SSC to ensure
integrity. This enables scaling to meet the needs of the largest organizations and systems that simply cannot fail.
See the `Artifactory's Onboarding Best Practices <https://www.jfrog.com/confluence/display/JFROG/Onboarding+Best+Practices%3A+JFrog+Artifactory>`_
for more details.

.. _integrations_artifactory_ce:

Artifactory Community Edition for C/C++
---------------------------------------

Artifactory Community Edition (CE) for C/C++ is the recommended server for development and
hosting packages for private development. It is completely free, and it features a WebUI,
great performance, a REST API, and generic repositories to host any kind of source or binary
artifact (tarballs, zips, etc).

This is a very brief introduction to Artifactory. For more documentation, visit `Artifactory
documentation <https://www.jfrog.com/confluence/>`_.

Running Artifactory CE
++++++++++++++++++++++

Please visit the :ref:`Artifactory CE Tutorial<tutorial_artifactory_ce_cpp>` for a step by
step guide

.. _integrations_artifactory_pro_e:

Artifactory Pro and Enterprise
------------------------------

For a comparison between Artifactory editions, check the `Artifactory Comparison Matrix
<https://www.jfrog.com/confluence/display/JFROG/Artifactory+Comparison+Matrix>`_.


.. _`ConanCenter`: https://conan.io/center
