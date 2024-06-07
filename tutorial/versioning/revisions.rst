Revisions
=========

This sections introduces how doing modifications to a given recipe or source code without explicitly
creating new versions, will still internally track those changes with a mechanism called revisions.


Creating different revisions
----------------------------

Let's start with a basic "hello" package:

.. code-block:: bash

    $ mkdir hello && cd hello
    $ conan remove hello* -c # clean possible existing ones
    $ conan new cmake_lib -d name=hello -d version=1.0
    $ conan create .
    hello/1.0: Hello World Release!
    ...

We can now list the existing recipe revisions in the cache:

.. code-block:: bash

    $ conan list "hello/1.0#*"
    Local Cache
      hello
        hello/1.0
          revisions
            2475ece651f666f42c155623228c75d2 (2023-01-31 23:08:08 UTC)

If we now edit the ``src/hello.cpp`` file, to change the output message from
"Hello" to "Bye"

.. code-block:: cpp
    :caption: hello/src/hello.cpp

    void hello(){
    
        #ifdef NDEBUG
        std::cout << "hello/1.0: Bye World Release!\n";
        ...

So if we create the package again, without changing the version ``hello/1.0``, we will 
get a new output:

.. code-block:: bash

    $ conan create .
    hello/1.0: Bye World Release!
    ...

But even if the version is the same, internally a new revision ``2b547b7f20f5541c16d0b5cbcf207502`` 
has been created.

.. code-block:: bash
    
    $ conan list "hello/1.0#*"
    Local Cache
      hello
        hello/1.0
          revisions
            2475ece651f666f42c155623228c75d2 (2023-01-31 23:08:08 UTC)
            2b547b7f20f5541c16d0b5cbcf207502 (2023-01-31 23:08:25 UTC)

This recipe **revision**  is the hash of the contents of the recipe, including the ``conanfile.py``,
and the exported sources (``src/main.cpp``, ``CMakeLists.txt``, etc., that is, all files exported
in the recipe).

We can now edit the ``conanfile.py``, to define the ``licence`` value:

.. code-block:: python
    :caption: hello/conanfile.py

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        # Optional metadata
        license = "MIT"
        ...


So if we create the package again, the output will be the same, but we will also get a new
revision, as the ``conanfile.py`` changed:

.. code-block:: bash

    $ conan create .
    hello/1.0: Bye World Release!
    ...
    $ conan list "hello/1.0#*"
    Local Cache
      hello
        hello/1.0
          revisions
            2475ece651f666f42c155623228c75d2 (2023-01-31 23:08:08 UTC)
            2b547b7f20f5541c16d0b5cbcf207502 (2023-01-31 23:08:25 UTC)
            1d674b4349d2b1ea06aa6419f5f99dd9 (2023-01-31 23:08:34 UTC)


.. important::

    The recipe **revision** is the hash of the contents. It can be changed to be the
    Git commit hash with ``revision_mode = "scm"``. But in any case it is critical
    that every revision represents an immutable source, including the recipe and the source code:

    - If the sources are managed with ``exports_sources``, then they will be automatically
      be part of the hash
    - If the sources are retrieved from a external location, like a downloaded tarball or a git
      clone, that should guarantee uniqueness, by forcing the checkout of a unique
      immutable tag, or a commit. Moving targets like branch names or HEAD would be
      broken, as revisions are considered immutable.
    
    Any change in source code or in recipe should always imply a new revision.

.. warning::

    **Line Endings Issue**

    Git, by default, will checkout files on Windows systems using ``CRLF`` line endings.
    This results in different files compared to Linux systems where files will use ``LF``
    line endings. Since the files are different, the Conan recipe revision computed on
    Windows will differ from the revisions on other platforms like Linux. Please, check
    more about this issue and how to solve it in the :ref:`FAQ dedicated section<faq_different_revisions>`. 



Using revisions
---------------

The recipe revisions are resolved by default to the latest revision for every
given version. In the case above, we could have a ``chat/1.0`` package that 
consumes the above ``hello/1.0`` package:

.. code-block:: bash

    $ cd ..
    $ mkdir chat && cd chat
    $ conan new cmake_lib -d name=chat -d version=1.0 -d requires=hello/1.0
    $ conan create .
    ...
    Requirements
    chat/1.0#17b45a168519b8e0ed178d822b7ad8c8 - Cache
    hello/1.0#1d674b4349d2b1ea06aa6419f5f99dd9 - Cache
    ...
    hello/1.0: Bye World Release!
    chat/1.0: Hello World Release!

We can see that by default, it is resolving to the latest revision ``1d674b4349d2b1ea06aa6419f5f99dd9``,
so we also see the ``hello/1.0: Bye World`` modified message.

It is possible to explicitly depend on a given revision in the recipes, so it is possible
to modify the ``chat/1.0`` recipe to define it requires the first created revision:


.. code-block:: python
    :caption: chat/conanfile.py

    def requirements(self):
        self.requires("hello/1.0#2475ece651f666f42c155623228c75d2")


So creating ``chat`` will now force the first revision:

.. code-block:: bash

    $ conan create .
    ...
    Requirements
    chat/1.0#12f87e1b8a881da6b19cc7f229e16c76 - Cache
    hello/1.0#2475ece651f666f42c155623228c75d2 - Cache
    ...
    hello/1.0: Hello World Release!
    chat/1.0: Hello World Release!


Uploading revisions
-------------------

The upload command will upload only the latest revision by default:

.. code-block:: bash

    # upload latest revision only, all package binaries
    $ conan upload hello/1.0 -c -r=myremote

If for some reason we want to upload all existing revisions, it is possible with:

.. code-block:: bash

    # upload all revisions, all binaries for each revision
    $ conan upload hello/1.0#* -c -r=myremote

In the server side, the latest uploaded revision becomes the latest one, and the
one that will be resolved by default. For this reason, the above command uploads
the different revisions in order (from older revision to latest revision), so the
relative order of revisions is respected in the server side.

Note that if another machine decides to upload a revision that was created some time
ago, it will still become the latest in the server side, because it is created in the 
server side with that time.


Package revisions
-----------------
Package binaries when created also compute the hash of their contents, forming the
**package revision**.  But they are very different in nature to **recipe revisions**.
Recipe revisions are naturally expected, every change in source code or in the recipe
would cause a new recipe revision. But package binaries shouldn't have more than one 
**package revision**, because binaries variability would be already encoded in a unique
``package_id``. Put in other words, if the recipe revision is the same (exact same 
input recipe and source code) and the ``package_id`` is the same (exact same configuration
profile, settings, etc.), then that binary should be built only once.

As C and C++ build are not deterministic, it is possible that subsequents builds of the
same package, without modifying anything will be creating new package revisions:

.. code-block:: bash

    # Build again 2 times the latest
    $ conan create .
    $ conan create .

In some OSs like Windows, this build will not be reproducible, and the resulting 
artifacts will have different checksums, resulting in new package revisions:


.. code-block:: bash

    $ conan list "hello/1.0:*#*"
    Local Cache
      hello
        hello/1.0
          revisions
            1d674b4349d2b1ea06aa6419f5f99dd9 (2023-02-01 00:03:29 UTC)
              packages
                2401fa1d188d289bb25c37cfa3317e13e377a351
                  revisions
                    8b8c3deef5ef47a8009d4afaebfe952e (2023-01-31 23:08:40 UTC)
                    8e8d380347e6d067240c4c00132d42b1 (2023-02-01 00:03:12 UTC)
                    c347faaedc1e7e3282d3bfed31700019 (2023-02-01 00:03:35 UTC)
                  info
                    settings
                    arch: x86_64
                    build_type: Release
                    ...

By default, the package revision will also be resolved to the latest one. However, 
it is not possible to pin a package revision explicitly in recipes, recipes can 
only require down to the recipe revision as we defined above.


.. warning::

    **Best practices**

    Having more than 1 package revision for any given recipe revision + ``package_id``
    is a smell or a potential bad practice. It means that something was rebuilt when 
    it was not necessary, wasting computing and storage resources. There are ways to
    avoid doing it, like ``conan create . --build=missing:hello*`` will only build that
    package binary if it doesn't exist already (or running ``conan graph info`` can 
    also return information of what needs to be built.)
