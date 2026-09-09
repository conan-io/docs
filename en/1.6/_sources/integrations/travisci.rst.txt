.. _travis_integration:


.. _travis_ci:

|travisci_logo| Travis Ci
=============================

You can use `Travis CI`_ cloud service to automatically build and test your project in Linux/OSX environments in the cloud.
It is free for OSS projects, and offers an easy integration with Github, so builds can be automatically
fired in Travis-CI after a :command:`git push` to Github.

You can use Travis-CI both for:

- Building and testing your project, which manages dependencies with Conan, and probably a conanfile.txt file
- Building and testing conan binary packages for a given conan package recipe (with a conanfile.py)


Building and testing your project
------------------------------------

We are going to use an example with GTest package now, with **Travis CI** support to run the tests.


Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


Create a ``.travis.yml`` file and paste this code in it: 


.. code-block:: text
   
	language: cpp
	compiler:
	- gcc
	install:
	# Upgrade GCC
	- sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
	- sudo apt-get update -qq
	- sudo apt-get install -qq g++-4.9 
	- sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.9
	
	# Install conan
	- pip install conan
	# Automatic detection of your arch, compiler, etc.
	- conan user
	
	script:
	# Download dependencies, build, test and create package
	- conan create . user/channel


Travis will install the **conan** tool and will execute the **conan install** command.
Then, the **script** section creates the build folder, compiles the project with **cmake** and runs the **tests**.


Creating, testing and uploading conan binary packages
-------------------------------------------------------

You can use Travis to automate the building of binary packages, which will be created in the
cloud after pushing to Github. You can probably setup your own way, but conan has some utilities to help in the process.

The command :command:`conan new` has arguments to create a default working *.travis.yml* file. 
Other setups might be possible, but for this example we are assuming that you are using github and also uploading your final packages to Bintray. 
You could follow these steps:

#. First, create an empty github repository, lets call it "hello", for creating a "hello world" package. Github allows to create it with a Readme and .gitignore.
#. Get the credentials User and API Key (remember, Bintray uses the API key as "password", not your main Bintray account password)
#. Create a conan repository in Bintray under your user or organization, and get its URL ("Set me up"). We will call it ``UPLOAD_URL``
#. Activate the repo in your Travis account, so it is built when we push changes to it.
#. Under *Travis More Options -> Settings->Environment Variables*, add the ``CONAN_PASSWORD`` environment variable with the Bintray API Key. If your Bintray user is different from the package user, you can define your Bintray username too, defining the environment variable ``CONAN_LOGIN_USERNAME``
#. Clone the repo: ``$ git clone <your_repo/hello> && cd hello``
#. Create the package: :command:`conan new Hello/0.1@<user>/testing -t -s -cilg -cis -ciu=UPLOAD_URL` where **user** is your Bintray username.
#. You can inspect the created files: both *.travis.yml*, *.travis/run.sh*, and ``.travis/install.sh`` and the *build.py* script, that is
   used by **conan-package-tools** utility to split different builds with different configurations in different travis jobs.
#. You can test locally, before pushing, with :command:`conan test`.
#. Add the changes, commit and push: :command:`git add . && git commit -m "first commit" && git push`.
#. Go to Travis and see the build, with the different jobs.
#. When it finish, go to your Bintray repository, you should see there the uploaded packages for different configurations.
#. Check locally, searching in Bintray: :command:`conan search Hello/0.1@<user>/testing -r=mybintray`.

If something fails, please report an issue in the ``conan-package-tools`` github repository: https://github.com/conan-io/conan-package-tools


.. |travisci_logo| image:: ../images/travisci_logo.jpeg
.. _`Travis CI`: https://travis-ci.org/
