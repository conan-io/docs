.. _reference_config_files_remotes_json:

remotes.json
============

The **remotes.json** file is located in the Conan user home directory, e.g., *[CONAN_HOME]/remotes.json*.

The default file created by Conan looks like this:

.. code-block:: json
    :caption: **remotes.json**

    {
     "remotes": [
      {
       "name": "conancenter",
       "url": "https://center2.conan.io",
       "verify_ssl": true
      }
     ]
    }


.. include:: ../../common/conancenter_frozen.inc


Essentially, it tells Conan where to list/upload/download the recipes/binaries from the remotes specified by their URLs.

The fields for each remote are:

* ``name`` (Required, ``string`` value): Name of the remote. This name will be used in commands
  like :ref:`reference_commands_list`, e.g., :command:`conan list zlib/1.2.11 --remote my_remote_name`.
* ``url`` (Required, ``string`` value): indicates the URL to be used by Conan to search for the recipes/binaries.
* ``verify_ssl`` (Required, ``bool`` value): Verify SSL certificate of the specified url.
* ``disabled`` (Optional, ``bool`` value, ``false`` by default): If the remote is enabled or not to be used by commands
  like search, list, download and upload. Notice that a disabled remote can be used to authenticate against it even
  if it's disabled.


.. seealso::

    - :ref:`How to manage SSL (TLS) certificates <reference_config_files_global_conf_ssl_certificates>`
    - :ref:`How to manage remotes.json through CLI: conan remotes <reference_commands_remote>`.
    - :ref:`How to use your own secrets manager for Conan remotes logins <reference_extensions_authorization_plugin>`.
