
.. _search_json:


Search output
-------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The :command:`conan search` provides a :command:`--json` parameter to generate a file containing the
information of the search process.

The output JSON contains a two first level keys:

  - **error**: ``True`` if the upload completed without error, ``False`` otherwise.
  - **results**: A list of the remotes with the packages found. Each element contains:

     - **remote**: Name of the remote.
     - **items**: List of the items found in that remote. For each item there will always be a
                  recipe and optionally also packages when searching them.

        - **recipe**: Document representing the uploaded recipe.
            - **id**: Reference, e.g., "OpenSSL/1.0.2n@conan/stable"

        - **packages**: List of elements representing the binary packages found for the recipe.
            - **id**: Package ID, e.g., "8018a4df6e7d2b4630a814fa40c81b85b9182d2b"
            - **options**: Dictionary of options of the package.
            - **settings**: Dictionary with settings of the package.
            - **requires**: List of requires of the package.
            - **outdated**: Boolean to show whether package is outdated from recipe or not.

**Examples:**

- Search references in all remotes: :command:`conan search eigen* -r all`

  .. code-block:: json

      {
          "error":false,
          "results":[
              {  
                  "remote":"conan-center",
                  "items":[
                      {
                          "recipe":{
                              "id":"eigen/3.3.4@conan/stable"
                          }
                      }
                  ]
              },
              {
                  "remote":"upload_repo",
                  "items":[
                      {
                          "recipe":{
                              "id":"eigen/3.3.4@danimtb/stable"
                          }
                      },
                      {
                          "recipe":{
                              "id":"eigen/3.3.4@danimtb/testing"
                          }
                      }
                  ]
              },
              {  
                  "remote":"conan-community",
                  "items":[
                      {
                          "recipe":{
                              "id":"eigen/3.3.4@conan/stable"
                          }
                      }
                  ]
              }
          ]
      }

- Search packages of a reference in a remote: :command:`conan search paho-c/1.2.0@conan/stable -r conan-center --json search.json`

  .. code-block:: json

      {
          "error":false,
          "results":[
              {
                  "remote":"conan-center",
                  "items":[
                      {
                          "recipe":{
                              "id":"paho-c/1.2.0@conan/stable"
                          },
                          "packages":[
                              {
                                  "id":"0000193ac313953e78a4f8e82528100030ca70ee",
                                  "options":{
                                      "shared":"False",
                                      "asynchronous":"False",
                                      "SSL":"False"
                                  },
                                  "settings":{
                                      "os":"Linux",
                                      "arch":"x86_64",
                                      "compiler":"gcc",
                                      "build_type":"Debug",
                                      "compiler.version":"4.9"
                                  },
                                  "requires":[

                                  ],
                                  "outdated":false
                              },
                              {
                                  "id":"014be746b283391f79d11e4e8af3154344b58223",
                                  "options":{
                                      "shared":"False",
                                      "asynchronous":"False",
                                      "SSL":"False"
                                  },
                                  "settings":{
                                      "os":"Windows",
                                      "compiler.threads":"posix",
                                      "compiler.exception":"seh",
                                      "arch":"x86_64",
                                      "compiler":"gcc",
                                      "build_type":"Debug",
                                      "compiler.version":"5"
                                  },
                                  "requires":[

                                  ],
                                  "outdated":false
                              },
                              {
                                "id":"0188020dbfd167611b967ad2fa0e30710d23e920",
                                  "options":{
                                      "shared":"True",
                                      "asynchronous":"False",
                                      "SSL":"False"
                                  },
                                  "settings":{
                                      "os":"Macos",
                                      "arch":"x86_64",
                                      "compiler":"apple-clang",
                                      "build_type":"Debug",
                                      "compiler.version":"9.1"
                                  },
                                  "requires":[

                                  ],
                                  "outdated":false
                              },
                              {
                                  "id":"03369b0caf8c0c8d4bb84d5136112596bde4652d",
                                  "options":{
                                      "shared":"True",
                                      "asynchronous":"False",
                                      "SSL":"False"
                                  },
                                  "settings":{
                                      "os":"Linux",
                                      "arch":"x86",
                                      "compiler":"gcc",
                                      "build_type":"Release",
                                      "compiler.version":"5"
                                  },
                                  "requires":[

                                  ],
                                  "outdated":false
                              }
                          ]
                      }
                  ]
              }
          ]
      }

