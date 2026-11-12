.. _qnx_neutrino:

|qnx_neutrino_logo| QNX Neutrino
________________________________

It's possible to cross-compile packages for `QNX Neutrino <http://blackberry.qnx.com/en/products/neutrino-rtos/neutrino-rtos>`__ operating
with Conan.

Conan has support for QNX Neutrino 6.x and 7.x. The following architectures are supported:

- armv7

- armv8

- sh4le

- ppc32be

The following C++ standard library implementations are supported for QCC:

- cxx (LLVM C++)

- gpp (GNU C++)

- cpp (Dinkum C++)

- cpp-ne (Dinkum C++ without exceptions)

- acpp (Dinkum Abridged C++)

- acpp-ne (Dinkum Abridged C++ without exceptions)

- ecpp (Dinkum Embedded C++)

- ecpp-ne (Dinkum Embedded C++ without exceptions)

Conan automatically sets up corresponding compiler flags for the given standard library (e.g. **-Y cxx** for the LLVM C++).

With `QNX SDK <http://www.qnx.com/download/>`__ set up on the machine, the following conan profile might be used for the cross-compiling (assuming **qcc** in the PATH):

.. code-block:: text

  include(default)
  [settings]
  os=Neutrino
  os.version=6.5
  arch=sh4le
  compiler=qcc
  compiler.version=4.4
  compiler.libcxx=cxx
  [options]
  [build_requires]
  [env]
  CC=qcc
  CXX=QCC

.. |qnx_neutrino_logo| image:: ../../images/conan-qnx_neutrino_logo.png
                       :width: 180px


