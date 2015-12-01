.. _commands:


Commands
========


conan export
------------

.. code-block:: bash

	$ conan export [--path PATH] user/channel


Export a conanfile located in the specified path under an user_name/channel specified.
By default, the path is the current directory and the channel is ``testing``


**Examples**


Export a conanfile.py from the current directory under ``fenix/testing`` user:

.. code-block:: bash

	$ conan export fenix


Export a conanfile.py from any folder directory under ``fenix/stable`` user:

.. code-block:: bash

	$ conan export ./folder_name fenix/stable


conan install
-------------

.. code-block:: bash

	$ conan install [conanfile_ref] [--remote REMOTE] [--options OPTIONS] [--settings SETTINGS]


Install a remote package specifying a ``conanfile_ref`` or install the requirements defined in a ``conanfile.py`` or ``conanfile.txt``.


**Examples**

Install a package requirement from a ``conanfile.txt`` saved in your current directory with one option and setting:

.. code-block:: bash

	$ conan install . -o use_debug_mode=on -s compiler=clang


.. note::

   You have to take into account that **settings** are cached as defaults in the **conaninfo.txt** file,
   so you don't have to type them again and again in the **conan install** or **conan test**
   commands. 
   
   But the default **options** are defined in your **conanfile**.
   If you want to change the default options across all your **conan install** commands, change
   them in the **conanfile**. If you change the **options** in the command line, they are changed
   just for one shot, next **conan install** will take **conanfile** options default values if you
   don't specify them again in the command line.
   

Install the **OpenCV/2.4.10@lasote/testing** reference with its default options and settings:

.. code-block:: bash

	$ conan install opencv/2.4.10@lasote/testing
   
   
build options
+++++++++++++

Both the conan **install** and **test** commands have options to specify whether it should
try to build things or not:

* **--build=never**  This is default option, not necessary to write it explicitely. It will
  not try to build packages when the requested configuration does not match, and throw an
  error
* **--build=missing** It will try to build from source all packages which requested configuration
  was not found on any of the active remotes
* **--build=[pattern]** It will force the build of the packages which name matches the given **pattern**.
  Several patterns can be specified chaining multiple options **--build=pattern1 --build=pattern2**
* **--build**. Build always from source, everything. Produces a clean re-build of all packages
  and transitively dependent packages


conan build
-----------
Utility command to run your current project **conanfile.py** ``build()`` method. It doesn't
work for **conanfile.txt**. It is convenient for automatic translation of conan settings and options
for example to CMake syntax, as it can be done by the CMake helper. It is also a good starting point
if you pretend to create a package from your current project.


conan test
----------

The **test** command looks for a ``test`` subfolder in the current directory, and builds the
project that is in it. It will typically be a project with a single requirement to the **conanfile.py**
being developed in the current directory.

The command line parameters are exactly the same as the **install** command, the settings, options,
and build parameters, with one small change.

In conan test, by default, the **--build=CurrentPackage** pattern is automatically apended for the
current tested package. You can always manually specify other build options, as **--build=never**
if you want just to check that the current existing package works for the test subproject without
re-building it.

conan search
------------

.. code-block:: bash

	$ conan search [-r REMOTE] [pattern]

Get a complete information about the specified reference pattern. You can use it to remote or local storage.


**Example**:

.. code-block:: bash

	$ conan search OpenCV/*


conan upload
------------

.. code-block:: bash

	$ conan upload [--package PACKAGE] [--remote REMOTE] [--all] [--force]

Uploads packages from your local storage to a remote one. If you use ``--force`` variable, it wiil not check the package date, it will be overridden remote with local

**Examples**:

Uploads a conanfile.py:

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable

Uploads a complete package to a specified remote:

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable --all -r my_remote


conan remove
------------

.. code-block:: bash

	$ conan remove [-p [PACKAGES]] [-b [BUILDS]] [-f] [-r REMOTE] pattern

Remove any ``conanfile_ref`` folders specifying a pattern, or their packages and/or build folders.

**Example**:

.. code-block:: bash

	$ conan remove OpenSSL/* --packages


conan user
----------

.. code-block:: bash

	$ conan user [-p PASSWORD] [--remote REMOTE] [name]

Update your cached user [and your password] to avoid it will be requested later, e.g., while you're uploading a package.
You can have more than one user, and locally manage all your packages from your different accounts
without having to change user. Just **conan export user/channel** the conanfiles, and develop.
Changing the user, or introducing the password is only necessary for uploading to the servers.