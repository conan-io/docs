conan graph
===========


The ``conan graph`` command contains several subcommands that return information of a dependency graph
without needing to download the package binaries.

.. toctree::
   :maxdepth: 1

   conan graph info: Computes a dependency graph and displays information about it <graph/info>
   conan graph build-order: Computes the detailed sequence of packages that need to be built from source <graph/build_order>
   conan graph build-order-merge: Merge 2 existing build-order sequences into one <graph/build_order_merge>
   conan graph explain: Explain what is wrong with the dependency graph, showing missing binaries, closest alternatives, and why they do not match <graph/explain>
