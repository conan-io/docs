.. _scons_generator:

scons
=====

Conan provides :ref:`integration with SCons <scons>` with this generator.

The generated ``SConscript_conan`` will generate several dictionaries, like:

.. code-block:: python

    "conan" : {
        "CPPPATH"     : ['/path/to/include'],
        "LIBPATH"     : ['/path/to/lib'],
        "BINPATH"     : ['/path/to/bin'],
        "LIBS"        : ['hello'],
        "CPPDEFINES"  : [],
        "CXXFLAGS"    : [],
        "CCFLAGS"     : [],
        "SHLINKFLAGS" : [],
        "LINKFLAGS"   : [],
    },

    "hello" : {
        "CPPPATH"     : ['/path/to/include'],
        "LIBPATH"     : ['/path/to/lib'],
        "BINPATH"     : ['/path/to/bin'],
        "LIBS"        : ['hello'],
        "CPPDEFINES"  : [],
        "CXXFLAGS"    : [],
        "CCFLAGS"     : [],
        "SHLINKFLAGS" : [],
        "LINKFLAGS"   : [],
    },

The ``conan`` dictionary will contain the aggregated values for all dependencies, while the individual ``"hello"`` dictionaries, one per
package, will contain just the values for that specific dependency.

These dictionaries can be directly loaded into the environment like:

.. code-block:: python

    conan = SConscript('{}/SConscript_conan'.format(build_path_relative_to_sconstruct))
    env.MergeFlags(conan['conan'])
