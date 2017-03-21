.. _conanfile_txt_reference:

conanfile.txt
=============

Sections
--------

[requires]
__________

List of requirements, specifing the full reference.


.. code-block:: text

    [requires]
    Poco/1.7.3@lasote/stable
    zlib/1.2.8@lasote/stable


Also support :ref:`version ranges<version_ranges>`:


.. code-block:: text

    [requires]
    Poco/[>1.0,<1.8]@lasote/stable
    zlib/1.2.8@lasote/stable



[generators]
____________

List of :ref:`generators<generators_reference>`


.. code-block:: text

    [requires]
    Poco/1.7.3@lasote/stable
    zlib/1.2.8@lasote/stable

    [generators]
    xcode
    cmake
    qmake


[options]
_________


List of :ref:`options<options_txt>`. Always specifying **package_name:option = Value**


.. code-block:: text

    [requires]
    Poco/1.7.3@lasote/stable
    zlib/1.2.8@lasote/stable

    [generators]
    cmake

    [options]
    Poco:shared=True
    OpenSSL:shared=True


[imports]
_________

List of files to be imported to a local directory. Read more: :ref:`imports<imports_txt>`.


.. code-block:: text

    [requires]
    Poco/1.7.3@lasote/stable
    zlib/1.2.8@lasote/stable

    [generators]
    cmake

    [options]
    Poco:shared=True
    OpenSSL:shared=True

    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my "bin" folder

