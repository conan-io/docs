Local package development flow
==============================

In the previous examples, we used ``$ conan create`` command to create a package of our
library. Every time we run it, conan will perform some costly operations:

1. Copy the sources to a new and clean build folder.
2. Build the entire library from scratch.
3. Package the library once it is built.
4. Build the ``test_package`` example and test if it works.

But sometimes, specially with big libraries, while we are developing the recipe, **we cannot afford**
to perform every time these operations.


The following section is the local development flow description extracted from the Bincrafters community at
`their Blog <https://bincrafters.github.io>`_


----

The local workflow encourages users to do trial-and-error in a local sub-directory relative to their recipe,
much like how developers typically test building their projects with other build tools.
The strategy is to test the ``conanfile.py`` methods individually during this phase.

Below are the commands listed in the order we use them now:


conan source
____________


You will generally want to start off with the conan source command, for example:


.. code-block:: bash

    $ conan source . --source-folder=tmp/source


The strategy here is that you’re testing your source method in isolation, and downloading the files
to a temporary sub-folder relative to conanfile.py.
This just makes it easier to get to the sources and validate them.
Once you’ve got your source method right, and it contains the files you expect,
you can move on to testing the various attributes and methods relating to the downloading of dependencies.


conan install
_____________


Conan has multiple methods and attributes which relate to dependencies
(all the ones with the word require in the name). The command conan install activates all them:


.. code-block:: bash

    $ conan install  . --install-folder=tmp/build [--profile XXXX]


This also generates ``conaninfo.txt`` and ``conanbuildinfo.xyz`` (extension depends on generator you’ve used)
in the temp folder (``install-folder``), which will be needed for the next step.
Once you’ve got this command working with no errors, you can move on to testing the build() method.


conan build
___________


The build method takes a path to a folder that has sources (basically an “input” folder), and a path
to a folder where it will perform the build (basically an “output” folder).

.. code-block:: bash

    $ conan build . --source-folder=tmp/source --build-folder=tmp/build

This is pretty strightforward, but it does add a very helpful new shortcut for people who are packaging
their own library. Now, developers can make changes in their normal source directory and just pass that
path as the ``--source-folder``.


conan package
_____________


Just as it sounds, this CLI command now simply runs the package() method of a recipe.
Like the conan build command, it basically takes “input” and “output” folders.
In this case as **input**: ``--source-folder --build-folder`` and **output**: ``--package-folder``:

.. code-block:: bash

    $ conan package . --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package


conan create
_____________


Now we know we have all the steps of a recipe working.
Thus, now is an appropriate time to try to run the recipe all the way through, and put it in the local cache.

.. code-block:: bash

    $ conan create . user/channel


conan test
__________

A final followup step in many workflows after the package is creating successfully is to work on the test_package.
There is often a need to repeatedly re-run the test, and so the conan test command exists. An example is shown below:


.. code-block:: bash

    $ conan test test_package package/version@user/channel
