
.. _user_json:


User output
-----------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The :command:`conan user` provides a :command:`--json` parameter to generate a file containing the
information of the users configured per remote.

The output JSON contains a two first level keys:

  - **error**: Boolean indicating whether command completed with error.
  - **remotes**: A list of the remotes with the packages found. Each element contains:

    - **name**: Name of the remote.
    - **user_name**: Name of the user set for that remote.
    - **authenticated**: Boolean indicating if user is authenticated or not.

**Example:**

List users per remote: :command:`conan user --json user.json`

  .. code-block:: json
     :caption: *user.json*

      {
          "error":false,
          "remotes":[  
              {
                  "name":"conan-center",
                  "user_name":"danimtb",
                  "authenticated":true
              },
              {
                  "name":"bincrafters",
                  "user_name":null,
                  "authenticated":false
              },
              {
                  "name":"conan-community",
                  "user_name":"danimtb",
                  "authenticated":true
              },
              {
                  "name":"the_remote",
                  "user_name":"foo",
                  "authenticated":false
              }
          ]
      }
