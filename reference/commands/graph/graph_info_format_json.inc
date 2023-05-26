
.. warning::

  The json output of the ``conan [create|install|export-pkg|graph info] xxxx --format=json`` command is **experimental** and
  subject to change.


:command:`[create|install|export-pkg|graph info] xxx --format json` commands follow the same JSON schema. It looks like this:

.. code-block:: json
    :caption: **graph-info-schema.json (simplified)**

    {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "graph-info",
      "description": "Conan graph information",
      "type": "object",
      "properties": {
        "graph": {
            "type": "object",
            "properties": {
                "nodes": {
                  "type": "object",
                  "properties": {
                    "0": {
                      "type": "object",
                      "properties": {
                        "ref": {
                          "type": "string"
                        },
                        "id": {
                          "type": "string"
                        },
                        "recipe": {
                          "type": "string"
                        },
                        "package_id": {
                          "type": "string"
                        },
                        "prev": {
                          "type": "string"
                        },
                        "build_id": {
                          "type": "string"
                        },
                        "binary": {
                          "type": "string"
                        },
                        "invalid_build": {
                          "type": "boolean"
                        },
                        "info_invalid": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        },
                        "user": {
                          "type": "string"
                        },
                        "channel": {
                          "type": "string"
                        },
                        "url": {
                          "type": "string"
                        },
                        "license": {
                          "type": "string"
                        },
                        "author": {
                          "type": "string"
                        },
                        "description": {
                          "type": "string"
                        },
                        "homepage": {
                          "type": "string"
                        },
                        "build_policy": {
                          "type": "string"
                        },
                        "upload_policy": {
                          "type": "string"
                        },
                        "revision_mode": {
                          "type": "string"
                        },
                        "provides": {
                          "type": "string"
                        },
                        "deprecated": {
                          "type": "string"
                        },
                        "win_bash": {
                          "type": "boolean"
                        },
                        "win_bash_run": {
                          "type": "boolean"
                        },
                        "default_options": {
                          "type": "object"
                        },
                        "options_description": {
                          "type": "string"
                        },
                        "version": {
                          "type": "string"
                        },
                        "topics": {
                          "type": "array"
                        },
                        "package_type": {
                          "type": "string"
                        },
                        "settings": {
                          "type": "object",
                        },
                        "options": {
                          "type": "object",
                        },
                        "options_definitions": {
                          "type": "object"
                        },
                        "generators": {
                          "type": "array"
                        },
                        "system_requires": {
                          "type": "object"
                        },
                        "recipe_folder": {
                          "type": "string"
                        },
                        "source_folder": {
                          "type": "string"
                        },
                        "build_folder": {
                          "type": "string"
                        },
                        "generators_folder": {
                          "type": "string"
                        },
                        "package_folder": {
                          "type": "string"
                        },
                        "cpp_info": {
                          "type": "object",
                        },
                        "label": {
                          "type": "string"
                        },
                        "dependencies": {
                          "type": "object",
                        },
                        "context": {
                          "type": "string"
                        },
                        "test": {
                          "type": "boolean"
                        }
                      }
                    }
                  }
                },
                "root": {
                  "type": "object",
                },
                "overrides": {
                  "type": "object",
                },
                "resolved_ranges": {
                  "type": "object"
                }
              }
          }
       }
    }


For instance, the JSON output generated by :command:`conan graph info --require=zlib/1.2.11 -r=conancenter --format=json > graph.json`:

