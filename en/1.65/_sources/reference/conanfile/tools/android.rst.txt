.. _conan_tools_android:

conan.tools.android
===================

.. important::

    Some of the features used in this section are still **under development**, while they are
    recommended and usable and we will try not to break them in future releases, some breaking
    changes might still happen if necessary to prepare for the *Conan 2.0 release*.


android_abi()
-------------

Available since: 1.59.0

This function might not be necessary when using Conan built-in integrations, as they already manage it, 
but can be useful if developing your own build system integration.

``android_abi()`` function returns the Android standard ABI name based on Conan ``settings.arch`` value, something like:

.. code-block:: python

  def android_abi(conanfile, context="host"):
    ...
    return {
          "armv5el": "armeabi",
          "armv5hf": "armeabi",
          "armv5": "armeabi",
          "armv6": "armeabi-v6",
          "armv7": "armeabi-v7a",
          "armv7hf": "armeabi-v7a",
          "armv8": "arm64-v8a",
          }.get(conanfile.settings.arch)


As it can be seen, the default is the "host" ABI, but it is possible to select also the "build" or "target" ones if necessary.

.. code-block:: python

    from conan.tools.android import android_abi

    class Pkg(ConanFile):
        def generate(self)
            abi = android_abi(self)
