.. _commands:


Commands
========


conan export
------------

.. code-block:: bash

	$ conan export [-h] [--path PATH] [--keep-source] user

Copies the package recipe (conanfile.py and associated files) to your local cache.
From the local cache it can be shared and reused in other projects.
Also, from the local cache, it can be uploaded to any remote with the "upload" command.
        
 
.. code-block:: bash   
    
	       
	positional arguments:
	  user                  user_name[/channel]. By default, channel is "testing",
	                        e.g., phil or phil/stable
	
	optional arguments:
	  --path PATH, -p PATH  Optional. Folder with a conanfile.py. Default current
	                        directory.
	  --keep-source, -k     Optional. Do not remove the source folder in the local
	                        cache. Use for testing purposes only
	 



**Examples**


- Export a recipe from the current directory, under the ``myuser/testing`` user and channel:

.. code-block:: bash

	$ conan export myuser


- Export a recipe from any folder directory, under the ``myuser/stable`` user and channel:

.. code-block:: bash

	$ conan export ./folder_name myuser/stable


- Export a recipe without removing the source folder in the local cache:

.. code-block:: bash

	$ conan export fenix/stable -k
	


conan install
-------------

.. code-block:: bash

	$ conan install [-h] [--package PACKAGE] [--all] [--file FILE] [--update]
                        [--scope SCOPE] [--profile PROFILE]
                        [--generator GENERATOR] [--werror]
                        [--manifests [MANIFESTS]]
                        [--manifests-interactive [MANIFESTS_INTERACTIVE]]
                        [--verify [VERIFY]] [--no-imports] [-r REMOTE]
                        [--options OPTIONS] [--settings SETTINGS] [--env ENV]
                        [--build [BUILD [BUILD ...]]]
                        [reference]



Installs the requirements specified in a ``conanfile.py`` or ``conanfile.txt``.
It can also be used to install a concrete recipe/package specified by the ``reference`` parameter.
If the recipe is not found in the local cache it will retrieve the recipe from a remote, looking
for it sequentially in the available configured remotes.
When the recipe has been downloaded it will try to download a binary package matching the specified settings,
only from the remote from which the recipe was retrieved.
If no binary package is found you can build the package from sources using the ``--build`` option.


.. code-block:: bash


	positional arguments:
	  reference             package recipe reference, e.g. MyPackage/1.2@user/channel or ./my_project/
	
	optional arguments:
	  --package PACKAGE, -p PACKAGE
	                        Force install specified package ID (ignore settings/options)
	  --all                 Install all packages from the specified package recipe
	  --file FILE, -f FILE  specify conanfile filename
	  --update, -u          update with new upstream packages, overwriting the local cache if needed.
	  --scope SCOPE, -sc SCOPE
	                        Use the specified scope in the install command
	  --profile PROFILE, -pr PROFILE
	                        Apply the specified profile to the install command
	  --generator GENERATOR, -g GENERATOR
	                        Generators to use
	  --werror              Error instead of warnings for graph inconsistencies
	  --manifests [MANIFESTS], -m [MANIFESTS]
	                        Install dependencies manifests in folder for later verify.
                                Default folder is .conan_manifests, but can be changed.
	  --manifests-interactive [MANIFESTS_INTERACTIVE], -mi [MANIFESTS_INTERACTIVE]
	                        Install dependencies manifests in folder for later verify, asking user for
                                confirmation. Default folder is .conan_manifests, but can be changed.
	  --verify [VERIFY], -v [VERIFY]
	                        Verify dependencies manifests against stored ones
	  --no-imports          Install specified packages but avoid running imports
	  -r REMOTE, --remote REMOTE
	                        look in the specified remote server
	  --options OPTIONS, -o OPTIONS
	                        Options to build the package, overwriting the defaults. e.g., -o with_qt=true
	  --settings SETTINGS, -s SETTINGS
	                        Settings to build the package, overwriting the defaults. e.g., -s compiler=gcc
	  --env ENV, -e ENV     Environment variables that will be set during the package build,
                                e.g. -e CXX=/usr/bin/clang++
	  --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]
	                        Optional, use it to choose if you want to build from sources:
	                        
	                        --build            Build all from sources, do not use binary packages.
	                        --build=never      Never build: use binary packages or fail
                                                   if a binary package is not found (default).
	                        --build=missing    Build from code if a binary package is not found.
	                        --build=outdated   Build from code if the binary is not built with the current
                                                   recipe or when missing binary package.
	                        --build=[pattern]  Always build these packages from source, but never build
                                                   the others.  Allows multiple --build parameters.
		
	


