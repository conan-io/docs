
.. _install_json:


Install and Create output [EXPERIMENTAL]
----------------------------------------


The :command:`conan install` and :command:`conan create` provide a ``--json`` parameter to generate
a file containing the information of the installation process.

The output JSON contains a two first level keys:

  - **error**: True is the install completed without error, False otherwise.
  - **installed**: A list of installed packages. Each element contains:

     - **recipe**: Document representing the downloaded recipe.

        - **remote**: remote URL if the recipe has been downloaded. ``null`` otherwise.
        - **cache**: ``true``/``false``. Retrieved from cache (not downloaded).
        - **downloaded**: ``true``/``false``. Downloaded from a remote (not in cache).
        - **time**: ``ISO 8601`` string with the time the recipe was downloaded/retrieved.
        - **error**: ``true``/``false``.
        - **id**: Reference. e.j: "OpenSSL/1.0.2n@conan/stable"

     - **packages**: List of elements, representing the binary packages downloaded for the recipe.
       Normally it will be only 1 element in this list, only in special cases with build requires, private
       dependencies and settings overriding this list could have more than one element.

        - **remote**: remote URL if the recipe has been downloaded. ``null`` otherwise.
        - **cache**: ``true``/``false``. Retrieved from cache (not downloaded).
        - **downloaded**: ``true``/``false``. Downloaded from a remote (not in cache).
        - **time**: ISO 8601 string with the time the recipe was downloaded/retrieved.
        - **error**: ``true``/``false``.
        - **id**: Package ID. e.j: "8018a4df6e7d2b4630a814fa40c81b85b9182d2b"


.. code-block:: json
    :caption: Example:

    {
       "installed":[
          {
             "packages":[
                {
                   "remote":null,
                   "built":false,
                   "cache":true,
                   "downloaded":false,
                   "time":"2018-03-28T08:39:41.385285",
                   "error":null,
                   "id":"227fb0ea22f4797212e72ba94ea89c7b3fbc2a0c"
                }
             ],
             "recipe":{
                "remote":null,
                "cache":true,
                "downloaded":false,
                "time":"2018-03-28T08:39:41.365836",
                "error":null,
                "id":"OpenSSL/1.0.2n@conan/stable"
             }
          },
          {
             "packages":[
                {
                   "remote":null,
                   "built":false,
                   "cache":true,
                   "downloaded":false,
                   "time":"2018-03-28T08:39:41.384952",
                   "error":null,
                   "id":"8018a4df6e7d2b4630a814fa40c81b85b9182d2b"
                }
             ],
             "recipe":{
                "remote":null,
                "cache":true,
                "downloaded":false,
                "time":"2018-03-28T08:39:41.379354",
                "error":null,
                "id":"zlib/1.2.11@conan/stable"
             }
          }
       ],
       "error":false
    }
