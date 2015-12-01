
Appveyor
________

|appveyor_logo| 


If you handle your project requirements with a *conanfile*, you can easily integrate your project with `AppVeyor`_.


We are going to use the :ref:`Google Test example<google_test_example>` now with **AppVeyor** support to run the tests.


Clone the project from github:


.. code-block:: bash

   $ git clone https://github.com/lasote/conan-gest-example


Create a ``appveyor.yml`` file and paste this code: 


.. code-block:: text
   
    version: 1.0.{build}
	platform:
	  - x64
	
	install:
	  - cmd: echo "Downloading conan..."
	  - ps: wget https://s3-eu-west-1.amazonaws.com/conanio/downloads/conan-win_0_3_0.exe -OutFile conan_installer.exe
	  - cmd: conan_installer.exe /VERYSILENT
	  - cmd: set PATH=%PATH%;C:\Program Files (x86)\Conan\conan
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
	  

Travis will install **conan** tool and will execute **conan install** command.
Then the **build_script** section creates the build folder, compiles the project with **cmake** and the section **test_script** runs the **tests**


.. |appveyor_logo| image:: ../images/appveyor_logo.png
.. _`AppVeyor`: https://ci.appveyor.com
