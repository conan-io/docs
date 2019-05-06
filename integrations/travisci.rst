.. _travis_integration:

.. _travis_ci:

|travisci_logo| Travis CI
=========================

You can use the `Travis CI`_ cloud service to automatically build and test your project in Linux/MacOS environments in the cloud.
It is free for OSS projects, and offers an easy integration with GitHub, so builds can be automatically
fired in Travis-CI after a :command:`git push` to GitHub.

You can use Travis-CI both for:

- Building and testing your project, which manages dependencies with Conan, and probably a *conanfile.txt* file.
- Building and testing Conan binary packages for a given Conan package recipe (with a *conanfile.py*).

Installing dependencies and building your project
-------------------------------------------------

A very common use case is to build your project after Conan takes care of installing your dependencies. Doing this process in Travis CI is
quite convenient as you can do it with :command:`conan install`.

To enable **Travis CI** support, you need to create a *.travis.yml* file and paste this code in it:

.. code-block:: text

    os: linux
    language: python
    python: "3.7"
    dist: xenial
    compiler:
      - gcc
    install:
    # Install conan
      - pip install conan
    # Automatic detection of your arch, compiler, etc.
      - conan user
    script:
    # Download dependencies and build project
      - conan install .
    # Call your build system
      - cmake . -G "Unix Makefiles"
      - cmake --build .
    # Run your tests
      - ctest .

Travis will install the gcc compiler and the :command:`conan` client and will execute the :command:`conan install` command using the
requirements and generators indicated in your *conanfile.py* or *conanfile.txt*. Then, the **script** section installs the requirements and
then you can use your build system to compile the project (using :command:`make` in this example).

Creating, testing and uploading Conan binary packages
-----------------------------------------------------

You can also use Travis CI to automate building new Conan binary packages with every change you push to GitHub. You can probably set up
your own way, but Conan has some utilities to help in the process.

The command :command:`conan new` has arguments to create a default working *.travis.yml* file. Other setups might be possible, but for this
example we are assuming that you are using GitHub and also uploading your final packages to Bintray.

You could follow these steps:

#. First, create an empty GitHub repository. Let's call it "hello", for creating a "hello world" package. GitHub allows creating it with a Readme and .gitignore.
#. Get the credentials User and API Key. (Remember, Bintray uses the API key as "password", not your main Bintray account password.)
#. Create a Conan repository in Bintray under your user or organization, and get its URL ("Set me up"). We will call it ``UPLOAD_URL``
#. Activate the repo in your Travis account, so it is built when we push changes to it.
#. Under *Travis More Options -> Settings->Environment Variables*, add the ``CONAN_PASSWORD`` environment variable with the Bintray API Key.
   If your Bintray user is different from the package user, you can also define your Bintray username, defining the environment variable
   ``CONAN_LOGIN_USERNAME``.
#. Clone the repo: :command:`git clone <your_repo/hello> && cd hello`.
#. Create the package: :command:`conan new Hello/0.1@<user>/testing -t -s -cilg -cis -ciu=UPLOAD_URL` where **user** is your Bintray username.
#. You can inspect the created files: both *.travis.yml*, *.travis/run.sh*, and ``.travis/install.sh`` and the *build.py* script, that is
   used by **conan-package-tools** utility to split different builds with different configurations in different Travis CI jobs.
#. You can test locally, before pushing, with :command:`conan test`.
#. Add the changes, commit and push: :command:`git add . && git commit -m "first commit" && git push`.
#. Go to Travis and see the build, with the different jobs.
#. When it has finished, go to your Bintray repository, you should see there the uploaded packages for different configurations.
#. Check locally, searching in Bintray: :command:`conan search Hello/0.1@<user>/testing -r=mybintray`.

If something fails, please report an issue in the ``conan-package-tools`` GitHub repository: https://github.com/conan-io/conan-package-tools


.. |travisci_logo| image:: ../images/travisci_logo.jpeg
.. _`Travis CI`: https://travis-ci.org/
