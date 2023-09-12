SConsDeps
=========

.. important::

   Some of the features used in this section are still **under development**, while they
   are recommended and usable and we will try not to break them in future releases, some
   breaking changes might still happen.

Available since: `1.61.0 <https://github.com/conan-io/conan/releases>`_

The ``SConsDeps`` is the dependencies generator for `SCons <https://scons.org/>`_. It will
generate a `SConscript_conandeps` file containing the necessary information for SCons to
build against the desired dependencies.

The ``SConsDeps`` generator can be used by name in conanfiles:

.. code-block:: python
   :caption: conanfile.py

   class Pkg(ConanFile):
       generators = "SConsDeps"

.. code-block:: text
   :caption: conanfile.txt

   [generators] 
   SConsDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

   from conan import ConanFile 
   from conan.tools.scons import SConsDeps

   class App(ConanFile):
       settings = "os", "arch", "compiler", "build_type"

       def generate(self):
           tc = SConsDeps(self) 
           tc.generate()


The ``SConsDeps`` generator will create after a ``conan install`` command the
`SConscript_conandeps` file. This file will provide the following information for `SCons`:
``CPPPATH``, ``LIBPATH``, ``BINPATH``, ``LIBS``, ``FRAMEWORKS``, ``FRAMEWORKPATH``,
``CPPDEFINES``, ``CXXFLAGS``, ``CCFLAGS``, ``SHLINKFLAGS``, ``LINKFLAGS`` this information
is generated for the accumulated list of all dependencies and also for each one of the
requirements. You can load it in your consumer `SConscript` like this:

.. code-block:: python
    :caption: consumer `SConscript`

    ...
    info = SConscript('./SConscript_conandeps')
    # you can use conandeps to get the information
    # for all the dependencies
    flags = info["conandeps"] 

    # or the name of the requirement if
    # you only want the information about that one
    flags = info["zlib"] 

    env.MergeFlags(flags)
    ...
