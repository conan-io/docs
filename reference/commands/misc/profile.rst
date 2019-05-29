
.. _conan_profile:

conan profile
=============

.. code-block:: bash

    $ conan profile [-h] {list,show,new,update,get,remove} ...

Lists profiles in the '.conan/profiles' folder, or shows profile details.

The 'list' subcommand will always use the default user 'conan/profiles' folder. But the
'show' subcommand is able to resolve absolute and relative paths, as well as to map names to
'.conan/profiles' folder, in the same way as the '--profile' install argument.

.. code-block:: text

    positional arguments:
      {list,show,new,update,get,remove}
        list                List current profiles
        show                Show the values defined for a profile
        new                 Creates a new empty profile
        update              Update a profile with desired value
        get                 Get a profile key
        remove              Remove a profile key

    optional arguments:
      -h, --help            show this help message and exit


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

- Update a setting from a profile located in a custom directory:

  .. code-block:: bash

      $ conan profile update settings.build_type=Debug /path/to/my/profile

- Add a new option to the default profile:

  .. code-block:: bash

      $ conan profile update options.zlib:shared=True default

- Create a new empty profile:

  .. code-block:: bash

      $ conan profile new /path/to/new/profile

- Create a new profile detecting the settings:

  .. code-block:: bash

      $ conan profile new /path/to/new/profile --detect

- Create a new or overwrite an existing profile with detected settings:

  .. code-block:: bash

      $ conan profile new /path/to/new/profile --detect --force
