.. _meson_build_tool:


|meson_logo| Meson Build
________________________

If you are using **Meson Build** as your library build system, you can use the **Meson** build helper.
This helper has ``.configure()`` and ``.build()`` methods available to ease the call to Meson build system.
It also will automatically take the ``pc files`` of your dependencies when using the :ref:`pkg_config
generator<pkg_config_generator_example>`.

Check :ref:`Building with Meson Build <meson_build_reference>` for more info.



.. |meson_logo| image:: ../../images/meson.png
