.. _conan_profile_command:

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

