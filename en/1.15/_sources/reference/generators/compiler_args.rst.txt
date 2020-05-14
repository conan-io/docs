.. spelling::

  Wl
  Zi


.. _compiler_args_generator:

compiler_args
=============

.. container:: out_reference_box

    This is the reference page for ``compiler_args`` generator.
    Go to :ref:`Integrations/Compilers on command line<gcc_integration>` if you want to learn how to integrate your project calling
    your compiler in the command line.



Generates a file named ``conanbuildinfo.args`` containing a command line parameters to invoke ``gcc``, ``clang`` or ``cl`` compiler.

You can use the **compiler_args** generator directly to build simple programs:


**gcc/clang**:

.. code-block:: bash

    > g++ timer.cpp @conanbuildinfo.args -o bin/timer


**cl**:

.. code-block:: bash

    $ cl /EHsc timer.cpp @conanbuildinfo.args



**gcc/clang**

+--------------------------------+----------------------------------------------------------------------+
| FLAG                           | MEANING                                                              |
+================================+======================================================================+
| -DXXX                          | Corresponding to requirements `defines`                              |
+--------------------------------+----------------------------------------------------------------------+
| -IXXX                          | Corresponding to requirements `include dirs`                         |
+--------------------------------+----------------------------------------------------------------------+
| -Wl,-rpathXXX                  | Corresponding to requirements `lib dirs`                             |
+--------------------------------+----------------------------------------------------------------------+
| -LXXX                          | Corresponding to requirements `lib dirs`                             |
+--------------------------------+----------------------------------------------------------------------+
| -lXXX                          | Corresponding to requirements `libs`                                 |
+--------------------------------+----------------------------------------------------------------------+
| -m64                           | For x86_64 architecture                                              |
+--------------------------------+----------------------------------------------------------------------+
| -m32                           | For x86 architecture                                                 |
+--------------------------------+----------------------------------------------------------------------+
| -DNDEBUG                       | For Release builds                                                   |
+--------------------------------+----------------------------------------------------------------------+
| -s                             | For Release builds (only gcc)                                        |
+--------------------------------+----------------------------------------------------------------------+
| -g                             | For Debug builds                                                     |
+--------------------------------+----------------------------------------------------------------------+
| -D_GLIBCXX_USE_CXX11_ABI=0     | When setting libcxx == "libstdc++"                                   |
+--------------------------------+----------------------------------------------------------------------+
| -D_GLIBCXX_USE_CXX11_ABI=1     | When setting libcxx == "libstdc++11"                                 |
+--------------------------------+----------------------------------------------------------------------+
| Other flags                    | cxxflags, cflags, sharedlinkflags, exelinkflags (applied directly)   |
+--------------------------------+----------------------------------------------------------------------+


**cl (Visual Studio)**

+--------------------------------+----------------------------------------------------------------------+
| FLAG                           | MEANING                                                              |
+================================+======================================================================+
| /DXXX                          | Corresponding to requirements `defines`                              |
+--------------------------------+----------------------------------------------------------------------+
| /IXXX                          | Corresponding to requirements `include dirs`                         |
+--------------------------------+----------------------------------------------------------------------+
| /LIBPATH:XX                    | Corresponding to requirements `lib dirs`                             |
+--------------------------------+----------------------------------------------------------------------+
| /MT, /MTd, /MD, /MDd           | Corresponding to Runtime                                             |
+--------------------------------+----------------------------------------------------------------------+
| -DNDEBUG                       | For Release builds                                                   |
+--------------------------------+----------------------------------------------------------------------+
| /Zi                            | For Debug builds                                                     |
+--------------------------------+----------------------------------------------------------------------+



You can also use it in a recipe:


.. code-block:: python
   :emphasize-lines: 15

   from conans import ConanFile

   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.9.0@pocoproject/stable"
      generators = "compiler_args"
      default_options = {"Poco:shared": True, "OpenSSL:shared": True}

      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

      def build(self):
         self.run("mkdir -p bin")
         command = 'g++ timer.cpp @conanbuildinfo.args -o bin/timer'
         self.run(command)
