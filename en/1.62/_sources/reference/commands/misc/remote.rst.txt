
.. _conan_remote:

conan remote
============

.. code-block:: bash

    $ conan remote [-h]
                   {list,add,remove,update,rename,list_ref,add_ref,remove_ref,update_ref,list_pref,add_pref,remove_pref,update_pref,clean,enable,disable}
                   ...

Manages the remote list and the package recipes associated with a remote.

.. code-block:: text

    positional arguments:
      {list,add,remove,update,rename,list_ref,add_ref,remove_ref,update_ref,list_pref,add_pref,remove_pref,update_pref,clean,enable,disable}
                            sub-command help
        list                List current remotes
        add                 Add a remote
        remove              Remove a remote
        update              Update the remote url
        rename              Update the remote name
        list_ref            List the package recipes and its associated remotes
        add_ref             Associate a recipe's reference to a remote
        remove_ref          Dissociate a recipe's reference and its remote
        update_ref          Update the remote associated with a package recipe
        list_pref           List the package binaries and its associated remotes
        add_pref            Associate a package reference to a remote
        remove_pref         Dissociate a package's reference and its remote
        update_pref         Update the remote associated with a binary package
        clean               Clean the list of remotes and all recipe-remote
                            associations
        enable              Enable a remote
        disable             Disable a remote

    optional arguments:
      -h, --help            show this help message and exit


**Examples**

- List remotes:

  .. code-block:: bash

      $ conan remote list
      conancenter: https://center.conan.io [Verify SSL: True]
      local: http://localhost:9300 [Verify SSL: True, Disabled: True]

- List remotes in a format almost valid for the *remotes.txt* to use with :ref:`conan_config_install`, only need
  to remove the ``True`` boolean appended to disabled remotes (notice line for ``local`` one in the output):

  .. code-block:: bash

      $ conan remote list --raw
      conancenter https://center.conan.io True
      local http://localhost:9300 True True
      # capture the current remotes in a text file
      $ conan remote list --raw > remotes.txt

- Add a new remote:

  .. code-block:: bash

      $ conan remote add remote_name remote_url [verify_ssl]

  Verify SSL option can be True or False (defaulted to True). Conan client will verify the SSL
  certificates.

- Insert a new remote:

  Insert as the first one (position/index 0), so it is the first one to be checked:

  .. code-block:: bash

      $ conan remote add remote_name remote_url [verify_ssl] --insert

  Insert as the second one (position/index 1), so it is the second one to be checked:

  .. code-block:: bash

      $ conan remote add remote_name remote_url [verify_ssl] --insert=1


- Add or insert a remote:

Adding the ``--force`` argument to ``conan remote add`` will always work, and won't raise an error.
If an existing remote exists with that remote name or URL, it will be updated with the new information.
The ``--insert`` works the same. If not specified, the remote will be appended the last one. If specified,
the command will insert the remote in the specified position

  .. code-block:: bash

      $ conan remote add remote_name remote_url [verify_ssl] --force --insert=1


- Remove a remote:

  .. code-block:: bash

      $ conan remote remove remote_name

- Remove all configured remotes (this will also remove all recipe-remote associations):

  .. code-block:: bash

      $ conan remote clean

- Update a remote:

  .. code-block:: bash

      $ conan remote update remote_name new_url [verify_ssl]

- Rename a remote:

  .. code-block:: bash

      $ conan remote rename remote_name new_remote_name

- Change an existing remote to the first position:

  .. code-block:: bash

      $ conan remote update remote_name same_url --insert 0

- List the package recipes and its associated remotes:

  .. code-block:: bash

      $ conan remote list_ref
      bzip2/1.0.6@lasote/stable: conan.io
      Boost/1.60.0@lasote/stable: conan.io
      zlib/1.2.8@lasote/stable: conan.io

- In some cases you may want to list the packages that are not associated with any remote:

  .. code-block:: bash

      $ conan remote list_ref --no-remote
      spdlog/1.8.0: None
      restinio/0.6.10: None
      opencv/2.4.13.7: None

- Also, you can list the remote association for different binaries of the same Conan package:

  .. code-block:: bash

      $ conan remote list_pref zlib/1.2.8@
      zlib/1.2.8:f83037eff23ab3a94190d7f3f7b37a2d6d522241: conancenter
      zlib/1.2.8:e46341e9b52d3e4c66657dc8fb13ab6cdd5831c6: conan-local-dev
      zlib/1.2.8:9de3196f2439d69299f168e3088bbefafe212f38: conan-local-prod

- If you want to know if any binaries of a Conan package have no remote association:

  .. code-block:: bash

      $ conan remote list_pref zlib/1.2.8@  --no-remote
      zlib/1.2.8:a7480322bf53ca215dbba4db77ee500c7c51ee33: None

- Associate a recipe's reference to a remote:

  .. code-block:: bash

      $ conan remote add_ref openssl/1.0.2u conancenter

- Update the remote associated with a package recipe:

  .. code-block:: bash

      $ conan remote update_ref openssl/1.0.2t local-remote

- Enable or disable remotes (accepts patterns such as ``*`` as argument using Unix shell-style wildcards):

  .. code-block:: bash

      $ conan remote disable "*"
      $ conan remote enable local-remote

.. note::

   Check the section :ref:`How to manage SSL (TLS) certificates <use_tls_certificates>` section to
   know more about server certificates verification and client certifications management .
