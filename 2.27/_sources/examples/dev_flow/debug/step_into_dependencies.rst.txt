
.. _examples_dev_flow_debug_step_into:


Debugging and stepping into dependencies 
========================================

Sometimes, when developing and debugging your own code, it could be useful to be able to step-into the
dependencies source code too. There are a couple of things to take into account:

- Recipes and packages from ConanCenter do not package always all the debug artifacts necessary to debug. For example in Windows, the ``*.pdb`` files are not packaged, because they are very heavy, and in practice barely used. It is possible to have your own packages to package the PDB files if you want, but that still won't solve the next point.
- Debug artifacts are often not relocatable, that means that such artifacts can only be used in the location they were built from sources. But packages that are uploaded to a server and downloaded to a different machine can put those artifacts in a different folder. Then, the debug artifacts might not correctly locate the source code, the symbols, etc.


Building from source
--------------------

The recommended approach for debugging dependencies is building them from source in the local cache. This approach should work out of the box for most recipes, including ConanCenter recipes. 

We can reuse the code from the very first example in the tutorial for this use case. Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/consuming_packages/simple_cmake_project

Then, lets make sure the dependency is built from source:

.. code-block:: bash

    $ conan install . -s build_type=Debug --build="zlib/*"
    ...
    Install finished successfully

Assuming that we have CMake>=3.23, we can use the presets (otherwise, please use the ``-DCMAKE_TOOLCHAIN_FILE`` arguments):

.. code-block:: bash

    $ cmake . --preset conan-default


This will create our project, that we can start building and debugging.


Step into a dependency with Visual Studio
-----------------------------------------

Once the project is created, in Visual Studio, we can double-click on the ``compressor.sln`` file, or open the file from the open Visual Studio IDE.

Once the project is open, the first step is building it, making sure the ``Debug`` configuration is the active one, going to ``Build -> Build Solution`` will do it. Then we can define ``compressor`` as the "Startup project" in project view.

Going to the ``compressor/main.c`` source file, we can introduce a breakpoint in some line there:

.. code-block:: c++
    :caption: main.c

    int main(void) {
        ...

        // add a breakpoint in deflateInit line in your IDE
        deflateInit(&defstream, Z_BEST_COMPRESSION);
        deflate(&defstream, Z_FINISH);

Clicking on the ``Debug -> Start Debugging`` (or F5), the program will start debugging and stop at the ``deflateInit()`` line. Clicking on the ``Debug -> Step Into``, the IDE should be able to navigate to the ``deflate.c`` source code. If we check this file, its path will be inside the Conan cache, like ``C:\Users\<myuser>\.conan2\p\b\zlib4f7275ba0a71f\b\src\deflate.c``

.. code-block:: c++
   :caption: deflate.c

   int ZEXPORT deflateInit_(strm, level, version, stream_size)
    z_streamp strm;
    int level;
    const char *version;
    int stream_size;
    {
        return deflateInit2_(strm, level, Z_DEFLATED, MAX_WBITS, DEF_MEM_LEVEL,
                            Z_DEFAULT_STRATEGY, version, stream_size);
        /* To do: ignore strm->next_in if we use it as window */
    }


.. seealso::

    - Modifying the dependency source code while debugging is not possible with this approach. If that is the intended flow, the recommended approach is to use :ref:`editable package<editable_packages>`.
