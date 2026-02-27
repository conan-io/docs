.. _gitlab_integration:


.. _gitlab:

|gitlab_logo| Gitlab
=============================

You can use the `Gitlab CI`_ cloud or local service to automatically build and test your project in Linux/MacOS/Windows environments.
It is free for OSS projects, and offers an easy integration with Gitlab, so builds can be automatically
fired in Gitlab CI after a :command:`git push` to Gitlab.

You can use Gitlab CI both for:

- Building and testing your project, which manages dependencies with Conan, and probably a conanfile.txt file
- Building and testing Conan binary packages for a given Conan package recipe (with a conanfile.py)


Building and testing your project
------------------------------------

We are going to use an example with GTest package, with **Gitlab CI** support to run the tests.


Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


Create a ``.gitlab-ci.yml`` file and paste this code in it:


.. code-block:: text

    image: conanio/gcc63

    build:
      before_script:
        # Upgrade Conan version
        - sudo pip install --upgrade conan
        # Automatic detection of your arch, compiler, etc.
        - conan user

      script:
        # Download dependencies, build, test and create package
        - conan create . user/channel


Gitlab CI will install the **conan** tool and will execute the **conan install** command.
Then, the **script** section creates the build folder, compiles the project with **cmake** and runs the **tests**.

.. hint:

On Windows the Gitlab runner may be running as a service and not have a home directory, in which case you need to set a custom value for ``CONAN_USER_HOME``.

Creating, testing and uploading Conan binary packages
------------------------------------------------------
You can use Gitlab CI to automate the building of binary packages, which will be created in the
cloud after pushing to Gitlab. You can probably setup your own way, but Conan has some utilities to help in the process.
The command :command:`conan new` has arguments to create a default working ``.gitlab-ci.yml`` file.
Other setups might be possible, but for this example we are assuming that you are using github and also uploading your final packages to Bintray.
You could follow these steps:

#. First, create an empty gitlab repository, let's call it "hello", for creating a "hello world" package. Gitlab allows to create it with a Readme, license and .gitignore.
#. Get the credentials User and API Key (remember, Bintray uses the API key as "password", not your main Bintray account password)
#. Create a Conan repository in Bintray under your user or organization, and get its URL ("Set me up"). We will call it ``UPLOAD_URL``
#. Under your project page, *Settings -> Pipelines -> Add a variable*, add the ``CONAN_PASSWORD`` environment variable with the Bintray API Key. If your Bintray user is different from the package user, you can also define your Bintray username, defining the environment variable ``CONAN_LOGIN_USERNAME``
#. Clone the repo: :command:`git clone <your_repo/hello> && cd hello`.
#. Create the package: :command:`conan new Hello/0.1@<user>/testing -t -s -ciglg -ciglc -cis -ciu=UPLOAD_URL` where **user** is your Bintray username.
#. You can inspect the created files: both *.gitlab-ci.yml* and the *build.py* script, that is used by **conan-package-tools** utility to
   split different builds with different configurations in different GitLab CI jobs.
#. You can test locally, before pushing, with :command:`conan create` or by GitLab Runner.
#. Add the changes, commit and push: :command:`git add . && git commit -m "first commit" && git push`.
#. Go to Pipelines page and see the pipeline, with the different jobs.
#. When it has finished, go to your Bintray repository, you should see there the uploaded packages for different configurations.
#. Check locally, searching in Bintray: :command:`conan search Hello/0.1@<user>/testing -r=mybintray`.

If something fails, please report an issue in the **conan-package-tools** github repository: https://github.com/conan-io/conan-package-tools

.. |gitlab_logo| image:: ../../images/conan-gitlab_logo.png
.. _`Gitlab CI`: https://about.gitlab.com/
