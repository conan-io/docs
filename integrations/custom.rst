.. _other_generator:


Custom integrations
===================

If you intend to use a build system that does not have a built-in generator, you may still be 
able to do so. There are several options:

- First, search in Bintray for generator packages. Generators can be created and contributed by users as regular packages, so you can depend
  on them as a normal requirement, use versioning and evolve faster without depending on the Conan releases.

- You can use the :ref:`text_generator` or :ref:`json_generator` generators. They will generate a text file, simple to read that you can
  easily parse with your tools to extract the required information.

- Use the **conanfile data model** (:ref:`deps_cpp_info_attributes_reference`, :ref:`deps_env_info_attributes_reference`) in your recipe to
  access its properties and values, so you can directly call your build system with that information, without requiring to generate a file.

- Write and **create your own generator**. So you can upload it, version and reuse it, as well as share it with your team or community.
  Check :ref:`dyn_generators`.

.. note::

    Need help integrating your build system? Tell us what you need: info@conan.io

.. _json_integration:

Use the JSON generator
----------------------

Specify the ``json`` generator in your recipe:

.. code-block:: ini
   :caption: *conanfile.txt*

    [requires]
    fmt/5.3.0@bincrafters/stable
    Poco/1.9.0@pocoproject/stable

    [generators]
    json

A file named *conanbuildinfo.json* will be generated. It will contain the information about every dependency:

.. code-block:: json
   :caption: *conanbuildinfo.json*

    {
      "dependencies":
      [
        {
          "name": "fmt",
          "version": "5.3.0",
          "include_paths": [
            "/path/to/.conan/data/fmt/5.3.0/bincrafters/stable/package/<id>/include"
          ],
          "lib_paths": [
            "/path/to/.conan/data/fmt/5.3.0/bincrafters/stable/package/<id>/lib"
          ],
          "libs": [
            "fmt"
          ],
          "...": "...",
        },
        {
          "name": "Poco",
          "version": "1.9.0",
          "...": "..."
        }
      ]
    }

.. _txt_integration:

Use the text generator
----------------------

Just specify the ``txt`` generator in your recipe:

.. code-block:: text
   :caption: *conanfile.txt*

    [requires]
    Poco/1.9.0@pocoproject/stable

    [generators]
    txt

A file is generated with the same information in a generic text format.

.. code-block:: text
   :caption: *conanbuildinfo.txt*

    [includedirs]
    /home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/include
    /home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/include
    /home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/include

    [libs]
    PocoUtil
    PocoXML
    PocoJSON
    PocoMongoDB
    PocoNet
    PocoCrypto
    PocoData
    PocoDataSQLite
    PocoZip
    PocoFoundation
    pthread
    dl
    rt
    ssl
    crypto
    z

    [libdirs]
    /home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/lib
    /home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/lib
    /home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/lib

    [bindirs]
    /home/laso/.conan/data/Poco/1.6.1/lasote/stable/package/afafc631e705f7296bec38318b28e4361ab6787c/bin
    /home/laso/.conan/data/OpenSSL/1.0.2d/lasote/stable/package/154942d8bccb87fbba9157e1daee62e1200e80fc/bin
    /home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/3b92a20cb586af0d984797002d12b7120d38e95e/bin

    [defines]
    POCO_STATIC=ON
    POCO_NO_AUTOMATIC_LIBS

    [USER_MyRequiredLib1]
    somevariable=Some Value
    othervar=Othervalue

    [USER_MyRequiredLib2]
    myvar=34

Use the Conan data model (in a *conanfile.py*)
----------------------------------------------

If you are using any other build system you can use Conan too. In the ``build()`` method you can access your settings and build information
from your requirements and pass it to your build system. Note, however, that probably is simpler and much more reusable to create a
generator to simplify the task for your build system.

