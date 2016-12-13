.. _commands:


Commands
========


conan export
------------

.. code-block:: bash

	$ conan export [--path PATH] user/channel


Export a package recipe under the specified user_name/channel.
A **conanfile.py** file has to be located in the specified path.
By default, the path is the current directory and the channel is ``testing``.


**Examples**


Export a package recipe from the current directory, under the ``fenix/testing`` user:

.. code-block:: bash

	$ conan export fenix


Export a package recipe from any folder directory, under the ``fenix/stable`` user:

.. code-block:: bash

	$ conan export ./folder_name fenix/stable


conan install
-------------

.. code-block:: bash

	$ conan install [package_recipe_ref] [--remote REMOTE] [--options OPTIONS] [--settings SETTINGS] [--scope SCOPE] [--profile PROFILE] [--update, -u] [--env ENV]



Install a package recipe and a remote package that matches with the specified settings.
It can be done specifying a ``package_recipe_ref`` (Hello/0.1@demo/testing) or installing the requirements defined in a ``conanfile.py`` or ``conanfile.txt``.

**Examples**

Install a package requirement from a ``conanfile.txt``, saved in your current directory with one option and setting:

.. code-block:: bash

	$ conan install . -o use_debug_mode=on -s compiler=clang


.. note::

   You have to take into account that **settings** are cached as defaults in the **conaninfo.txt** file,
   so you don't have to type them again and again in the **conan install** or **conan test**
   commands. 
   
   However, the default **options** are defined in your **conanfile**.
   If you want to change the default options across all your **conan install** commands, change
   them in the **conanfile**. When you change the **options** on the command line, they are only changed
   for one shot. Next time, **conan install** will take the **conanfile** options as default values, if you
   don't specify them again in the command line.
   

Install the **OpenCV/2.4.10@lasote/testing** reference with its default options and settings:

.. code-block:: bash

	$ conan install opencv/2.4.10@lasote/testing
   
   
Install the **OpenCV/2.4.10@lasote/testing** reference updating the recipe and the binary package if new upstream versions are available:

.. code-block:: bash

   $ conan install opencv/2.4.10@lasote/testing --update


.. _buildoptions:


build options
+++++++++++++

Both the conan **install** and **test** commands have options to specify whether conan should
try to build things or not:

* :command:`--build=never`  This is the default option. It is not necessary to write it explicitly. Conan will
  not try to build packages when the requested configuration does not match, in which case it will
  throw an error.
* :command:`--build=missing` Conan will try to build from source, all packages of which the requested configuration
  was not found on any of the active remotes.
* :command:`--build=outdated` Conan will try to build from code if the binary is not built with the current recipe or when missing binary package 
* :command:`--build=[pattern]` Conan will force the build of the packages, the name of which matches the given **pattern**.
  Several patterns can be specified, chaining multiple options, e.g. :command:`--build=pattern1 --build=pattern2`
* :command:`--build` Always build everything from source. Produces a clean re-build of all packages
  and transitively dependent packages


env variables
+++++++++++++

With the **-e** parameters you can define:

   - Global environment variables (-e SOME_VAR="SOME_VALUE"). These variables will be defined before the `build` step in all the requires and will be cleaned after the `build` execution.
   - Specific package environment variables (-e zlib:SOME_VAR="SOME_VALUE"). These variables will be defined only in the specified requires. 

You can specify this variables not only for your direct requires but any require in the dependency tree.


settings
++++++++

With the **-s** parameters you can define:

   - Global settings (-s compiler="Visual Studio"). Will apply to all the requires.
   - Specific package settings (-s zlib:compiler="MinGW"). Those settings will be applied only to the specified requires.

You can specify custom settings not only for your direct requires but any require in the dependency tree.


options
+++++++

With the **-o** parameters you can only define specific package options (-o zlib:shared=True).
See :ref:`using options section <usingoptions>` for more information.



.. note::

   You can use :ref:`profiles <profiles>` files to create predefined sets of **settings**, **options**, **environment variables** and **scopes**



conan build
-----------
Utility command to run your current project **conanfile.py** ``build()`` method. It doesn't
work for **conanfile.txt**. It is convenient for automatic translation of conan settings and options,
for example to CMake syntax, as it can be done by the CMake helper. It is also a good starting point
if you would like to create a package from your current project.


conan test_package
------------------

The **test_package** (previously named **test**) command looks for a ``test_package`` subfolder in the current directory, and builds the
project that is in it. It will typically be a project with a single requirement, pointing to
the **conanfile.py** being developed in the current directory.

This is intended to do a test of the package, not to run unit or integrations tests on the package
being created. Those tests could be launched if desired in the ``build()`` method.

The command line arguments are exactly the same as the settings, options, and build parameters
for the **install** command, with one small difference.

In conan test, by default, the **--build=CurrentPackage** pattern is automatically apended for the
current tested package. You can always manually specify other build options, like **--build=never**,
if you just want to check that the current existing package works for the test subproject, without
re-building it.

If you want to use a different folder name than **test_package**, just use it and pass it to the ``-f folder``
command line option

