Products pipeline: single configuration
=======================================




- When the ``products pipeline`` build all necessary new binaries for all intermediate and product packages and check that every is correct, then
  these new packages can be made available for all other developers and CI jobs. This can be done with a promotion of these packages, copying
  them from the ``products`` repository to the ``develop`` repository. As the changes have been integrated and tested consistently for the main
  organization products, developers doing ``conan install`` will start seeing and using the new packages and binaries.