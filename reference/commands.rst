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

	$ conan install [package_recipe_ref] [--remote REMOTE] [--options OPTIONS] [--settings SETTINGS] [--scope SCOPE]


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
   
   
build options
+++++++++++++

Both the conan **install** and **test** commands have options to specify whether conan should
try to build things or not:

* :command:`--build=never`  This is the default option. It is not necessary to write it explicitly. Conan will
  not try to build packages when the requested configuration does not match, in which case it will
  throw an error.
* :command:`--build=missing` Conan will try to build from source, all packages of which the requested configuration
  was not found on any of the active remotes
* :command:`--build=[pattern]` Conan will force the build of the packages, the name of which matches the given **pattern**.
  Several patterns can be specified, chaining multiple options, e.g. :command:`--build=pattern1 --build=pattern2`
* :command:`--build` Always build everything from source. Produces a clean re-build of all packages
  and transitively dependent packages


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


conan search
------------

.. code-block:: bash

	$ conan search [-r REMOTE] [pattern]

Get complete information about the specified package recipe reference pattern. You can use it on remote or local storage.


**Example**:

.. code-block:: bash

	$ conan search OpenCV/*


conan info
----------

.. code-block:: bash

   $ conan info [package or path]

Get complete information about the specified package recipe pattern or path. 
You can use it for your current project (just point to the path if you want), or for any
existing package in your local cache


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
    Required by:
        Hello/1.0@user/channel

   Hello/1.0@user/channel
       URL: http://...
       License: MIT
       Required by:
           Project
       Requires:
           Hello0/0.1@user/channel

   
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
   
   conan.io: https://server.conan.io
   local: http://localhost:9300
   
   

* Add a new remote:

.. code-block:: bash

   $ conan remote add remote_name remote_url


* Remote a remote:

.. code-block:: bash

   $ conan remote remove remote_name


* Update a remote url:

.. code-block:: bash

   $ conan remote update remote_name new_url
   

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
   

conan package
-------------

Intended for package creators, for regenerating a package without recompiling the source.
Calls your conanfile.py "package" method for a specific package or regenerates the existing package's manifest.


.. code-block:: bash

   $ conan package [-h] [-o] [--all] package_recipe_ref [package]



Positional arguments:

 * **package_recipe_ref**   Package recipe reference name. e.g. openssl/1.0.2@lasote/testing
 * **package**              Package ID to regenerate. e.g.9cf83afd07b678d38a9c1645f605875400847ff3

Optional arguments:

  * **-o, --only-manifest**  Just regenerate manifest for the existing package.If True conan won't call your conanfile's package method.
  * **--all**                Package all packages from specified reference.


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
