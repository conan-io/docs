.. _json_generator:

json
====

.. warning::

    Actual JSON may have more fields not documented here. Those fields may change in the future
    without previous warning.

A file named *conanbuildinfo.json* will be generated. It will contain the information about
every dependency and the installed settings and options:

.. code-block:: json

    {
      "deps_env_info": {
        "MY_ENV_VAR": "foo"
      },
      "deps_user_info": {
        "hello": {
          "my_var": "my_value"
        }
      },
      "dependencies":
      [
        {
          "name": "fmt",
          "version": "4.1.0",
          "include_paths": [
            "/path/to/.conan/data/fmt/4.1.0/<user>/<channel>/package/<id>/include"
          ],
          "lib_paths": [
            "/path/to/.conan/data/fmt/4.1.0/<user>/<channel>/package/<id>/lib"
          ],
          "libs": [
            "fmt"
          ],
          "...": "...",
        },
        {
          "name": "poco",
          "version": "1.9.4",
          "...": "..."
        }
      ],
      "settings": {
        "os": "Linux",
        "arch": "armv7"
      },
      "options": {
        "curl": {
          "shared": true,
        }
      }
    }

The generated *conanbuildinfo.json* file is a JSON file with the following keys:

dependencies
-------------

The dependencies is a list, with each item belonging to one dependency, and each one with the following keys:

 - ``name``
 - ``version``
 - ``description``
 - ``rootpath``
 - ``sysroot``
 - ``include_paths``, ``lib_paths``, ``bin_paths``, ``build_paths``, ``res_paths``, ``framework_paths``
 - ``libs``, ``frameworks``, ``system_libs``
 - ``defines``, ``cflags``, ``cppflags``, ``sharedlinkflags``, ``exelinkflags``
 - ``configs`` (only for multi config dependencies, see below)

Please note that the dependencies are ordered, it isn't a map, order is relevant. Upstream dependencies, i.e. the
ones that do not depend on other packages, will be first, and their direct dependencies after them, and so on.

The node ``configs`` will appear only for :ref:`multi config recipes<packaging_approach_N_1>`,
it is holding a dictionary with the data related to each configuration:

.. code-block:: json

    {
    "...": "...",
    "dependencies": [
        {
            "name": "hello",
            "rootpath": "/private/var/folders/yq/14hmvxm96xd7gfgl37_tnrbh0000gn/T/tmpkp9l_dovconans/path with spaces/.conan/data/hello/0.1/lasote/testing/package/46f53f156846659bf39ad6675fa0ee8156e859fe",
            "...": "...",
            "configs": {
                "debug": {
                    "libs": ["hello_d"]
                },
                "release": {
                    "libs": ["hello"]
                }
            }
        },
        {
            "...": "..."
        }
        ]
    }

deps_env_info
-------------

The environment variables defined by upstream dependencies.

deps_user_info
--------------

The user variables defined by upstream dependencies.

settings
--------

The settings used during :command:`conan install`.

options
-------

The options of each dependency.
