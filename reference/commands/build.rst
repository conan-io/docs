
conan build
===========


.. code-block:: bash

	$ conan build [-h] [--file FILE] [path]

Utility command to run your current project **conanfile.py** ``build()`` method. It doesn't
work for **conanfile.txt**. It is convenient for automatic translation of conan settings and options,
for example to CMake syntax, as it can be done by the CMake helper. It is also a good starting point
if you would like to create a package from your current project.



.. code-block:: bash

    positional arguments:
      path                  path to conanfile.py, e.g., conan build .

    optional arguments:
      -h, --help            show this help message and exit
      --file FILE, -f FILE  specify conanfile filename



The ``conan build`` and the ``build()`` method might use dependencies information, either from
``cpp_info`` or from ``env_info``. That information is saved in the ``conan install`` step if
using the ``txt`` generator in the ``conanbuildinfo.txt``.
So, if the ``conan build`` command is to be used, the recommended way to run install would be:

.. code-block:: bash

    $ conan install .. -g txt

or adding ``txt`` generator to the consuming conanfile ``generators`` section

