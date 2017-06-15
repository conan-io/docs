.. _appveyor_integration:


|appveyor_logo| Appveyor 
========================



You can use `AppVeyor`_ cloud service to automatically build and test your project in a Windows environment in the cloud.
It is free for OSS projects, and offers an easy integration with Github, so builds can be automatically
fired in Appveyor after a ``git push`` to Github.

You can use Appveyor both for:

- Building and testing your project, which manages dependencies with Conan, and probably a conanfile.txt file
- Building and testing conan binary packages for a given conan package recipe (with a conanfile.py)


Building and testing your project
------------------------------------

We are going to use the :ref:`Google Test example<google_test_example>` now, with **AppVeyor** support to run the tests.


Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gtest-example


Create an ``appveyor.yml`` file and paste this code in it: 


.. code-block:: text
   
    version: 1.0.{build}
	platform:
	  - x64
	
	install:
	  - cmd: echo "Downloading conan..."
	  - cmd: set PATH=%PATH%;%PYTHON%/Scripts/
	  - cmd: pip.exe install conan
	  - cmd: conan user # Create the conan data directory
	  - cmd: conan --version
	
	build_script:
	  - cmd: mkdir build 
	  - cmd: conan install -o gtest:shared=True
	  - cmd: cd build 
	  - cmd: cmake ../ -DBUILD_TEST=TRUE  -G "Visual Studio 14 2015 Win64"
	  - cmd: cmake --build . --config Release
	
	test_script:
	  - cmd: cd bin
	  - cmd: encryption_test.exe
	  

Appveyor will install the **conan** tool and will execute the **conan install** command.
Then, the **build_script** section creates the build folder, compiles the project with **cmake** and the section **test_script** runs the **tests**.

Creating and testing conan package binaries
---------------------------------------------------------

You can use Appveyor to automate the building of binary packages, which will be created in the
cloud after pushing to Github. You can probably setup your own way, but it is recommended
to use :ref:`conan tools for package creators <package_tools>`


.. |appveyor_logo| image:: ../images/appveyor_logo.png
.. _`AppVeyor`: https://ci.appveyor.com
