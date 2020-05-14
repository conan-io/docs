.. _qbs_generator:

qbs
===

.. container:: out_reference_box

    This is the reference page for ``qbs`` generator.
    Go to :ref:`Integrations/Qbs<qbs>` if you want to learn how to integrate your project or recipes with Qbs.


Generates a file named ``conanbuildinfo.qbs`` that can be used for your qbs builds.

A Product ``ConanBasicSetup`` contains the aggregated requirement values and also there is N Product declared, one per
requirement.


.. code-block:: text

    import qbs 1.0

    Project {
        Product {
            name: "ConanBasicSetup"
            Export {
                Depends { name: "cpp" }
                cpp.includePaths: [{INCLUDE DIRECTORIES REQUIRE 1}, {INCLUDE DIRECTORIES REQUIRE 2}]
                cpp.libraryPaths: [{LIB DIRECTORIES REQUIRE 1}, {LIB DIRECTORIES REQUIRE 2}]
                cpp.systemIncludePaths: [{BIN DIRECTORIES REQUIRE 1}, {BIN DIRECTORIES REQUIRE 2}]
                cpp.dynamicLibraries: [{LIB NAMES REQUIRE 1}, {LIB NAMES REQUIRE 2}]
                cpp.defines: []
                cpp.cppFlags: []
                cpp.cFlags: []
                cpp.linkerFlags: []
            }
        }

        Product {
            name: "REQUIRE1"
            Export {
                Depends { name: "cpp" }
                cpp.includePaths: [{INCLUDE DIRECTORIES REQUIRE 1}]
                cpp.libraryPaths: [{LIB DIRECTORIES REQUIRE 1}]
                cpp.systemIncludePaths: [{BIN DIRECTORIES REQUIRE 1}]
                cpp.dynamicLibraries: ["{LIB NAMES REQUIRE 1}"]
                cpp.defines: []
                cpp.cppFlags: []
                cpp.cFlags: []
                cpp.linkerFlags: []
            }
        }
        // lib root path: {ROOT PATH REQUIRE 1}

        Product {
            name: "REQUIRE2"
            Export {
                Depends { name: "cpp" }
                cpp.includePaths: [{INCLUDE DIRECTORIES REQUIRE 2}]
                cpp.libraryPaths: [{LIB DIRECTORIES REQUIRE 2}]
                cpp.systemIncludePaths: [{BIN DIRECTORIES REQUIRE 2}]
                cpp.dynamicLibraries: ["{LIB NAMES REQUIRE 2}"]
                cpp.defines: []
                cpp.cppFlags: []
                cpp.cFlags: []
                cpp.linkerFlags: []
            }
        }
        // lib root path: {ROOT PATH REQUIRE 2}
    }