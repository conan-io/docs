.. _markdown_generator:

markdown
========


This generator creates a *.md* file for each requirement with useful information to consume
the installed packages: libraries available, headers, compiler flags, snippet to consume them
using different build systems,...

.. code-block:: bash

    $ conan install libxml2/2.9.9@ --generator markdown
    ...
    Generator markdown created libxml2.md


Although markdown files can be read in plain text, we highly recommend you to use any plugin
to see it with proper rendering (browsers, IDEs,.. all of them have plugins that will render
markdown documents).


.. image:: /images/conan-markdown_generator.png
    :alt: Markdown generator output for ``libxml2/2.9.9`` package.
    :width: 800 px
    :align: center

