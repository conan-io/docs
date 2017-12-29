
.. _gcc_generator:

gcc
===

.. container:: out_reference_box

    This is the reference page for ``gcc`` generator.
    Go to :ref:`Integrations/GCC / Clang<gcc_integration>` if you want to learn how to integrate your project or recipes with ``gcc`` or ``clang`` compilers.



Generates a file named ``conanbuildinfo.gcc`` containing a command line parameters to invoke ``gcc`` or ``clang``
compilers.

.. code-block:: bash

    > g++ timer.cpp @conanbuildinfo.gcc -o bin/timer

+--------------------------------+----------------------------------------------------------------------+
| OPTION                         | VALUE                                                                |
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
| Other flags                    | cppflags, cflags, sharedlinkflags, exelinkflags (applied directly)   |
+--------------------------------+----------------------------------------------------------------------+



You could use the **gcc** generator directly to build your source code.
It's valid to invoke both gcc and clang compilers.


.. code-block:: python
   :emphasize-lines: 15

   from conans import ConanFile

   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.8p3@pocoproject/stable"
      generators = "gcc"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"

      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

      def build(self):
         self.run("mkdir -p bin")
         command = 'g++ timer.cpp @conanbuildinfo.gcc -o bin/timer'
         self.run(command)