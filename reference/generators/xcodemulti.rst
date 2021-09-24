.. _xcode_multi_generator:

xcode_multi
===========

.. container:: out_reference_box

    This is the reference page for ``xcode_multi`` generator.
    Go to :ref:`Integrations/Xcode<xcode>` if you want to learn how to integrate your project or recipes with Xcode.

The ``xcode`` generator creates a file named *conanbuildinfo_multi.xcconfig* that can be imported to your Xcode project.
In addition it generates a *conanbuildinfo_<arch>.xcconfig* file for each generated architecture.

The architecture specific files declare these variables with a conditional statement defining the architecture:

+--------------------------------+---------------------------------------------------------------------------+
| VARIABLE                       | VALUE                                                                     |
+================================+===========================================================================+
| HEADER_SEARCH_PATHS            | The requirements `include dirs`                                           |
+--------------------------------+---------------------------------------------------------------------------+
| LIBRARY_SEARCH_PATHS           | The requirements `lib dirs`                                               |
+--------------------------------+---------------------------------------------------------------------------+
| OTHER_LDFLAGS                  | `-lXXX` corresponding to library and system library names                 |
+--------------------------------+---------------------------------------------------------------------------+
| GCC_PREPROCESSOR_DEFINITIONS   | The requirements definitions                                              |
+--------------------------------+---------------------------------------------------------------------------+
| OTHER_CFLAGS                   | The requirements cflags                                                   |
+--------------------------------+---------------------------------------------------------------------------+
| OTHER_CPLUSPLUSFLAGS           | The requirements cxxflags                                                 |
+--------------------------------+---------------------------------------------------------------------------+
| FRAMEWORK_SEARCH_PATHS         | The requirements framework folders, so xcode can find packaged frameworks |
+--------------------------------+---------------------------------------------------------------------------+

Usage
-----
Run `conan install` with a profile for each architecture. This will generate the architecture
specific project files and add an include entry for each architecture in *conanbuildinfo_multi.xcconfig*