.. code-block:: bash

    $ conan test_package --f my_test_folder


This command will run the equivalent to ``conan export <user>/<channel>`` where ``user`` and ``channel``
will be deduced from the values of the requirement in the ``conanfile.py`` inside the test subfolder.
This is very convenient, as if you are running a package test it is extremely likely that you have
just edited the package recipe. If the package recipe is locally modified, it has to be exported again,
otherwise, the package will be tested with the old recipe. If you want to inhibit this ``export``,
you can use the ``-ne, --no-export`` parameter.


conan search
------------

Conan search can search both for package recipes and package binaries. If you provide a pattern,
then it will search for existing package recipes matching that pattern:

.. code-block:: bash

	$ conan search [-r REMOTE] [pattern]

Get complete information about the specified package recipe reference pattern.
You can use it on remote or local storage, if nothing is specified, the local conan cache is
assumed:


.. code-block:: bash

	$ conan search OpenCV/*
	$ conan search OpenCV/* -r=conan.io


If you use instead the full package recipe reference, you can explore the binaries existing for
that recipe, also in a remote or in the local conan cache:

.. code-block:: bash

    $ conan search Boost/1.60.0@lasote/stable

A query syntax is allowed to look for specific binaries, you can use ``AND`` and ``OR`` operators and parenthesis, with settings and also options.

.. code-block:: bash

    $ conan search Boost/1.60.0@lasote/stable -q arch=x86_64
    $ conan search Boost/1.60.0@lasote/stable -q "(arch=x86_64 OR arch=ARM) AND (build_type=Release OR os=Windows)"
    
    
If you specify a query filter for a setting and the package recipe is not restricted by this setting, will find all packages:

.. code-block:: python

    class MyRecipe(ConanFile):
        settings="arch"
        
        
.. code-block:: bash

    $ conan search MyRecipe/1.0@lasote/stable -q os=Windows
    
    
The query above will find all the MyRecipe binary packages, because the recipe doesn't declare "os" as a setting.
   


conan info
----------

.. code-block:: bash

   $ conan info [package or path] [--update, -u]

Get complete information about the specified package recipe pattern or path. 
You can use it for your current project (just point to the path if you want), or for any
existing package in your local cache.

The ``--update`` option will check if there is any new recipe/package available in remotes. Use ``conan install -u``
to update them.


**Examples**:

.. code-block:: bash

   $ conan info 
   $ conan info myproject_path
   $ conan info Hello/1.0@user/channel
   
The output will look like:

.. code-block:: bash

   Dependency/0.1@user/channel
    URL: http://...
    License: MIT
    Updates: Version not checked
    Required by:
        Hello/1.0@user/channel

   Hello/1.0@user/channel
       URL: http://...
       License: MIT
       Updates: Version not checked
       Required by:
           Project
       Requires:
           Hello0/0.1@user/channel


It is possible to use the ``conan info`` command to extract useful information for Continuous
Integration systems. More precisely, it has the ``--build_order, -bo`` option, that will produce
a machine-readable output with an ordered list of package references, in the order they should be
built. E.g., lets assume that we have a project that depends on Boost and Poco, which in turn 
depends on OpenSSL and ZLib transitively. So we can query our project with a reference that has
changed (most likely due to a git push on that package):

.. code-block:: bash

    $ conan info -bo zlib/1.2.8@lasote/stable
    [zlib/1.2.8@lasote/stable], [OpenSSL/1.0.2g@lasote/stable], [Boost/1.60.0@lasote/stable, Poco/1.7.2@lasote/stable]
    
Note the result is a list of lists. When there is more than one element in one of the lists, it means
that they are decoupled projects and they can be built in parallel by the CI system.


conan upload
------------

.. code-block:: bash

	$ conan upload [--package PACKAGE] [--remote REMOTE] [--all] [--force]

Uploads packages from your local to remote storage. If you use the ``--force`` variable, it wiil not check the package date. It will override the remote with the local package.

**Examples**:

Uploads a package recipe (conanfile.py and the exported files):

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable

Uploads a package recipe and all the generated packages to a specified remote:

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable --all -r my_remote


conan remove
------------

.. code-block:: bash

	$ conan remove [-p [PACKAGES]] [-b [BUILDS]] [-f] [-r REMOTE] pattern

Remove any package recipe folders matching a pattern, or their packages and/or build folders.

**Example**:

.. code-block:: bash

	$ conan remove OpenSSL/* --packages


conan user
----------

.. code-block:: bash

	$ conan user [-p PASSWORD] [--remote REMOTE] [name]

Update your cached user name [and password] to avoid it being requested later, e.g. while you're uploading a package.
You can have more than one user, and locally manage all your packages from your different accounts,
without having to change user. Just **conan export user/channel** the conanfiles, and develop.
Changing the user, or introducing the password is only necessary for uploading to the servers.


conan remote
------------

Handles the remote list and the package recipes associated to a remote.


.. code-block:: bash

   $ conan remote  {list,add,remove,update,list_ref,add_ref,remove_ref,update_ref}


* List remotes:

.. code-block:: bash

   $ conan remote list
   
   conan.io: https://server.conan.io [Verify SSL: True]
   local: http://localhost:9300 [Verify SSL: True]
   
   

* Add a new remote:

.. code-block:: bash

   $ conan remote add remote_name remote_url [verify_ssl]
   
 
Verify SSL option can be True or False (default True). Conan client will verify the SSL certificates.


* Remove a remote:

.. code-block:: bash

   $ conan remote remove remote_name


* Update a remote:

.. code-block:: bash

   $ conan remote update remote_name new_url [verify_ssl]
   

* List the package recipes and its associated remotes:

.. code-block:: bash

   $ conan remote list_ref

   bzip2/1.0.6@lasote/stable: conan.io
   Boost/1.60.0@lasote/stable: conan.io
   zlib/1.2.8@lasote/stable: conan.io
   
   
* Associate a recipe's reference to a remote:


.. code-block:: bash

   $ conan remote add_ref package_recipe_ref remote_name
   
   
* Update the remote associated with a package recipe:

.. code-block:: bash

   $ conan remote update_ref package_recipe_ref new_remote_name
   
conan source
------------

The ``source`` command executes a conanfile.py ``source()`` method, retrieving source code as
defined in the method, both locally, in user space or for a package in the local cache.

Positional arguments:

* **reference**   Package recipe reference name. e.g. openssl/1.0.2@lasote/testing or local path, e.g. ./myproject

Optional arguments:

* **-f, --force**  In the case of local cache, force the removal of the source folder, then the execution and
  retrieval of the source code. Otherwise, if the code has already been retrieved, it will do nothing.


In user space, the command will execute a local conanfile.py ``source()`` method, in the current
directory.

.. code-block:: bash

   $ conan source ../mysource_folder


In the conan local cache, it will execute the recipe ``source()`` , in the corresponding ``source``
folder, as defined by the local cache layout. This command is useful for retrieving such source
code before launching multiple concurrent package builds, that could otherwise collide in the
source code retrieval process.

.. code-block:: bash

   $ conan source Pkg/0.2@user/channel


conan package
-------------

Intended for package creators, for regenerating a package without recompiling the source. That is,
it is just an optimization. Most likely **command not needed** for most use cases.
Calls your conanfile.py ``package()`` method. 
It is necessary that the package has already been built locally.

.. code-block:: bash

   $ conan package [-h] reference [package]


Positional arguments:

 * **reference**    Package recipe reference name. e.g. openssl/1.0.2@lasote/testing, or path, e.g. ../build_folder
 * **package**      Package ID to regenerate. e.g.9cf83afd07b678d38a9c1645f605875400847ff3. This
   optional parameter is only used for the local conan cache.


This command also works locally, in the user space, and it will copy artifacts from the provided
folder to the current one.

.. code-block:: bash

   $ conan package ../build

This local command is useful for extracting artifacts locally from a build (without being a real
conan package), or to test things before actually creating a conan package.


conan copy
----------

Copy conan recipes and packages to another user/channel. Useful to promote packages (e.j. from "beta" to "stable"). 
Also for moving packages from an user to another.


.. code-block:: bash

   $ conan copy package_recipe_ref otheruser/otherchannel

Positional arguments:

 * **package_recipe_ref**   Package recipe reference name. e.g. openssl/1.0.2@lasote/testing
 * **user_channel**         Destination user/channel. e.g. lasote/stable

Optional arguments:

  * **-p** Specify a package to copy. e.g. -p 9cf83afd07b678d38a9c1645f605875400847ff3
  * **--force** Override destination packages and the package recipe.
  * **--all**   Copy all packages from the specified package recipe


conan new
---------

.. code-block:: bash

   $ conan new package/version@user/channel


Creates a new ``conanfile.py`` file from a template.


 * **-t, --test**              Create test_package skeleton to test_package command.
 * **-i, --header**            Create a headers only package template.
 * **-c, --pure_c**            Create a C language package only package (non-headers).

**Examples**


Create a new ``conanfile.py`` for a new package **mypackage/1.0@myuser/stable**

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable


Create also a test_package folder skeleton:

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable -t



conan imports
-------------

.. code-block:: bash

   $ conan imports


Execute the ``imports`` stage of a conanfile.txt or a conanfile.py

Positional arguments:

 * **reference**   Specify the location of the folder containing the conanfile.
   By default it will be the current directory. It can also use a full reference e.g. openssl/1.0.2@lasote/testing
   and the recipe ``imports()`` for that package in the local conan cache will be used

Optional arguments:


 * **-f, --file**              Use another filename, e.g.: ``conan imports -f=conanfile2.py``
 * **-d, --dest**              Directory to copy the artifacts to. By default it will be the current
   directory.


The ``imports`` functionality needs the existence of the file ``conanbuildinfo.txt``, so it has
to be generated in the previous ``conan install``, either specifying it in the conanfile, or as
a command line parameter:

**Examples**


.. code-block:: bash

   $ conan install --no-imports -g txt
   $ conan imports


