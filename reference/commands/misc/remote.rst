
.. _conan_remote:

conan remote
============

.. code-block:: bash

    $ conan remote [-h]
                   {list,add,remove,update,rename,list_ref,add_ref,remove_ref,update_ref}
                   ...

Manages the remote list and the package recipes associated to a remote.

.. code-block:: text

    positional arguments:
      {list,add,remove,update,rename,list_ref,add_ref,remove_ref,update_ref}
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

    optional arguments:
      -h, --help            show this help message and exit


**Examples**

- List remotes:

  .. code-block:: bash

      $ conan remote list
      conan-center: https://conan.bintray.com [Verify SSL: True]
      local: http://localhost:9300 [Verify SSL: True]

- Add a new remote:

  .. code-block:: bash

      $ conan remote add remote_name remote_url [verify_ssl]

  Verify SSL option can be True or False (default True). Conan client will verify the SSL
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

- Associate a recipe's reference to a remote:

  .. code-block:: bash

      $ conan remote add_ref OpenSSL/1.0.2i@conan/stable conan-center

- Update the remote associated with a package recipe:

  .. code-block:: bash

      $ conan remote update_ref OpenSSL/1.0.2i@conan/stable local-remote

.. note::

   Check the section :ref:`How to manage SSL (TLS) certificates <use_tls_certificates>` section to
   know more about server certificates verification and client certifications management .