.. _appveyor_ci:


|appveyor_logo| Appveyor
========================



You can use the `AppVeyor`_ cloud service to automatically build and test your project in a Windows environment in the cloud.
It is free for OSS projects, and offers an easy integration with Github, so builds can be automatically
fired in Appveyor after a :command:`git push` to Github.

You can use Appveyor both for:

- Building and testing your project, which manages dependencies with Conan, and probably a conanfile.txt file
- Building and testing Conan binary packages for a given Conan package recipe (with a conanfile.py)


Building and testing your project
------------------------------------

We are going to use an example with GTest package, with **AppVeyor** support to run the tests.


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
	  - cmd: conan install . -o gtest:shared=True
	  - cmd: cd build
	  - cmd: cmake ../ -DBUILD_TEST=TRUE  -G "Visual Studio 14 2015 Win64"
	  - cmd: cmake --build . --config Release

	test_script:
	  - cmd: cd bin
	  - cmd: encryption_test.exe


Appveyor will install the **Conan** tool and will execute the **conan install** command.
Then, the **build_script** section creates the build folder, compiles the project with **cmake** and the section **test_script** runs the **tests**.

Creating, testing and uploading Conan binary packages
-------------------------------------------------------

You can use Appveyor to automate the building of binary packages, which will be created in the
cloud after pushing to Github. You can probably set up your own way, but Conan has some utilities to help in the process.

The command :command:`conan new` has arguments to create a default working *appveyor.yml* file. Other setups might be possible, but for this
example we are assuming that you are using GitHub and also uploading your final packages to Bintray. You could follow these steps:

#. First, create an empty github repository. Let's call it "hello", for creating a "hello world" package. Github allows to create it with a Readme and .gitignore.
#. Get the credentials User and API Key. (Remember, Bintray uses the API key as "password", not your main Bintray account password.)
#. Create a Conan repository in Bintray under your user or organization, and get its URL ("Set me up"). We will call it ``UPLOAD_URL``
#. Activate the repo in your Appveyor account, so it is built when we push changes to it.
#. Under *Appveyor Settings->Environment*, add the ``CONAN_PASSWORD`` environment variable with the Bintray API Key, and encrypt it.  If your Bintray user is different from the package user, you can define your Bintray username too, defining the environment variable ``CONAN_LOGIN_USERNAME``
#. Clone the repo: ``$ git clone <your_repo/hello> && cd hello``
#. Create the package: :command:`conan new Hello/0.1@<user>/testing -t -s -ciw -cis -ciu=UPLOAD_URL` where **user** is your Bintray username
#. You can inspect the created files: both *appveyor.yml* and the *build.py* script, that is used by **conan-package-tools** utility to
   split different builds with different configurations in different appveyor jobs.
#. You can test locally, before pushing, with :command:`conan create`
#. Add the changes, commit and push: :command:`git add . && git commit -m "first commit" && git push`
#. Go to Appveyor and see the build, with the different jobs.
#. When it finish, go to your Bintray repository, you should see there the uploaded packages for different configurations
#. Check locally, searching in Bintray: :command:`conan search Hello/0.1@<user>/testing -r=mybintray`

If something fails, please report an issue in the ``conan-package-tools`` github repository: https://github.com/conan-io/conan-package-tools


.. |appveyor_logo| image:: ../../images/conan-appveyor_logo.png
.. _`AppVeyor`: https://ci.appveyor.com