- Search references in local cache: :command:`conan search paho-c* --json search.json`

  .. code-block:: json

      {
          "error":false,
          "results":[
              {
                  "remote":"None",
                  "items":[
                      {
                          "recipe":{
                              "id":"paho-c/1.2.0@danimtb/testing"
                          }
                      }
                  ]
              }
          ]
      }

- Search packages of a reference in local cache: :command:`conan search paho-c/1.2.0@danimtb/testing --json search.json`

  .. code-block:: json

      {
          "error":false,
          "results":[
              {
                  "remote":"None",
                  "items":[
                      {
                          "recipe":{
                              "id":"paho-c/1.2.0@danimtb/testing"
                          },
                            "packages":[
                              {
                                  "id":"6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7",
                                  "options":{
                                      "SSL":"False",
                                      "asynchronous":"False",
                                      "shared":"False"
                                  },
                                  "settings":{
                                      "arch":"x86_64",
                                      "build_type":"Release",
                                      "compiler":"Visual Studio",
                                      "compiler.runtime":"MD",
                                      "compiler.version":"15",
                                      "os":"Windows"
                                  },
                                  "requires":[

                                  ],
                                  "outdated":false
                                },
                                {
                                  "id":"95cd13dfc3f6b80d3ccb2a38441e3a1ad88e5a15",
                                  "options":{
                                      "SSL":"False",
                                      "asynchronous":"True",
                                      "shared":"True"
                                  },
                                  "settings":{
                                      "arch":"x86_64",
                                      "build_type":"Release",
                                      "compiler":"Visual Studio",
                                      "compiler.runtime":"MD",
                                      "compiler.version":"15",
                                      "os":"Windows"
                                  },
                                  "requires":[

                                  ],
                                  "outdated":true
                              },
                              {
                                  "id":"970e773c5651dc2560f86200a4ea56c23f568ff9",
                                  "options":{
                                      "SSL":"False",
                                      "asynchronous":"False",
                                      "shared":"True"
                                  },
                                  "settings":{
                                      "arch":"x86_64",
                                      "build_type":"Release",
                                      "compiler":"Visual Studio",
                                      "compiler.runtime":"MD",
                                      "compiler.version":"15",
                                      "os":"Windows"
                                  },
                                  "requires":[

                                  ],
                                  "outdated":true
                              },
                              {
                                  "id":"c4c0a49b09575515ce1dd9841a48de0c508b9d7c",
                                  "options":{
                                      "SSL":"True",
                                      "asynchronous":"False",
                                      "shared":"True"
                                  },
                                  "settings":{
                                      "arch":"x86_64",
                                      "build_type":"Release",
                                      "compiler":"Visual Studio",
                                      "compiler.runtime":"MD",
                                      "compiler.version":"15",
                                      "os":"Windows"
                                  },
                                  "requires":[
                                      "OpenSSL/1.0.2n@conan/stable:606fdb601e335c2001bdf31d478826b644747077",
                                      "zlib/1.2.11@conan/stable:6cc50b139b9c3d27b3e9042d5f5372d327b3a9f7"
                                  ],
                                  "outdated":true
                              },
                              {
                                  "id":"db9d6ba7004592ed2598f2c369484d4a01269110",
                                  "options":{
                                      "SSL":"True",
                                      "asynchronous":"False",
                                      "shared":"True"
                                  },
                                  "settings":{
                                      "arch":"x86_64",
                                      "build_type":"Release",
                                      "compiler":"gcc",
                                      "compiler.exception":"seh",
                                      "compiler.threads":"posix",
                                      "compiler.version":"7",
                                      "os":"Windows"
                                  },
                                  "requires":[
                                      "OpenSSL/1.0.2n@conan/stable:f761d91cef7988eafb88c6b6179f4cf261609f26",
                                      "zlib/1.2.11@conan/stable:6dc82da13f94df549e60f9c1ce4c5d11285a4dff"
                                  ],
                                  "outdated":true
                              }
                          ]
                      }
                  ]
              }
          ]
      }
