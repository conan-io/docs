
|gitlab_logo| Gitlab 
=============================

You can use `Gitlab CI`_ cloud or local service to automatically build and test your project in Linux/OSX/Windows environments.
It is free for OSS projects, and offers an easy integration with Gitlab, so builds can be automatically
fired in Gitlab CI after a ``git push`` to Gitlab.

You can use Gitlab CI both for:

- Building and testing your project, which manages dependencies with Conan, and probably a conanfile.txt file
- Building and testing conan binary packages for a given conan package recipe (with a conanfile.py)


Building and testing your project
------------------------------------

We are going to use the :ref:`Google Test example<google_test_example>` now, with **Gitlab CI** support to run the tests.


Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


Create a ``.gitlab-ci.yml`` file and paste this code in it: 


.. code-block:: text

    image: lasote/conangcc63

    build:
      before_script:
        # Upgrade Conan version
        - sudo pip install --upgrade conan
        # Automatic detection of your arch, compiler, etc.
        - conan user

      script:
        # Download dependencies, build, test and create package
        - conan test_package


Gitlab CI will install the **conan** tool and will execute the **conan install** command.
Then, the **script** section creates the build folder, compiles the project with **cmake** and runs the **tests**.


Creating and testing conan package binaries
---------------------------------------------------------
You can use Gitlab CI to automate the building of binary packages, which will be created in the
cloud after pushing to Gitlab. You can probably setup your own way, but it is recommended
to use :ref:`conan tools for package creators <package_tools>`


.. |gitlab_logo| image:: ../images/gitlab_logo.png
.. _`Gitlab CI`: https://gitlab.com/
