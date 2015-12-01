
Travis Ci
_________


|travisci_logo| 


.. |travisci_logo| image:: ../images/travisci_logo.jpeg
   

If you handle your project requirements with a *conanfile*, you can easily integrate your project with `Travis CI`_.


We are going to use the :ref:`Google Test example<google_test_example>` now with **Travis CI** support to run the tests.


Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


Create a ``.travis.yml`` file and paste this code: 


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
	
	# Download conan
	- wget https://s3-eu-west-1.amazonaws.com/conanio/downloads/conan-ubuntu-64_0_3_0.deb -O conan.deb
	- sudo dpkg -i conan.deb
	- rm conan.deb
	
	# Automatic detection of your arch, compiler, etc
	- conan install
	  
	script:
	- mkdir build
	- cd build && cmake ../ -DBUILD_TEST=TRUE && cmake --build .
	- ./bin/encryption_test


Travis will install **conan** tool and will execute **conan install** command.
Then the **script** section creates the build folder, compiles the project with **cmake** and runs the **tests**



.. _`Travis CI`: https://travis-ci.org/