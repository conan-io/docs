.. _vxworks:

|vxworks_logo| VxWorks
________________________________

It's possible to cross-compile packages for `VxWorks <https://www.windriver.com/products/vxworks>`__ operating
with Conan.

Conan has support for VxWorks 7. The following architectures are supported:

- armv7

The following C++ standard library implementations are supported for QCC:

- clang++ (LLVM C++)

- g++ (GNU C++)

With a proper build VxWorks Source Build (VSB) set up on the machine, the following conan profile might be used for the cross-compiling (assuming clang in the PATH):

.. code-block:: text

  include(default)
  [settings]
  os=VxWorks
  os.version=7
  arch=armv7
  compiler=clang
  compiler.version=12
  compiler.libcxx=libstdc++11
  [options]
  [tool_requires]
  [env]

.. |vxworks_logo| image:: ../../images/conan-vxworks_logo.png
                       :width: 180px


