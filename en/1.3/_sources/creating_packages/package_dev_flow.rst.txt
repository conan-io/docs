Package development flow
========================

In the previous examples, we used :command:`conan create` command to create a package of our library. Every time we run it, conan will perform
some costly operations:

1. Copy the sources to a new and clean build folder.
2. Build the entire library from scratch.
3. Package the library once it is built.
4. Build the ``test_package`` example and test if it works.

But sometimes, specially with big libraries, while we are developing the recipe, **we cannot afford** to perform every time these
operations.

The following section is the local development flow description based on the
`Bincrafters community blog <https://bincrafters.github.io>`_.

----

The local workflow encourages users to do trial-and-error in a local sub-directory relative to their recipe, much like how developers
typically test building their projects with other build tools. The strategy is to test the *conanfile.py* methods individually during this
phase.

We will use the following `conan flow example <https://github.com/memsharded/example_conan_flow>`_ to follow the steps in the order below:

conan source
^^^^^^^^^^^^

You will generally want to start off with the :command:`conan source` command. The strategy here is that you’re testing your source method in
isolation, and downloading the files to a temporary sub-folder relative to the *conanfile.py*. This just makes it easier to get to the
sources and validate them.

This method outputs the source files into the source-folder.

+---------------+-------------------+
| Input folders | Output folders    |
+===============+===================+
| --            | ``source-folder`` |
+---------------+-------------------+

.. code-block:: bash

    $ cd example_conan_flow
    $ conan source . --source-folder=tmp/source

    PROJECT: Configuring sources in C:\Users\conan\example_conan_flow\tmp\source
    Cloning into 'hello'...
    ...

Once you’ve got your source method right and it contains the files you expect, you can move on to testing the various attributes and methods
relating to the downloading of dependencies.

conan install
^^^^^^^^^^^^^

Conan has multiple methods and attributes which relate to dependencies (all the ones with the word "require" in the name). The command
:command:`conan install` activates all them.

+---------------+--------------------+
| Input folders | Output folders     |
+===============+====================+
| --            | ``install-folder`` |
+---------------+--------------------+

.. code-block:: bash

    $ conan install . --install-folder=tmp/install [--profile XXXX]

    PROJECT: Installing C:\Users\conan\example_conan_flow\conanfile.py
    Requirements
    Packages
    ...

This also generates *conaninfo.txt* and *conanbuildinfo.xyz* (extension depends on generator you’ve used) in the temp folder
(``install-folder``), which will be needed for the next step. Once you've got this command working with no errors, you can move on to
testing the ``build()`` method.

conan build
^^^^^^^^^^^

The build method takes a path to a folder that has sources and also to the install folder to get the information of the settings and
dependencies. It uses a path to a folder where it will perform the build.

+--------------------+------------------+
| Input folders      | Output folders   |
+====================+==================+
| ``source-folder``  | ``build-folder`` |
|                    |                  |
| ``install-folder`` |                  |
+--------------------+------------------+

.. code-block:: bash

    $ conan build . --source-folder=tmp/source --install-folder=tmp/install --build-folder=tmp/build

    Project: Running build()
    ...
    Build succeeded.
        0 Warning(s)
        0 Error(s)

    Time Elapsed 00:00:03.34

This is pretty strightforward, but it does add a very helpful new shortcut for people who are packaging their own library. Now, developers
can make changes in their normal source directory and just pass that path as the ``--source-folder``.

conan package
^^^^^^^^^^^^^

Just as it sounds, this command now simply runs the ``package()`` method of a recipe. It needs all the information of the other folders in
order to collect the needed information for the package: header files from source folder, settings and depency information from the install
folder and built artifacts from the build folder.

+--------------------+--------------------+
| Input folders      | Output folders     |
+====================+====================+
| ``source-folder``  | ``package-folder`` |
|                    |                    |
| ``install-folder`` |                    |
|                    |                    |
| ``build-folder``   |                    |
+--------------------+--------------------+

.. code-block:: bash

    $ conan package . --source-folder=tmp/source --install-folder=tmp/install --build-folder=tmp/build --package-folder=tmp/package

    PROJECT: Generating the package
    PROJECT: Package folder C:\Users\conan\example_conan_flow\tmp\package
    PROJECT: Calling package()
    PROJECT package(): Copied 1 '.h' files: hello.h
    PROJECT package(): Copied 2 '.lib' files: greet.lib, hello.lib
    PROJECT: Package 'package' created

conan export-pkg
^^^^^^^^^^^^^^^^

When you have checked that the packaged is done correctly, you can generate the package in the local cache. Note that the package is
generated again to make sure this step is always reproducible.

This parameters takes the same parameters as ``package()``.

+--------------------+--------------------+
| Input folders      | Output folders     |
+====================+====================+
| ``source-folder``  | --                 |
|                    |                    |
| ``install-folder`` |                    |
|                    |                    |
| ``build-folder``   |                    |
|                    |                    |
| ``package-folder`` |                    |
+--------------------+--------------------+