**Examples**

- Install a package requirement from a ``conanfile.txt``, saved in your current directory with one option and setting
(other settings will be defaulted as defined in ``<userhome>/.conan/conan.conf``):

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
   

- Install the **OpenCV/2.4.10@lasote/testing** reference with its default options and 
default settings from ``<userhome>/.conan/conan.conf``:

.. code-block:: bash

	$ conan install opencv/2.4.10@lasote/testing
   
   
- Install the **OpenCV/2.4.10@lasote/testing** reference updating the recipe and the binary package if new upstream versions are available:

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

   - Global environment variables (``-e SOME_VAR="SOME_VALUE"``). These variables will be defined before the `build` step in all the packages and will be cleaned after the `build` execution.
   - Specific package environment variables (``-e zlib:SOME_VAR="SOME_VALUE"``). These variables will be defined only in the specified packages (e.g. zlib). 

You can specify this variables not only for your direct ``requires`` but for any package in the dependency graph.

If you want to define an environment variable but you want to append the variables declared in your
requirements you can use the [] syntax:

.. code-block:: bash

    conan install -e PYTHONPATH=[/other/path]

This way the first entry in the PYTHONPATH variable will be `/other/path` but the PYTHONPATH values declared in the requirements
of the project will be appended at the end using the system path separator.

Read more about environment variables management here: :ref:`Manage environment variables in your recipes<migrate_to_new_environment_management>`

settings
++++++++

With the **-s** parameters you can define:

   - Global settings (-s compiler="Visual Studio"). Will apply to all the requires.
   - Specific package settings (-s zlib:compiler="MinGW"). Those settings will be applied only to the specified packages.

You can specify custom settings not only for your direct ``requires`` but for any package in the dependency graph.


options
+++++++

With the **-o** parameters you can only define specific package options (-o zlib:shared=True).
See :ref:`using options section <usingoptions>` for more information.



.. note::

   You can use :ref:`profiles <profiles>` files to create predefined sets of **settings**, **options**, **environment variables** and **scopes**


conan search
------------

.. code-block:: bash

	$ conan search [-r REMOTE] [pattern]

Search both package recipes and package binaries in the local cache or in a remote server.
If you provide a pattern, then it will search for existing package recipes matching that pattern.

You can search in a remote or in the local cache, if nothing is specified, the local conan cache is
assumed.

