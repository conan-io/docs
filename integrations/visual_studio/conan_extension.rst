|visual_logo| Conan Extension for Visual Studio
===============================================

Thanks to the invaluable help of our community we manage to develop and maintain a free
extension for Visual Studio in the Microsoft Marketplace, it is called `Conan Extension
for Visual Studio <https://marketplace.visualstudio.com/items?itemName=conan-io.conan-vs-extension>`_
and it provides integration with Conan using the
Visual Studio generators.

.. image:: ../../images/visual_studio/conan-marketplace-header.png
   :width: 90%
   :alt: Conan Extension for Visual Studio in the Microsoft marketplace

You can install it into your IDE using the **Extensions manager** and start using it right
away. This extension will look for a *conanfile.py* (or *conanfile.txt*) and retrieve the
requirements declared in it that match your build configuration (it will build them from
sources if no binaries are available).

.. note::

    **Location of the conanfile**

    In version ``1.0`` of the extension, the algorithm to look for the *conanfile.py* (preferred)
    or *conanfile.txt* is very naive: It will start looking for those files in the directory
    where the **Visual Studio project file** is located and then it will walk recursively into
    parent directories looking for them.

The extension creates a property sheet file and adds it to the project, so all the
information from the dependencies handled by Conan should be added (as inherited properties)
to those already available in your projects.

At this moment (release ``v1.0.x``) the extension is under heavy development, some behaviors may
change and new features will be added. You can subscribe to `its repository`_ to stay updated and,
of course, any feedback about it will be more than welcome.

.. |visual_logo| image:: ../../images/conan-visual-studio-logo.png
.. _`its repository`: https://github.com/conan-io/conan-vs-extension
