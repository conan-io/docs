.. xmake:

|xmake_logo| XMake
==================

.. warning::

    This is a **deprecated** feature. Please refer to the :ref:`Migration Guidelines<conan2_migration_guide>`
    to find the feature that replaced this one.


Install third-party packages:
-----------------------------

After version 2.2.5, xmake supports installing for dependency libraries of conan package manager.

.. code-block:: lua
   :caption: xmake.lua
    
    -- xmake.lua
    
    add_requires("conan::zlib/1.2.11@conan/stable", {alias = "zlib", debug = true})
    add_requires("conan::openssl/1.1.1g", {alias = "openssl",
        configs = {options = "OpenSSL:shared=True"}})
    
    target("test")
        set_kind("binary")
        add_files("src/*.c") 
        add_packages("openssl", "zlib")


After executing xmake to compile:

.. code-block:: bash

    $ xmake
    checking for the architecture ... x86_64
    checking for the Xcode directory ... /Applications/Xcode.app
    checking for the SDK version of Xcode ... 10.14
    note: try installing these packages (pass -y to skip confirm)?
      -> conan::zlib/1.2.11@conan/stable  (debug)
      -> conan::openssl/1.1.1g  
    please input: y (y/n)

      => installing conan::zlib/1.2.11@conan/stable .. ok
      => installing conan::openssl/1.1.1g .. ok

    [  0%]: ccache compiling.release src/main.c
    [100%]: linking.release test


Find a conan package
--------------------

XMake v2.2.6 and later versions also support finding the specified package in the Conan cache:

.. code-block:: lua
   :caption: xmake.lua
    
    ...
    find_packages("conan::openssl/1.1.1g")

Test command for finding package
--------------------------------

We can also add a third-party package manager prefix to test:

.. code-block:: bash
    
    xmake l find_packages conan::openssl/1.1.1g

.. |xmake_logo| image:: ../../images/conan-xmake_logo.png

**Note:** It should be noted that if the find_package command is executed in the project directory with xmake.lua, there will be a cache.
If the search fails, the next lookup will also use the cached result. If you want to force a retest every time,
Please switch to the non-project directory to execute the above command.
