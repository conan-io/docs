.. _circleci_integration:


.. _circleci:

|circleci_logo| Circle CI
=============================

You can use `Circle CI`_ cloud to automatically build and test your project in Linux/macOS environments.
It is free for OSS projects, and offers an easy integration with Github, so builds can be automatically
fired in CircleCI after a ``git push`` to Github.

You can use CircleCI both for:

- Building and testing your project, which manages dependencies with Conan, and probably a conanfile.txt file
- Building and testing conan binary packages for a given conan package recipe (with a conanfile.py)


Building and testing your project
------------------------------------

We are going to use an example with GTest package, with **CircleCI** support to run the tests.


Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


Create a ``.circleci/config.yml`` file and paste this code in it:


.. code-block:: text

  version: 2
  gcc-6:
    docker:
      - image: conanio/gcc6
    steps:
      - checkout
      - run:
          name: Build Conan package
          command: |
            sudo pip install --upgrade conan
            conan user
            conan create . user/channel
  workflows:
    version: 2
    build_and_test:
      jobs:
      - gcc-6


CircleCI will install the **conan** tool and will execute the **conan create** command.
Then, the **script** section creates the build folder, compiles the project with **cmake** and runs the **tests**.


Creating, testing and uploading conan package binaries
------------------------------------------------------
You can use CircleCI to automate the building of binary packages, which will be created in the
cloud after pushing to Github. You can probably setup your own way, but conan has some utilities to help in the process.

The command ``conan new`` has arguments to create a default working ``.circleci/config.yml`` file.
Other setups might be possible, but for this example we are assuming that you are using github and also uploading your final packages to Bintray.
You could follow these steps:

#. First, create an empty Github repository, let's call it "hello", for creating a "hello world" package. Github allows to create it with a Readme, license and .gitignore.
#. Get the credentials User and API Key (remember, Bintray uses the API key as "password", not your main Bintray account password)
#. Create a conan repository in Bintray under your user or organization, and get its URL ("Set me up"). We will call it ``UPLOAD_URL``
#. Under your project page, *Settings -> Pipelines -> Add a variable*, add the ``CONAN_PASSWORD`` environment variable with the Bintray API Key. If your Bintray user is different from the package user, you can define your Bintray username too, defining the environment variable ``CONAN_LOGIN_USERNAME``
#. Clone the repo: ``$ git clone <your_repo/hello> && cd hello``
#. Create the package: ``$ conan new Hello/0.1@<user>/testing -t -s -ciccg -ciccc -cicco -cis -ciu=UPLOAD_URL`` where ``user`` is your Bintray username
#. You can inspect the created files: both ``.circleci/config.yml`` and the ``build.py`` script, that is used by ``conan-package-tools`` utility to split different builds with different configurations in different GitLab CI jobs.
#. You can test locally, before pushing, with ``$ conan create``
#. Add the changes, commit and push: ``$ git add . && git commit -m "first commit" && git push``
#. Go to Pipelines page and see the pipeline, with the different jobs.
#. When it finish, go to your Bintray repository, you should see there the uploaded packages for different configurations
#. Check locally, searching in Bintray: ``$ conan search Hello/0.1@<user>/testing -r=mybintray``

If something fails, please report an issue in the ``conan-package-tools`` github repository: https://github.com/conan-io/conan-package-tools

.. |circleci_logo| image:: ../images/circleci_logo.png
.. _`Circle CI`: https://circleci.com/
