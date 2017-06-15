.. _travis_integration:


|travisci_logo| Travis Ci
=============================

You can use `Travis CI`_ cloud service to automatically build and test your project in Linux/OSX environments in the cloud.
It is free for OSS projects, and offers an easy integration with Github, so builds can be automatically
fired in Travis-CI after a ``git push`` to Github.

You can use Travis-CI both for:

- Building and testing your project, which manages dependencies with Conan, and probably a conanfile.txt file
- Building and testing conan binary packages for a given conan package recipe (with a conanfile.py)


Building and testing your project
------------------------------------

We are going to use the :ref:`Google Test example<google_test_example>` now, with **Travis CI** support to run the tests.


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
	- conan test_package


Travis will install the **conan** tool and will execute the **conan install** command.
Then, the **script** section creates the build folder, compiles the project with **cmake** and runs the **tests**.


Creating and testing conan package binaries
---------------------------------------------------------
You can use Travis to automate the building of binary packages, which will be created in the
cloud after pushing to Github. You can probably setup your own way, but it is recommended
to use :ref:`conan tools for package creators <package_tools>`


.. |travisci_logo| image:: ../images/travisci_logo.jpeg
.. _`Travis CI`: https://travis-ci.org/
