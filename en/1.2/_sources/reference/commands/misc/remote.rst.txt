.. _conan_remote:

conan remote
============

.. code-block:: bash

   $ conan remote [-h] {list,add,remove,update,list_ref,add_ref,remove_ref,update_ref} ...

Manages the remote list and the package recipes associated to a remote.

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

- Remove a remote:

  .. code-block:: bash

      $ conan remote remove remote_name

- Update a remote:

  .. code-block:: bash

      $ conan remote update remote_name new_url [verify_ssl]

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