There are 2 modes of operation:

- Using ``source-folder`` and ``build-folder``will use the ``package()`` method to extract the artifacts from those 
  folders and create the package, directly in the conan local cache. Strictly speaking, it doesn't require executing
  a ``$ conan package`` before, as it packages directly from those source and build folder, though ``$ conan package``
  is still recommended in the dev-flow to debug the ``package()`` method.
- Using the ``package-folder`` argument (incompatible with the above 2), will not use the ``package()`` method,
  it will do an exact copy of the provided folder. It assumes the package has already been created by a previous
  ``$ conan package`` command or with a ``$ conan build`` command with a ``build()`` method running a ``cmake.install()``.

..  code-block:: bash

    $ conan export-pkg . user/testing --source-folder=tmp/source --install-folder=tmp/install --build-folder=tmp/build

    Packaging to 6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7
    Hello/0.1@user/channel: Generating the package
    Hello/0.1@user/channel: Package folder C:\Users\conan\.conan\data\Hello\0.1\user\channel\package\6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7
    Hello/0.1@user/channel: Calling package()
    Hello/0.1@user/channel package(): Copied 2 '.lib' files: greet.lib, hello.lib
    Hello/0.1@user/channel package(): Copied 2 '.lib' files: greet.lib, hello.lib
    Hello/0.1@user/channel: Package '6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7' created

conan test
^^^^^^^^^^

The finally step to test the package for consumer is the test command. This step is quite straight-forward:

.. code-block:: bash

    $ conan test test_package Hello/0.1@user/channel

    Hello/0.1@user/channel (test package): Installing C:\Users\conan\repos\example_conan_flow\test_package\conanfile.py
    Requirements
        Hello/0.1@user/channel from local
    Packages
        Hello/0.1@user/channel:6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7

    Hello/0.1@user/channel: Already installed!
    Hello/0.1@user/channel (test package): Generator cmake created conanbuildinfo.cmake
    Hello/0.1@user/channel (test package): Generator txt created conanbuildinfo.txt
    Hello/0.1@user/channel (test package): Generated conaninfo.txt
    Hello/0.1@user/channel (test package): Running build()
    ...

There is often a need to repeatedly re-run the test to check the package is well generated for consumers.

As a summary, you could use the default folders and the flow would be as simple as:

.. code-block:: bash

    $ git clone git@github.com:memsharded/example_conan_flow.git
    $ cd example_conan_flow
    $ conan source .
    $ conan install .
    $ conan build .
    $ conan package .
    ...
    PROJECT package(): Copied 1 '.h' files: hello.h
    PROJECT package(): Copied 2 '.lib' files: greet.lib, hello.lib
    PROJECT: Package 'package' created

conan create
^^^^^^^^^^^^

Now we know we have all the steps of a recipe working. Thus, now is an appropriate time to try to run the recipe all the way through, and
put it completely in the local cache.

The usual command for this is :command:`conan create` and it basically performs the previous commands with :command:`conan test` for the `test_package`
folder:

.. code-block:: bash

    $ conan create . user/channel

Even with this command, the package creator can iterate over the local cache if something does not work. This could be done with
``--keep-source`` and ``--keep-build`` flags.

If you see in the traces that the ``source()`` method has been properly executed but the package creation finally failed, you can skip the
``source()`` method the next time you issue :command:`conan create` using :command:`--keep-source`:

.. code-block:: bash

    $ conan create . user/channel --keep-source

    Hello/0.1@user/channel: A new conanfile.py version was exported
    Hello/0.1@user/channel: Folder: C:\Users\conan\.conan\data\Hello\0.1\user\channel\export
    Hello/0.1@user/channel (test package): Installing C:\Users\conan\repos\example_conan_flow\test_package\conanfile.py
    Requirements
        Hello/0.1@user/channel from local
    Packages
        Hello/0.1@user/channel:6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7

    Hello/0.1@user/channel: WARN: Forced build from source
    Hello/0.1@user/channel: Building your package in C:\Users\conan\.conan\data\Hello\0.1\user\channel\build\6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7
    Hello/0.1@user/channel: Configuring sources in C:\Users\conan\.conan\data\Hello\0.1\user\channel\source
    Cloning into 'hello'...
    remote: Counting objects: 17, done.
    remote: Total 17 (delta 0), reused 0 (delta 0), pack-reused 17
    Unpacking objects: 100% (17/17), done.
    Switched to a new branch 'static_shared'
    Branch 'static_shared' set up to track remote branch 'static_shared' from 'origin'.
    Hello/0.1@user/channel: Copying sources to build folder
    Hello/0.1@user/channel: Generator cmake created conanbuildinfo.cmake
    Hello/0.1@user/channel: Calling build()
    ...

If you see that library builds correctly too, you can do the same to skip also the ``build()`` step with the ``--keep-build`` flag:

.. code-block:: bash

    $ conan create --keep-build
