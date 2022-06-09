.. _creating_packages_handle_sources_in_packages:

Handle sources in packages
==========================

In the :ref:`previous tutorial
section<creating_packages_create_your_first_conan_package>`, we created a Conan package
for a "Hello World" C++ library. We used the ``exports_sources`` attribute of the
Conanfile to declare the location of the sources for the library. Using this method is the
simplest way to do this when the sources are in the same folder as the Conanfile. However,
sometimes the sources are stored in a repository or a file in a remote server and not in
the same location as the Conanfile. In this section we will modify the recipe we created
previously to retrieve the same sources from other repository or a remote server.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/handle_sources

The structure of the project is the same as the one of the previous example: