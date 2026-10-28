.. _reference_conanfile_methods_source:


source()
========

The ``source()`` method can be used to retrieve the necessary source code to build a package from source, and to apply patches to such source code if necessary. It will be called when a package is being built from source, like with ``conan create`` or ``conan install  --build=pkg*``, but it will not be called if a package pre-compiled binary is being used. That means that the source code will not be downloaded if a pre-compiled binary exists.

The ``source()`` method can implement different strategies for retrieving the source code:

- Fetching the source code for a third party library:

  - Using a ``Git(self).clone()`` to clone a Git repository
  - Executing a ``download()`` + ``unzip()`` or a combined ``get()`` (internally does download + unzip) to download a tarball, tgz, or zip archive.
- Fetching the source code for itself, from its repository, whose coordinates have been captured in the ``conandata.yml`` file in the ``export()`` method. This is the strategy that would be used to manage the source code for packages in which the ``conanfile.py`` lives in the package itself, but that for some reason we don't want to put the source code in the recipe (like not distributing our source code, but being able to distribute our package binaries).


The ``source()`` method executes in the ``self.source_folder``, the current working directory will be equal to that folder (which value is derived from ``layout()`` method).

A ``source()`` implementation might use the convenient ``get()`` helper, or use its own mechanisms or other Conan helpers for the task, something like:

..  code-block:: python

    import os
    import shutil
    
    from conan import ConanFile
    from conan.tools.files import download, unzip, check_sha1


    class PocoConan(ConanFile):
        name = "poco"
        version = "1.6.0"

        def source(self):
            zip_name = f"poco-{self.version}-release.zip"
            # Immutable source .zip
            download(self, f"https://github.com/pocoproject/poco/archive/poco-{self.version}-release.zip", zip_name)
            # Recommended practice, always check hashes of downloaded files
            check_sha1(self, zip_name, "8d87812ce591ced8ce3a022beec1df1c8b2fac87")
            unzip(self, zip_name)
            shutil.move(f"poco-poco-{self.version}-release", "poco")
            os.unlink(zip_name)



Applying patches to downloaded sources can be done (and should be done) in the ``source()`` method if those patches
apply to all possible configurations. As explained below, it is not possible to introduce conditionals in the
``source()`` method. If the patches are in file form, those patches must be exported together with the recipe, so they can be used whenever a build from source is fired.

It is possible to apply patches with:

- Your own or ``git`` patches utilities
- The Conan built-in ``patch()`` utility to explicitly apply patches one by one
- Apply the ``apply_conandata_patches()`` Conan utility to automatically apply all patches defined in ``conandata.yml`` file following some conventions.

.. _reference_conanfile_methods_source_caching:

Source caching
--------------

Once the ``source()`` method has been called, its result will be cached and reused for any build from source, for any configuration. That means that the retrieval of sources from the ``source()`` method should be completely independent of the configuration. It is not possible to implement conditionals on the ``settings``, and in general, any attempt to apply any conditional logic to the ``source()`` method is wrong.

.. code-block:: python

    def source(self):
        if self.settings.compiler == "gcc":  # ERROR, will raise
            # download some source

Trying to bypass the Conan exception by using some other mechanism like:

.. code-block:: python

    def source(self):
        # Might work, but NOT recommended, try to avoid as much as possible
        if platform.system() == "Windows":
            # download something
        else:
            # download something different

Might apparently work if not doing any cross-build, and not recollecting sources in a different OS, but could be problematic otherwise.
  
To be completely safe, if different source code is necessary for different configurations, the recommended approach would be to retrieve that code conditionally in the ``build()`` method.


Forced retrieval of sources
---------------------------

When working with a recipe in a user folder, it is easy to call the ``source()`` method and force the retrieval of the source code, that will be done in the same user folder, according to the ``layout()`` definition:

.. code-block:: bash

    $ conan source .


Calling the ``source()`` method and forcing the retrieval of source code in the cache, for all or some dependencies, even if they are not being built from sources, is possible with the ``tools.build:download_source=True`` configuration. For example:

.. code-block:: bash

    $ conan graph info . -c tools.build:download_source=True

Will compute the dependency graph, then call the ``source()`` method for all "host" packages in the graph (as the configuration by default is a "host" configuration, if you want also the sources for the "build" context ``tool_requires``, you could use ``-c:b tools.build:download_source=True``). It is possible to collect all the source folders from the json formatted output, or to automate recollection of all sources, a ``deployer`` could be used.

Likewise, it is possible to retrieve the sources for packages in other ``create`` and ``install`` commands, just by passing the configuration. Finally, as also configuration can be defined per-package, using ``-c mypkg*:tools.build:download_source=True`` would only retrieve the sources of packages matching the ``mypkg*`` pattern.

Note that ``tools.build:download_source=True`` will not have any effect on packages in **editable** mode. Downloading sources in that case could easily overwrite and destroy local developer changes over that code. The ``conan source`` command must be used on packages in editable mode to download the sources.


.. note::

    **Best practices**

    - The ``source()`` method should be the same for all configurations, it cannot be conditional to any configuration.
    - The ``source()`` method should retrieve immutable sources. Using some branch name, HEAD, or a tarball whose URL is not immutable and is being overwritten is a bad practice and will lead to broken packages. Using a Git commit, a frozen Git release tag, or a fixed and versioned release tarballs is the expected input. 
    - Applying patches should be done by default in the ``source()`` method, except if the patches are exclusive for one configuration, in that case they could be applied in ``build()`` method.
    - The ``source()`` method should not access nor manipulate files in other folders different to the ``self.source_folder``. All the "exported" files are copied to the ``self.source_folder`` before calling it.


.. seealso::
    
    See :ref:`the tutorial about managing recipe sources<creating_packages_handle_sources_in_packages>` for more information.
