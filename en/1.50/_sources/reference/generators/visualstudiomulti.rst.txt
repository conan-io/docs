.. _visual_studio_multi:


visual_studio_multi
===================

.. container:: out_reference_box

    This is the reference page for ``visual_studio_multi`` generator.
    Go to :ref:`Integrations/Visual Studio<visual_studio>` if you want to learn how to integrate your project or recipes with Visual Studio.

Usage
-----

.. code-block:: bash

    $ conan install . -g visual_studio_multi -s arch=x86 -s build_type=Debug
    $ conan install . -g visual_studio_multi -s arch=x86_64 -s build_type=Debug
    $ conan install . -g visual_studio_multi -s arch=x86 -s build_type=Release
    $ conan install . -g visual_studio_multi -s arch=x86_64 -s build_type=Release

These commands will generate 5 files for each compiler version:

- *conanbuildinfo_multi.props*: All properties
- *conanbuildinfo_release_x64_v141.props.props*: Variables for release/64bits/VS2015 (toolset v141).
- *conanbuildinfo_debug_x64_v141.props.props*: Variables for debug/64bits/VS2015 (toolset v141).
- *conanbuildinfo_release_win32_v141.props.props*: Variables for release/32bits/VS2015 (toolset v141).
- *conanbuildinfo_debug_win32_v141.props.props*: Variables for debug/32bits/VS2015 (toolset v141).

You can now load *conanbuildinfo_multi.props* in your Visual Studio IDE property manager, and all configurations will be loaded at once.

Each one of the configurations will have the format and information defined in :ref:`the visual_studio generator<visualstudio_generator>`.
