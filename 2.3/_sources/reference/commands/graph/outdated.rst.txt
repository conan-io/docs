.. _reference_graph_outdated:

conan graph outdated
====================

.. autocommand::
    :command: conan graph outdated -h


The ``conan graph outdated`` command provides details on libraries for which a newer version is available in a remote
repository. This command helps users in identifying outdated libraries by displaying the latest version available in
the remote repository and indicating which specific remote repository it was found in. Additionally, it presents
information on the versions currently stored in the local cache and specifies the version ranges for each library.

It will display the information for every library on the dependency graph it is run on. For example if running
the command with an older version of ``libcurl`` it will display:

.. code-block:: bash

    $ conan graph outdated --requires=libcurl/[*]

.. code-block:: text

    ======== Computing dependency graph ========
    Graph root
        cli
    Requirements
        libcurl/8.5.0#95279f20d2443016907657f081a79261 - Cache
        openssl/3.2.1#edbeabd3bfc383d2cca3858aa2a78a0d - Cache
        zlib/1.3.1#f52e03ae3d251dec704634230cd806a2 - Cache
    Build requirements
        nasm/2.15.05#058c93b2214a49ca1cfe9f8f26205568 - Cache
        strawberryperl/5.32.1.1#8f83d05a60363a422f9033e52d106b47 - Cache
    Resolved version ranges
        libcurl/[*]: libcurl/8.5.0
        openssl/[>=1.1 <4]: openssl/3.2.1
        zlib/[>=1.2.11 <2]: zlib/1.3.1

    ======== Checking remotes ========
    Found 35 pkg/version recipes matching libcurl in conancenter
    Found 46 pkg/version recipes matching openssl in conancenter
    Found 6 pkg/version recipes matching zlib in conancenter
    Found 5 pkg/version recipes matching nasm in conancenter
    Found 3 pkg/version recipes matching strawberryperl in conancenter
    ======== Outdated dependencies ========
    libcurl
        Current versions:  libcurl/8.5.0
        Latest in remote(s):  libcurl/8.6.0 - conancenter
        Version ranges: libcurl/[*]
    nasm
        Current versions:  nasm/2.15.05
        Latest in remote(s):  nasm/2.16.01 - conancenter

