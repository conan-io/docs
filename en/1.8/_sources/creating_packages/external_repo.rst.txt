.. _external_repo:

Recipe and Sources in a Different Repo
======================================


In the previous section, we fetched the sources of our library from an external repository.
It is a typical workflow for packaging third party libraries.

There are two different ways to fetch the sources from an external repository:

1. Using the ``source()`` method as we displayed in the previous section:

.. code-block:: python

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
        ...

        def source(self):
            self.run("git clone https://github.com/memsharded/hello.git")
            self.run("cd hello && git checkout static_shared")
            ...

You can also use the :ref:`tools.Git <tools_git>` class:

.. code-block:: python

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
        ...

        def source(self):
            git = tools.Git(folder="hello")
            git.clone("https://github.com/memsharded/hello.git", "static_shared")
            ...


2. Using the :ref:`scm attribute <scm_attribute>` of the ConanFile [EXPERIMENTAL]:


.. code-block:: python

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
         scm = {
            "type": "git",
            "subfolder": "hello",
            "url": "https://github.com/memsharded/hello.git",
            "revision": "static_shared"
         }
        ...


Conan will clone the ``scm url`` and will checkout the ``scm revision``. Head to
:ref:`creating package documentation <scm_feature>`
to know more details about SCM feature.


The ``source()`` method will be called after the checkout process, so you can still use it to patch something or
retrieve more sources, but it is not necessary in most cases.
