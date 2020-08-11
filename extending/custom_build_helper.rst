.. _custom_build_helper:

Creating a custom build helper for Conan
----------------------------------------

If Conan doesn't have a build helper for the build tool you are using, you can create a custom build helper
with the :ref:`python_requires`. You can create a package defining the build helper for that
build tool and reuse it later in the consumers importing the build helper as a
*Python requires*. 

As you probably know, build helpers are wrappers of the build tool that help with the conversion
of the Conan settings to the build tool’s ones. They assist users with the compilation of libraries
and applications in the `build()` method of a recipe.

As an example, we are going to create a minimal implementation of a build helper for the `Waf build
system <https://waf.io/>`_ . First, we need to create a recipe for the ``python_requires`` that will
export *waf_environment.py*, where all the implementation of the build helper is.

.. code-block:: python
    
    from conans import ConanFile
    from waf_environment import WafBuildEnvironment


    class PythonRequires(ConanFile):
        name = "waf-build-helper"
        version = "0.1"
        exports = "waf_environment.py"

As we said, the build helper is responsible for translating Conan settings to something that the
build tool understands. That can be passing arguments through the command line when invoking the tool
or creating files that will take as an input. In this case, the build helper for *Waf* will create
one file named *waf_toolchain.py* that will contain linker and compiler flags based on the Conan
settings.

To pass that information to `Waf` in the file, you have to modify its configuration environment
through the ``conf.env`` variable setting all the relevant flags. We will also define a ``configure``
and a ``build`` method. Let's see how the most important parts of *waf_environment.py* file that
defines the build helper could look. In this case, for simplification, the build helper will only add
flags depending on the conan setting value for the ``build_type``.

.. code-block:: python    

    class WafBuildEnvironment(object):
        def __init__(self, conanfile):
            self._conanfile = conanfile
            self._settings = self._conanfile.settings

        def build_type_flags(self, settings):
            if "Visual Studio" in self._compiler:
                if self._build_type == "Debug":
                    return ['/Zi', '/FS']
                elif self._build_type == "Release":
                    return ['/O2']
            else:
                if self._build_type == "Debug":
                    return ['-g']
                elif self._build_type == "Release":
                    return ['-O3']

        def _toolchain_content(self):
            sections = []
            sections.append("def configure(conf):")
            sections.append("    conf.env.CXXFLAGS = conf.env.CXXFLAGS or []")
            _build_type_flags = build_type_flags(self._settings)
            sections.append("    conf.env.CXXFLAGS.extend({})".format(_build_type_flags))
            return "\n".join(sections)

        def _save_toolchain_file(self):
            filename = "waf_conan_toolchain.py"
            content = self._toolchain_content()
            output_path = self._conanfile.build_folder
            save(os.path.join(output_path, filename), content)

        def configure(self, args=None):
            self._save_toolchain_file()
            args = args or []
            command = "waf configure " + " ".join(arg for arg in args)
            self._conanfile.run(command)

        def build(self, args=None): 
            args = args or []
            command = "waf build " + " ".join(arg for arg in args)
            self._conanfile.run(command)


Now you can export your custom build helper to the local cache, or upload to a remote:

.. code-block:: bash

    $ conan export .

After exporting this package to the local cache you can use this custom build helper to compile
our packages using the *Waf* build system. Just add the necessary configuration files for *Waf* and
import the ``python_requires``. The *conanfile.py* of that package could look similar to this:

.. code-block:: python

    from conans import ConanFile


    class TestWafConan(ConanFile):
        python_requires = "waf-build-helper/0.1"
        settings = "os", "compiler", "build_type", "arch"
        name = "waf-consumer"
        generators = "Waf"
        requires = "mylib-waf/1.0"
        build_requires = "WafGen/0.1", "waf/2.0.19"
        exports_sources = "wscript", "main.cpp"

        def build(self):
            waf = self.python_requires["waf-build-helper"].module.WafBuildEnvironment(self)
            waf.configure()
            waf.build()

As you can see in the *conanfile.py* we also are requiring the build tool and a generator for that
build tool. If you want more detailed information on how to integrate your own build system in Conan,
please `check this blog-post about that topic
<https://blog.conan.io/2019/07/24/C++-build-systems-new-integrations-in-Conan-package-manager.html>`_.
