.. _visual_studio_packages:


Creating and reusing packages based on Visual Studio
============================================================

Conan has different helpers to manage Visual Studio and MSBuild based projects. This how-to illustrates how to put them together to create and consume packages that are purely based on Visual Studio. This how-to is using VS2015, but other versions can be used too.


Creating packages
------------------

Start cloning the existing example repository, containing a simple "Hello World" library, and application:

.. code-block:: bash

    $ git clone https://github.com/memsharded/hello_vs
    $ cd hello_vs

It contains a ``src`` folder with the source code and a ``build`` folder with a Visual Studio 2015 solution, containing 2 projects: the HelloLib static library, and the Greet application. Open it:

.. code-block:: bash

    $ build\HelloLib\HelloLib.sln

You should be able to select the ``Greet`` subproject -> ``Set as Startup Project``. Then build and run the app with Ctrl+F5. (Debug -> Start Without Debugging)


.. code-block:: bash

    $ Hello World Debug!
    # Switch IDE to Release mode, repeat
    $ Hello World Release!

Because the ``hello.cpp`` file contains an ``#ifdef _DEBUG`` to switch between debug and release message.


In the repository, there is already a ``conanfile.py`` recipe:

.. code-block:: python

    from conans import ConanFile, tools

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        license = "MIT"
        url = "https://github.com/memsharded/hello_vs"
        settings = "os", "compiler", "build_type", "arch"
        exports_sources = "src/*", "build/*"

        def build(self):
            cmd = tools.msvc_build_command(self.settings, "build/HelloLib/HelloLib.sln")
            self.run(cmd)

        def package(self):
            self.copy("*.h", dst="include", src="src")
            self.copy("*.lib", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["HelloLib"]


This recipe is using :ref:`the msvc_build_command() function <msvc_build_command>` to get a command string containing required commands to build the application with the correct configuration.

The recipe contains also a ``test_package`` folder with a simple example consuming application. In this example, the consuming application is using cmake to build, but it could also use Visual Studio too. We have left the cmake one because it is the default generated with ``conan new``, and also to show that packages created from Visual Studio projects can also be consumed with other build systems like CMake.

Once we want to create a package, it is advised to close VS IDE, clean the temporary build files from VS to avoid problems, then create and test the package (here it is using system defaults, assuming they are Visual Studio 14, Release, x86_64):

.. code-block:: bash

   # close VS
   $ git clean -xdf
   $ conan test_package
   ...
   > Hello World Release!

Instead of closing the IDE and running ``git clean`` we could also configure a smarter filter in ``exports_sources`` field, so temporary build files are not exported into the recipe.

This process can be repeated to create and test packages for different configurations:

.. code-block:: bash

   $ conan test_package -s arch=x86
   $ conan test_package -s compiler="Visual Studio" -s compiler.runtime=MDd -s build_type=Debug
   $ conan test_package -s compiler="Visual Studio" -s compiler.runtime=MDd -s build_type=Debug -s arch=x86


You can list the different created package binaries:

.. code-block:: bash

    $ conan search Hello/0.1@memsharded/testing

Uploading binaries
-------------------

Your locally created packages can already be uploaded to a conan remote. If you created them with the original username "memsharded", as from the git clone, you might want to do a ``conan copy`` to put them on your own username. Of course, you can also edit the recipes or set the environment variable ``CONAN_USERNAME`` to define your own username.

Another alternative is to configure the permissions in the remote, to allow uploading packages with different usernames. Artifactory will allow it, but by default conan_server doesn't allow that: permissions must be given in ``[write_permissions]`` section of ``server.conf``.


Reusing packages
-------------------

To use existing packages directly from Visual Studio, conan provides the ``visual_studio`` generator. Let's clone an existing "Chat" project, consisting of a ChatLib static library that makes use of the previous "Hello World" package, and a MyChat application, calling the ChatLib library function.

.. code-block:: bash

   $ git clone https://github.com/memsharded/chat_vs
   $ cd chat_vs

As above, the repository contains a Visual Studio solution in the ``build`` folder. But if you try to open it, it will fail to load. This is because it is expecting to find a file with the required information about dependencies, so it is necessary to obtain that file first. Just run:

.. code-block:: bash

    $ conan install .

You will see that it created two files, a ``conaninfo.txt`` file, containing the current configuration of dependencies, and a ``conanbuildinfo.props`` file, containing the Visual Studio properties (like ``<AdditionalIncludeDirectories>``), so it is able to find the installed dependencies.

Now you can open the IDE and build and run the app (by the way, the chat function is just calling the ``hello()`` function two or three times, depending on the build type):

.. code-block:: bash

    $  build\ChatLib\ChatLib.sln
    # Switch to Release
    # MyChat -> Set as Startup Project
    # Ctrl + F5 (Debug -> Run without debugging)
    > Hello World Release!
    > Hello World Release!

If you wish to link with the debug version of Hello package, just install it and change IDE build type:

.. code-block:: bash

    $ conan install . -s build_type=Debug -s compiler="Visual Studio" -s compiler.runtime=MDd
    # Switch to Debug
    # Ctrl + F5 (Debug -> Run without debugging)
    > Hello World Debug!
    > Hello World Debug!
    > Hello World Debug!

Now you can close the IDE and clean the temporary files:

.. code-block:: bash

    # close VS IDE
    $ git clean -xdf

Again, there is a ``conanfile.py`` package recipe in the repository, together with a ``test_package``. The recipe is almost identical to the above one, just with two minor differences:

.. code-block:: python

    requires = "Hello/0.1@memsharded/testing"
    ...
    generators = "visual_studio"

This will allow us to create and test the package of the ChatLib library:

.. code-block:: bash

    $ conan test_package
    > Hello World Release!
    > Hello World Release!

You can also repeat the process for different build types and architectures.


Other configurations
---------------------

The above example works as-is for VS2017, because VS support upgrading from previous versions. The ``tools.msvc_build_command()`` already implements such functionality, so building and testing packages with VS2017 can be done. The only requirement is to define the ``VS150COMNTOOLS`` environment variable, as VS2017 doesn't define it, and it is necessary to find the tools:

.. code-block:: bash

    # maybe better done system-wide after VS2017 installation
    $ set VS150COMNTOOLS C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/Tools
    $ conan test_package -s compiler="Visual Studio" -s compiler.version=15


If you have to build for older versions of Visual Studio, it is also possible. In that case, you would probably have different solution projects inside your build folder. Then the recipe only has to select the correct one, something like:


.. code-block:: python

    def build(self):
        # assuming HelloLibVS12, HelloLibVS14 subfolders
        sln_file = "build/HelloLibVS%s/HelloLib.sln" % self.settings.compiler.version
        cmd = tools.msvc_build_command(self.settings, sln_file)
        self.run(cmd)

Finally, we used just one ``conanbuildinfo.props`` file, which the solution loaded at a global level. You could also define multiple ``conanbuildinfo.props`` files, one per configuration (Release/Debug, x86/x86_64), and load them accordingly.


.. note::

    So far, the ``visual_studio`` generator is single-configuration (packages containing debug or release artifacts, the generally recommended approach), it does not support multi-config packages (packages containing both debug and release artifacts). Please report and provide feedback (submit an issue in github) to request this feature if necessary. 


