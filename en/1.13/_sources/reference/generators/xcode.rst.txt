.. _xcode_generator:

xcode
=====

.. container:: out_reference_box

    This is the reference page for ``xcode`` generator.
    Go to :ref:`Integrations/Xcode<xcode>` if you want to learn how to integrate your project or recipes with Xcode.




The **xcode** generator creates a file named ``conanbuildinfo.xcconfig`` that can be imported to your *Xcode* project.

The file declare these variables:

+--------------------------------+----------------------------------------------------------------------+
| VARIABLE                       | VALUE                                                                |
+================================+======================================================================+
| HEADER_SEARCH_PATHS            | The requirements `include dirs`                                      |
+--------------------------------+----------------------------------------------------------------------+
| LIBRARY_SEARCH_PATHS           | The requirements `lib dirs`                                          |
+--------------------------------+----------------------------------------------------------------------+
| OTHER_LDFLAGS                  | `-lXXX` corresponding to library names                               |
+--------------------------------+----------------------------------------------------------------------+
| GCC_PREPROCESSOR_DEFINITIONS   | The requirements definitions                                         |
+--------------------------------+----------------------------------------------------------------------+
| OTHER_CFLAGS                   | The requirements cflags                                              |
+--------------------------------+----------------------------------------------------------------------+
| OTHER_CPLUSPLUSFLAGS           | The requirements cxxflags                                            |
+--------------------------------+----------------------------------------------------------------------+
| FRAMEWORK_SEARCH_PATHS         | The requirements root folders, so xcode can find packaged frameworks |
+--------------------------------+----------------------------------------------------------------------+
