Metadata
++++++++

Optional metadata, like license, description, author, etc. Not necessary for most cases, but can be useful to have.


description
-----------

This is an optional, but recommended text field, containing the description of the package,
and any information that might be useful for the consumers. The first line might be used as a
short description of the package.

.. code-block:: python

    class HelloConan(ConanFile):
        name = "hello"
        version = "0.1"
        description = """This is a Hello World library.
                        A fully featured, portable, C++ library to say Hello World in the stdout,
                        with incredible iostreams performance"""


license
-------

License of the **target** source code and binaries, i.e. the code
that is being packaged, not the ``conanfile.py`` itself.
Can contain several, comma separated licenses. It is a text string, so it can
contain any text, but it is strongly recommended that recipes of Open Source projects use
`SPDX <https://spdx.dev>`_ identifiers from the `SPDX license list <https://spdx.org/licenses/>`_


This will help people wanting to automate license compatibility checks, like consumers of your
package, or you if your package has Open-Source dependencies.

.. code-block:: python

    class Pkg(ConanFile):
        license = "MIT"


author
------
Main maintainer/responsible for the package, any format. This is an optional attribute.

.. code-block:: python

    class HelloConan(ConanFile):
        author = "John J. Smith (john.smith@company.com)"

topics
------

Tags to group related packages together and describe what the code is about.
Used as a search filter in ConanCenter. Optional attribute. It should be a tuple of strings.

.. code-block:: python

    class ProtocInstallerConan(ConanFile):
        name = "protoc_installer"
        version = "0.1"
        topics = ("protocol-buffers", "protocol-compiler", "serialization", "rpc")

homepage
--------

The home web page of the library being packaged.

Used to link the recipe to further explanations of the library itself like an overview of its features, documentation, FAQ
as well as other related information.

.. code-block:: python

    class EigenConan(ConanFile):
        name = "eigen"
        version = "3.3.4"
        homepage = "http://eigen.tuxfamily.org"


url
---

URL of the package repository, i.e. not necessarily of the original source code.
Recommended, but not mandatory attribute.

.. code-block:: python

    class HelloConan(ConanFile):
        name = "hello"
        version = "0.1"
        url = "https://github.com/conan-io/libhello.git"