.. code-block:: bash

	positional arguments:
	  pattern               Pattern name, e.g. openssl/* or package recipe
	                        reference if "-q" is used. e.g.
	                        MyPackage/1.2@user/channel
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --case-sensitive      Make a case-sensitive search
	  -r REMOTE, --remote REMOTE
	                        Remote origin
	  -q QUERY, --query QUERY
	                        Packages query: "os=Windows AND (arch=x86 OR
	                        compiler=gcc)". The "pattern" parameter has to be a
	                        package recipe reference: MyPackage/1.2@user/channel

**Examples**


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
    
    
The query above will find all the ``MyRecipe`` binary packages, because the recipe doesn't declare "os" as a setting.


conan info
----------

.. code-block:: bash

   $ usage: conan info [-h] [--file FILE] [--only [ONLY]]
                  [--build_order BUILD_ORDER] [--update] [--scope SCOPE]
                  [--profile PROFILE] [-r REMOTE] [--options OPTIONS]
                  [--settings SETTINGS] [--env ENV]
                  [--build [BUILD [BUILD ...]]]
                  [reference]

Prints information about a package recipe's dependency graph. 
You can use it for your current project (just point to the path of your conanfile if you want), or for any
existing package in your local cache.


The ``--update`` option will check if there is any new recipe/package available in remotes. Use ``conan install -u``
to update them.


.. code-block:: bash

    positional arguments:
      reference             reference name or path to conanfile file, e.g.,
                            MyPackage/1.2@user/channel or ./my_project/

    optional arguments:
      --file FILE, -f FILE  specify conanfile filename
      --only [ONLY], -n [ONLY]
                            show fields only
      --build_order BUILD_ORDER, -bo BUILD_ORDER
                            given a modified reference, return an ordered list to
                            build (CI)
      --update, -u          check updates exist from upstream remotes
      --scope SCOPE, -sc SCOPE
                            Use the specified scope in the install command
      --profile PROFILE, -pr PROFILE
                            Apply the specified profile to the install command
      -r REMOTE, --remote REMOTE
                            look in the specified remote server
      --options OPTIONS, -o OPTIONS
                            Options to build the package, overwriting the
                            defaults. e.g., -o with_qt=true
      --settings SETTINGS, -s SETTINGS
                            Settings to build the package, overwriting the
                            defaults. e.g., -s compiler=gcc
      --env ENV, -e ENV     Environment variables that will be set during the
                            package build, -e CXX=/usr/bin/clang++
      --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]
                            given a build policy (same install command "build"
                            parameter), return an ordered list of packages that
                            would be built from sources in install command
                            (simulation)


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

Also you can get a list of nodes that would be built (simulation) in an install command specifying a build policy with the ``--build`` parameter:

e.g., If I try to install ``Boost/1.60.0@lasote/stable`` recipe with ``--build missing`` build policy and ``arch=x86``, which libraries will be build?

.. code-block:: bash

	$ conan info Boost/1.60.0@lasote/stable --build missing -s arch=x86
	bzip2/1.0.6@lasote/stable, zlib/1.2.8@lasote/stable, Boost/1.60.0@lasote/stable
	
	


conan remote
------------

.. code-block:: bash

   $ conan remote [-h] {list,add,remove,update,list_ref,add_ref,remove_ref,update_ref}
   

Handles the remote list and the package recipes associated to a remote.

   
.. code-block:: bash

	positional arguments:
	  {list,add,remove,update,list_ref,add_ref,remove_ref,update_ref}
	                        sub-command help
	    list                list current remotes
	    add                 add a remote
	    remove              remove a remote
	    update              update the remote url
	    list_ref            list the package recipes and its associated remotes
	    add_ref             associate a recipe's reference to a remote
	    remove_ref          dissociate a recipe's reference and its remote
	    update_ref          update the remote associated with a package recipe
	
	optional arguments:
	  -h, --help            show this help message and exit
		

**Examples**

- List remotes:

.. code-block:: bash

   $ conan remote list
   
   conan.io: https://server.conan.io [Verify SSL: True]
   local: http://localhost:9300 [Verify SSL: True]
   
   

- Add a new remote:

.. code-block:: bash

   $ conan remote add remote_name remote_url [verify_ssl]
   
 
Verify SSL option can be True or False (default True). Conan client will verify the SSL certificates.


- Remove a remote:

.. code-block:: bash

   $ conan remote remove remote_name


- Update a remote:

.. code-block:: bash

   $ conan remote update remote_name new_url [verify_ssl]
   

- List the package recipes and its associated remotes:

.. code-block:: bash

   $ conan remote list_ref

   bzip2/1.0.6@lasote/stable: conan.io
   Boost/1.60.0@lasote/stable: conan.io
   zlib/1.2.8@lasote/stable: conan.io
   
   
- Associate a recipe's reference to a remote:


.. code-block:: bash

   $ conan remote add_ref package_recipe_ref remote_name
   
   
- Update the remote associated with a package recipe:

.. code-block:: bash

   $ conan remote update_ref package_recipe_ref new_remote_name




conan profile
-------------

.. code-block:: bash

	$ conan profile [-h] {list,show} ...
	
	
List all the profiles that exist in the ``.conan/profiles`` folder, or show details for a given profile.
The ``list`` subcommand will always use the default user ``.conan/profiles`` folder. But the 
``show`` subcommand is able to resolve absolute and relative paths, as well as to map names to 
``.conan/profiles`` folder, in the same way as the ``--profile`` install argument. 

	
.. code-block:: bash

	positional arguments:
	  {list,show}  sub-command help
	    list       list current profiles
	    show       show the values defined for a profile. Can be a path (relative
	               or absolute) to a profile file in any location.


**Examples**

- List the profiles:

.. code-block:: bash

   $ conan profile list
   > myprofile1
   > myprofile2
   
- Print profile contents:

.. code-block:: bash

   $ conan profile show myprofile1
   Profile myprofile1
   [settings]
   ...
   
- Print profile contents (in the standard directory ``.conan/profiles``):

.. code-block:: bash

   $ conan profile show myprofile1
   Profile myprofile1
   [settings]
   ...
   
- Print profile contents (in a custom directory):

.. code-block:: bash

   $ conan profile show /path/to/myprofile1
   Profile myprofile1
   [settings]
   ...



conan upload
------------

.. code-block:: bash

	$ conan upload [-h] [--package PACKAGE] [--remote REMOTE] [--all]
                    [--force] [--confirm] [--retry RETRY]
                    [--retry_wait RETRY_WAIT]
                    pattern

Uploads recipes and binary packages from your local cache to a remote server.

If you use the ``--force`` variable, it won't check the package date. It will override the remote with the local package.

If you use a pattern instead of a conan recipe reference you can use the ``-c`` or ``--confirm`` option to upload all the matching recipes.

If you use the ``--retry`` option you can specify how many times should conan try to upload the packages in case of failure. The default is 2.
With ``--retry_wait`` you can specify the seconds to wait between upload attempts.

If not remote is specified, the first configured remote (by default conan.io, use
``conan remote list`` to list the remotes) will be used. 


.. code-block:: bash

	positional arguments:
	  pattern               Pattern or package recipe reference, e.g.,
	                        "openssl/*", "MyPackage/1.2@user/channel"
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --package PACKAGE, -p PACKAGE
	                        package ID to upload
	  --remote REMOTE, -r REMOTE
	                        upload to this specific remote
	  --all                 Upload both package recipe and packages
	  --force               Do not check conan recipe date, override remote with
	                        local
	  --confirm, -c         If pattern is given upload all matching recipes
	                        without confirmation
	  --retry RETRY         In case of fail it will retry the upload again N times
	  --retry_wait RETRY_WAIT
	                        Waits specified seconds before retry again
		

**Examples**:

Uploads a package recipe (conanfile.py and the exported files):

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable

Uploads a package recipe and all the generated binary packages to a specified remote:

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable --all -r my_remote


Uploads all recipes and binary packages from our local cache to ``my_remote`` without confirmation:

.. code-block:: bash

   $ conan upload "*" --all -r my_remote -c
   
Upload all local packages and recipes beginning with "Op" retrying 3 times and waiting 10 seconds between upload attempts:

.. code-block:: bash

   $ conan upload "Op*" --all -r my_remote -c --retry 3 --retry_wait 10


conan remove
------------

.. code-block:: bash

	$ conan remove [-h] [-p [PACKAGES]] [-b [BUILDS]] [-s] [-f] [-r REMOTE]
                    pattern


Remove any package recipe or binary matching a pattern. It can also be used to remove
temporary source or build folders in the local conan cache.

If no remote is specified, the removal will be done by default in the local conan cache.


.. code-block:: bash

	positional arguments:
	  pattern               Pattern name, e.g., openssl/*
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -p [PACKAGES], --packages [PACKAGES]
	                        By default, remove all the packages or select one,
	                        specifying the SHA key
	  -b [BUILDS], --builds [BUILDS]
	                        By default, remove all the build folders or select
	                        one, specifying the SHA key
	  -s, --src             Remove source folders
	  -f, --force           Remove without requesting a confirmation
	  -r REMOTE, --remote REMOTE
	                        Will remove from the specified remote


**Examples**:

- Remove from the local conan cache the binary packages (the package recipes will not be removed)
  from all the recipes matching ``OpenSSL/*`` pattern:


.. code-block:: bash

	$ conan remove OpenSSL/* --packages
	

- Remove the temporary build folders from all the recipes matching ``OpenSSL/*`` pattern without requesting confirmation:
	
.. code-block:: bash

	$ conan remove OpenSSL/* --builds --force


- Remove the recipe and the binary packages from a specific remote:
	
.. code-block:: bash

	$ conan remove OpenSSL/1.0.2@lasote/stable -r myremote



conan user
----------

.. code-block:: bash

	$ conan user [-h] [-p PASSWORD] [--remote REMOTE] [-c] [name]

Update your cached user name (and auth token) to avoid it being requested later, e.g. while you're uploading a package.
You can have more than one user (one per remote). Changing the user, or introducing the password is only necessary to upload 
packages to a remote.

.. code-block:: bash

	positional arguments:
	  name                  Username you want to use. If no name is provided it
	                        will show the current user.
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -p PASSWORD, --password PASSWORD
	                        User password. Use double quotes if password with
	                        spacing, and escape quotes if existing
	  --remote REMOTE, -r REMOTE
	                        look in the specified remote server
	  -c, --clean           Remove user and tokens for all remotes



**Examples**:

- List my user for each remote:

.. code-block:: bash

	$ conan user
	
	
- Change **conan.io** remote user to **foo**:

.. code-block:: bash

	$ conan user foo -r conan.io

- Change **conan.io** remote user to **foo**, authenticating against the remote and storing the
  user and authentication token locally, so a later upload won't require entering credentials:

.. code-block:: bash

	$ conan user foo -r conan.io -p mypassword

- Clean all local users and tokens

.. code-block:: bash

    $ conan user --clean


.. note::
	
	The password is not stored in the client computer at any moment. Conan uses `JWT <https://en.wikipedia.org/wiki/JSON_Web_Token>`: conan
	gets a token (expirable by the server) checking the password against the remote credentials. 
	If the password is correct, an authentication token will be obtained, and that token is the
	information cached locally. For any subsequent interaction with the remotes, the conan client will only use that JWT token.


conan copy
----------

.. code-block:: bash

   $ conan copy package_recipe_ref otheruser/otherchannel


Copy conan recipes and packages to another user/channel. Useful to promote packages (e.g. from "beta" to "stable"). 
Also for moving packages from one user to another.


.. code-block:: bash

    positional arguments:
	  reference             package recipe reference, e.g.
	                        MyPackage/1.2@user/channel
	  user_channel          Destination user/channel, e.g. lasote/testing
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --package PACKAGE, -p PACKAGE
	                        copy specified package ID
	  --all                 Copy all packages from the specified package recipe
	  --force               Override destination packages and the package recipe
	    
	    
**Examples**

- Promote a package to **stable** from **beta**:

.. code-block:: bash

    $ conan copy OpenSSL/1.0.2i@lasote/beta lasote/stable
    
    
- Change a package's username:

.. code-block:: bash

    $ conan copy OpenSSL/1.0.2i@lasote/beta foo/beta



conan new
---------

.. code-block:: bash

   $ conan new [-h] [-t] [-i] [-c] name


Creates a new package recipe template with a ``conanfile.py`` and optionally, ``test_package``
package testing files.

.. code-block:: bash

	positional arguments:
	  name          Package name, e.g.: Poco/1.7.3@user/testing
	
	optional arguments:
	  -h, --help    show this help message and exit
	  -t, --test    Create test_package skeleton to test package
	  -i, --header  Create a headers only package template
	  -c, --pure_c  Create a C language package only package, 
	                deleting "self.settings.compiler.libcxx" setting in the configure method


**Examples**:


- Create a new ``conanfile.py`` for a new package **mypackage/1.0@myuser/stable**

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable


- Create also a ``test_package`` folder skeleton:

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable -t




conan test_package
------------------

.. code-block:: bash

	$ conan test_package [-h] [-ne] [-f FOLDER] [--scope SCOPE]
	                          [--keep-source] [--update] [--profile PROFILE]
	                          [-r REMOTE] [--options OPTIONS]
	                          [--settings SETTINGS] [--env ENV]
	                          [--build [BUILD [BUILD ...]]]
	                          [path]



The ``test_package`` (previously named **test**) command looks for a **test_package subfolder** in the current directory, and builds the
project that is in it. It will typically be a project with a single requirement, pointing to
the ``conanfile.py`` being developed in the current directory.

This was mainly intended to do a test of the package, not to run unit or integrations tests on the package
being created. Those tests could be launched if desired in the ``build()`` method.
But it can be used for that purpose if desired, there are no real technical constraints.

The command line arguments are exactly the same as the settings, options, and build parameters
for the ``install`` command, with one small difference:

In conan test, by default, the ``--build=CurrentPackage`` pattern is automatically appended for the
current tested package. You can always manually specify other build options, like ``--build=never``,
if you just want to check that the current existing package works for the test subproject, without
re-building it.

You can use the ``conan new`` command with the ``-t`` option to generate a ``test_package`` skeleton.


.. code-block:: bash

	positional arguments:
	  path                  path to conanfile file, e.g. /my_project/
	
	optional arguments:
	  -ne, --not-export     Do not export the conanfile before test execution
	  -f FOLDER, --folder FOLDER
	                        alternative test folder name
	  --scope SCOPE, -sc SCOPE
	                        Use the specified scope in the install command
	  --keep-source, -k     Optional. Do not remove the source folder in local cache.
                                Use for testing purposes only
	  --update, -u          update with new upstream packages, overwriting the local cache if needed.
	  --profile PROFILE, -pr PROFILE
	                        Apply the specified profile to the install command
	  -r REMOTE, --remote REMOTE
	                        look in the specified remote server
	  --options OPTIONS, -o OPTIONS
	                        Options to build the package, overwriting the defaults. e.g., -o with_qt=true
	  --settings SETTINGS, -s SETTINGS
	                        Settings to build the package, overwriting the defaults. e.g., -s compiler=gcc
	  --env ENV, -e ENV     Environment variables to set during the package build,
                                e.g. -e CXX=/usr/bin/clang++
	  --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]
	                        Optional, use it to choose if you want to build from sources:
	                        
	                        --build            Build all from sources, do not use binary packages.
	                        --build=never      Default option. Never build, use binary packages
                                                   or fail if a binary package is not found.
	                        --build=missing    Build from code if a binary package is not found.
	                        --build=outdated   Build from code if the binary is not built with the
                                                   current recipe or when missing binary package.
	                        --build=[pattern]  Build always these packages from source, but never build
                                                   the others. Allows multiple --build parameters.
		


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


conan source
------------

.. code-block:: bash

   $ conan source [-h] [-f] [reference]


The ``source`` command executes a conanfile.py ``source()`` method, retrieving source code as
defined in the method, both locally, in user space or for a package in the local cache.


.. code-block:: bash

	positional arguments:
	  reference    package recipe reference. e.g., MyPackage/1.2@user/channel or
	               ./my_project/
	
	optional arguments:
	  -h, --help   show this help message and exit
	  -f, --force  In the case of local cache, force the removal of the source
	               folder, then the execution and retrieval of the source code.
	               Otherwise, if the code has already been retrieved, it will do
	               nothing.
		

The ``conan source`` and the ``source()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan source`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt

or adding ``txt`` generator to the consuming conanfile ``generators`` section


**Examples**:

- Call a local recipe's source method: In user space, the command will execute a local conanfile.py 
  ``source()`` method, in the current directory.

.. code-block:: bash

   $ conan source ../mysource_folder


- Call a cached recipe's source method: In the conan local cache, it will execute the recipe ``source()`` , 
  in the corresponding ``source`` folder, as defined by the local cache layout. 
  This command is useful for retrieving such source code before launching multiple concurrent package builds, 
  that could otherwise collide in the source code retrieval process.

.. code-block:: bash

   $ conan source Pkg/0.2@user/channel
   
   

conan build
-----------


.. code-block:: bash

	$ conan build conan build [-h] [--file FILE] [path]

Utility command to run your current project **conanfile.py** ``build()`` method. It doesn't
work for **conanfile.txt**. It is convenient for automatic translation of conan settings and options,
for example to CMake syntax, as it can be done by the CMake helper. It is also a good starting point
if you would like to create a package from your current project.



.. code-block:: bash

    positional arguments:
      path                  path to conanfile.py, e.g., conan build .

    optional arguments:
      -h, --help            show this help message and exit
      --file FILE, -f FILE  specify conanfile filename

	  
	  
The ``conan build`` and the ``build()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan build`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt
    
or adding ``txt`` generator to the consuming conanfile ``generators`` section
	

conan package
-------------

.. code-block:: bash

   $ conan package [-h] reference [package]


Calls your conanfile.py ``package()`` method for a specific package recipe.
Intended for package creators, for regenerating a package without recompiling
the source, i.e. for troubleshooting, and fixing the ``package()`` method, not
normal operation. 

It requires that the package has been built locally, it won't
re-package otherwise. When used in a user space project, it
will execute from the build folder specified as parameter, and the current
directory. This is useful while creating package recipes or just for
extracting artifacts from the current project, without even being a package

This command also works locally, in the user space, and it will copy artifacts from the provided
folder to the current one.

.. code-block:: bash

    positional arguments:
	  reference   package recipe reference e.g. MyPkg/0.1@user/channel, or local
	              path to the build folder (relative or absolute)
	  package     Package ID to regenerate. e.g.,
	              9cf83afd07b678d38a9c1645f605875400847ff3 This optional parameter
	              is only used for the local conan cache. If not specified, ALL binaries 
	              for this recipe are re-packaged

The ``conan package`` and the ``package()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan package`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt
    
or adding  ``txt`` generator to the consuming conanfile ``generators`` section


**Examples**


- Copy artifacts from the provided ``build`` folder to the current one:

.. code-block:: bash

   $ conan package ../build


- Copy the artifacts from the build directory to package directory in the local cache:


.. code-block:: bash

	$ conan package MyPackage/1.2@user/channel 9cf83afd07b678da9c1645f605875400847ff3 


.. note:: 

    Conan package command won't create a new package, use 'install' or 'test_package' instead for
    creating packages in the conan local cache, or `build' for conanfile.py in user space.



conan imports
-------------

.. code-block:: bash

   $ conan imports [-h] [--file FILE] [-d DEST] [-u] [reference]



Execute the ``imports`` stage of a conanfile.txt or a conanfile.py. It requires
to have been previously installed it and have a ``conanbuildinfo.txt`` generated file.

The ``imports`` functionality needs a ``conanbuildinfo.txt`` file, so it has
to be generated with a previous ``conan install`` either specifying it in the conanfile, or as
a command line parameter. It will generate a manifest file called ``conan_imports_manifests.txt``
with the files that have been copied from conan local cache to user space. 


.. code-block:: bash

	positional arguments:
	  reference             Specify the location of the folder containing the
	                        conanfile. By default it will be the current directory.
	                        It can also use a full reference e.g.
	                        MyPackage/1.2@user/channel and the recipe
	                        'imports()' for that package in the local conan cache
	                        will be used
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --file FILE, -f FILE  Use another filename, e.g.: conan imports
	                        -f=conanfile2.py
	  -d DEST, --dest DEST  Directory to copy the artifacts to. By default it will
	                        be the current directory
	  -u, --undo            Undo imports. Remove imported files

The ``conan imports`` and the ``imports()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan imports`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt
    
or adding ``txt`` generator to the consuming conanfile ``generators`` section
    


**Examples**

- Execute the ``imports()`` method for a package in the local cache:


.. code-block:: bash

   $ conan imports MyPackage/1.2@user/channel
   
   
- Import files from a current conanfile in current directory:

.. code-block:: bash

   $ conan install --no-imports -g txt # Creates the conanbuildinfo.txt
   $ conan imports
   

- Remove the copied files (undo the import):


.. code-block:: bash

   $ conan imports --undo


conan config
------------

.. code-block:: bash

   $ conan config [-h] {rm,set,get} ...


Manages conan.conf information.

.. code-block:: bash

    positional arguments:
      {rm,set,get}  sub-command help
        rm          rm an existing config element
        set         set/add value
        get         get the value of existing element


**Examples**

- Change the logging level to 10:

.. code-block:: bash

    $ conan config set log.level=10

- Get the logging level:

.. code-block:: bash

    $ conan config get log.level
    $> 10


