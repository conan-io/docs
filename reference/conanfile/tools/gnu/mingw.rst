.. _conan_tools_gnu_mingw:

conan.tools.gnu.is_mingw()
--------------------------

Available since: `1.56.0 <https://github.com/conan-io/conan/releases/tag/1.56.0>`_

.. code-block:: python

    def is_mingw(conanfile):

Check whether ``self.settings`` is a MinGW compiler.
It returns ``True`` when host os is ``Windows`` and host compiler is ``gcc`` or ``clang``
and ``compiler.runtime`` is not set, otherwise returns ``False``.
When the ``compiler`` is empty, it returns ``False``.

Parameters:

- **conanfile**: ConanFile instance.

.. code-block:: python

    from conan.tools.gnu import is_mingw

    def build(self):
        if is_mingw(self):
            # some logic to build with mingw