.. code-block:: json
    :caption: **graph.json**

    {
      "graph": {
          "nodes": {
                "0": {
                    "ref": "conanfile",
                    "id": "0",
                    "recipe": "Cli",
                    "package_id": null,
                    "prev": null,
                    "build_id": null,
                    "binary": null,
                    "invalid_build": false,
                    "info_invalid": null,
                    "name": null,
                    "user": null,
                    "channel": null,
                    "url": null,
                    "license": null,
                    "author": null,
                    "description": null,
                    "homepage": null,
                    "build_policy": null,
                    "upload_policy": null,
                    "revision_mode": "hash",
                    "provides": null,
                    "deprecated": null,
                    "win_bash": null,
                    "win_bash_run": null,
                    "default_options": null,
                    "options_description": null,
                    "version": null,
                    "topics": null,
                    "package_type": "unknown",
                    "settings": {
                        "os": "Macos",
                        "arch": "x86_64",
                        "compiler": "apple-clang",
                        "compiler.cppstd": "gnu17",
                        "compiler.libcxx": "libc++",
                        "compiler.version": "12.0",
                        "build_type": "Release"
                    },
                    "options": {},
                    "options_definitions": {},
                    "generators": [],
                    "system_requires": {},
                    "recipe_folder": null,
                    "source_folder": null,
                    "build_folder": null,
                    "generators_folder": null,
                    "package_folder": null,
                    "cpp_info": {
                        "root": {
                            "includedirs": [
                                "include"
                            ],
                            "srcdirs": null,
                            "libdirs": [
                                "lib"
                            ],
                            "resdirs": null,
                            "bindirs": [
                                "bin"
                            ],
                            "builddirs": null,
                            "frameworkdirs": null,
                            "system_libs": null,
                            "frameworks": null,
                            "libs": null,
                            "defines": null,
                            "cflags": null,
                            "cxxflags": null,
                            "sharedlinkflags": null,
                            "exelinkflags": null,
                            "objects": null,
                            "sysroot": null,
                            "requires": null,
                            "properties": null
                        }
                    },
                    "label": "cli",
                    "dependencies": {
                        "1": {
                            "ref": "zlib/1.2.11",
                            "run": "False",
                            "libs": "True",
                            "skip": "False",
                            "test": "False",
                            "force": "False",
                            "direct": "True",
                            "build": "False",
                            "transitive_headers": "None",
                            "transitive_libs": "None",
                            "headers": "True",
                            "package_id_mode": "None",
                            "visible": "True"
                        }
                    },
                    "context": "host",
                    "test": false
                },
                "1": {
                    "ref": "zlib/1.2.11#ffa77daf83a57094149707928bdce823",
                    "id": "1",
                    "recipe": "Cache",
                    "package_id": "d0599452a426a161e02a297c6e0c5070f99b4909",
                    "prev": null,
                    "build_id": null,
                    "binary": "Missing",
                    "invalid_build": false,
                    "info_invalid": null,
                    "name": "zlib",
                    "user": null,
                    "channel": null,
                    "url": "https://github.com/conan-io/conan-center-index",
                    "license": "Zlib",
                    "author": null,
                    "description": "A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)",
                    "homepage": "https://zlib.net",
                    "build_policy": null,
                    "upload_policy": null,
                    "revision_mode": "hash",
                    "provides": null,
                    "deprecated": null,
                    "win_bash": null,
                    "win_bash_run": null,
                    "default_options": {
                        "shared": false,
                        "fPIC": true
                    },
                    "options_description": null,
                    "version": "1.2.11",
                    "topics": [
                        "zlib",
                        "compression"
                    ],
                    "package_type": "static-library",
                    "settings": {
                        "os": "Macos",
                        "arch": "x86_64",
                        "compiler": "apple-clang",
                        "compiler.version": "12.0",
                        "build_type": "Release"
                    },
                    "options": {
                        "fPIC": "True",
                        "shared": "False"
                    },
                    "options_definitions": {
                        "shared": [
                            "True",
                            "False"
                        ],
                        "fPIC": [
                            "True",
                            "False"
                        ]
                    },
                    "generators": [],
                    "system_requires": {},
                    "recipe_folder": "/Users/franchuti/.conan2/p/zlib774aa77541f8b/e",
                    "source_folder": null,
                    "build_folder": null,
                    "generators_folder": null,
                    "package_folder": null,
                    "cpp_info": {
                        "root": {
                            "includedirs": [
                                "include"
                            ],
                            "srcdirs": null,
                            "libdirs": [
                                "lib"
                            ],
                            "resdirs": null,
                            "bindirs": [
                                "bin"
                            ],
                            "builddirs": null,
                            "frameworkdirs": null,
                            "system_libs": null,
                            "frameworks": null,
                            "libs": null,
                            "defines": null,
                            "cflags": null,
                            "cxxflags": null,
                            "sharedlinkflags": null,
                            "exelinkflags": null,
                            "objects": null,
                            "sysroot": null,
                            "requires": null,
                            "properties": null
                        }
                    },
                    "label": "zlib/1.2.11",
                    "dependencies": {},
                    "context": "host",
                    "test": false
                }
            },
            "root": {
                "0": "None"
            },
            "overrides": {},
            "resolved_ranges": {}
        }
    }