.. code-block:: python
   :caption: *conanfile.py*

    from conans import ConanFile


    class MyProjectWithConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        requires = "Poco/1.9.0@pocoproject/stable"
        ########### IT'S IMPORTANT TO DECLARE THE TXT GENERATOR TO DEAL WITH A GENERIC BUILD SYSTEM
        generators = "txt"
        default_options = {"Poco:shared": False, "OpenSSL:shared": False}

        def imports(self):
            self.copy("*.dll", dst="bin", src="bin") # From bin to bin
            self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

        def build(self):
            ############ Without any helper ###########
            # Settings
            print(self.settings.os)
            print(self.settings.arch)
            print(self.settings.compiler)

            # Options
            #print(self.options.my_option)
            print(self.options["OpenSSL"].shared)
            print(self.options["Poco"].shared)
      
            # Paths and libraries, all
            print("-------- ALL --------------")
            print(self.deps_cpp_info.include_paths)
            print(self.deps_cpp_info.lib_paths)
            print(self.deps_cpp_info.bin_paths)
            print(self.deps_cpp_info.libs)
            print(self.deps_cpp_info.defines)
            print(self.deps_cpp_info.cflags)
            print(self.deps_cpp_info.cxxflags)
            print(self.deps_cpp_info.sharedlinkflags)
            print(self.deps_cpp_info.exelinkflags)

            # Just from OpenSSL
            print("--------- FROM OPENSSL -------------")
            print(self.deps_cpp_info["OpenSSL"].include_paths)
            print(self.deps_cpp_info["OpenSSL"].lib_paths)
            print(self.deps_cpp_info["OpenSSL"].bin_paths)
            print(self.deps_cpp_info["OpenSSL"].libs)
            print(self.deps_cpp_info["OpenSSL"].defines)
            print(self.deps_cpp_info["OpenSSL"].cflags)
            print(self.deps_cpp_info["OpenSSL"].cxxflags)
            print(self.deps_cpp_info["OpenSSL"].sharedlinkflags)
            print(self.deps_cpp_info["OpenSSL"].exelinkflags)

            # Just from POCO
            print("--------- FROM POCO -------------")
            print(self.deps_cpp_info["Poco"].include_paths)
            print(self.deps_cpp_info["Poco"].lib_paths)
            print(self.deps_cpp_info["Poco"].bin_paths)
            print(self.deps_cpp_info["Poco"].libs)
            print(self.deps_cpp_info["Poco"].defines)
            print(self.deps_cpp_info["Poco"].cflags)
            print(self.deps_cpp_info["Poco"].cxxflags)
            print(self.deps_cpp_info["Poco"].sharedlinkflags)
            print(self.deps_cpp_info["Poco"].exelinkflags)

            # self.run("invoke here your configure, make, or others")
            # self.run("basically you can do what you want with your requirements build info)

            # Environment variables (from requirements self.env_info objects)
            # are automatically applied in the python ``os.environ`` but can be accesible as well:
            print("--------- Globally -------------")
            print(self.env)

            print("--------- FROM MyLib -------------")
            print(self.deps_env_info["MyLib"].some_env_var)

            # User declared variables (from requirements self.user_info objects)
            # are available in the self.deps_user_info object
            print("--------- FROM MyLib -------------")
            print(self.deps_user_info["MyLib"].some_user_var)

Create your own generator
-------------------------

There are two ways in which generators can be contributed:

- Forking and adding the new generator in the Conan codebase. This will be a built-in generator. It might have a much slower release and
  update cycle, it needs to pass some tests before being accepted, but it has the advantage than no extra things are needed to use that
  generator (once next Conan version is released).

- Creating a custom :ref:`generator package <dyn_generators>`. You can write a *conanfile.py* and add the custom logic for a generator
  inside that file, then upload, refer and depend on it as any other package. These generators will be another node in the dependency graph
  but they have many advantages: much faster release cycles, independent from the Conan codebase and can be versioned. So backwards
  compatibility and upgrades are much easier.


.. _pylint_integration:


Extending Conan
---------------

There are other powerful mechanisms to integrate other tools with Conan. Check the :ref:`Extending Conan <extending>` section for further information.
