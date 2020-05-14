.. _json_generator:

json
====

A file named *conanbuildinfo.json* will be generated. It will contain the information about every dependency and the installed settings and options:

.. code-block:: json

    {
      "deps_env_info": {
        "MY_ENV_VAR": "foo"
      }, 
      "deps_user_info": {
        "Hello": {
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
          "name": "Poco",
          "version": "1.7.8p3",
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



The generated ``conanbuildinfo.json`` file is a json file with the following keys:

dependencies
-------------

The dependencies is a list, with each item belonging to one dependency, and each one with the following keys:
- name
- version
- description
- rootpath
- sysroot
- include_paths, lib_paths, bin_paths, build_paths, res_paths
- libs
- defines, cflags, cppflags, sharedlinkflags, exelinkflags

Please note it is an ordered list, not a map, and dependency order is relevant. Upstream dependencies, i.e. the
ones that do not depend on other packages, will be first, and their direct dependencies after them, and so on.


deps_env_info
-------------

The environment variables defined by upstream dependencies

deps_user_info
--------------

The user variables defined by upstream dependencies

settings
--------

The settings used during `conan install`

options
-------

The options of each dependency
