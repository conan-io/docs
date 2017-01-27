.. _how_to_define_complex_compatibility:

How to define complex compatibility relations
=============================================


Introduction
------------

Conan keeps the compatibility between binary packages using ``settings``.
When a recipe author specifies some settings in the :ref:`settings_property` property, is telling that any change at any 
of those settings will require a different binary package:

.. code-block:: python


	class MyLibConanPackage(ConanFile):	
	    name = "lib"
	    version = "1.0"
	    settings = "os", "arch", "compiler", "build_type"
	
So, we can require a conan package from our project using a ``conanfile.txt``:

.. code-block:: txt

    [requires]
    lib/1.0@my_user/stable
    
    [generators]
    cmake
	
And then install it:

.. code-block:: bash
    
    conan install .
    
Conan will retrieve the "lib/1.0@my_user/stable" recipe, read the ``settings`` field and mix those declared settings with my default settings
(because I didn't use any ``-s`` parameter), in my case:

**~/.conan/conan.conf**

.. code-block:: txt

	[settings_defaults]
	    os=Linux
	    arch=x86_64
	    build_type=Release
	    compiler=GCC
	    compiler.libcxx=libstdc++
	    compiler.version=4.9

So the mix of my settings values with the specified values will give us a SHA1 hash that will identify the binary package (Package ID) that we need, for example
``c6d75a933080ca17eb7f076813e7fb21aaa740f2``.

Now conan will try to locate the ``c6d75...`` package. If it's present conan will retrieve it, if don't we can try to build it with ``conan install --build``.
The important thing is that, if the recipe author has declared the settings correctly, we can guarantee that the binaries are compatible. 
So when I build and upload a package to a conan server, any user with the same settings (Linux, x86_64... etc) can reuse the binary package without building it from sources. 

Actually, the package ID also depend on two more things, the ``options`` declared in the recipe (and the given values), and the ``requires``: If a recipe depends on one or more recipes,
those recipes will be resolved to binary packages, each one with a package ID. And those package IDs from the required recipes will affect the computed package ID of our recipe. 
Check the :ref:`controlling_requires_compatibility` section.

But there are some use cases pending: 

- We know that our package is compatible with several different compiler versions:
	
	For example, our binary package is compatible with any GCC from version 4 to version 5.5., we don't want to build and upload one package for each version, one package
	is enough.

- Imagine that our library ``Mylib/1.0`` is requiring another library ``MyOtherLib/2.0``. If I change my required version from 2.0 to 2.1. What should happen?
  My requires are changing, so my package ID can change, then I need to build ``Mylib/1.0`` again, but should it be rebuilt? 
  It depends in different factors (static/shared, headers changing...) How can I control it? 


.. _controlling_settings_options_compatibility:


Using package_id() to control settings and options compatibility
----------------------------------------------------------------

The ``package_id()`` method allows us to precisely control when the computed package ID has to change.
Within the ``package_id`` method we have access to the ``self.info`` object. That object contents will
establish the package ID (just an object representation digest).

 - **self.info.settings**: Contains all the declared settings, always as string values. 
   We can access/alter the settings. E.j: ``self.info.settings.compiler.version``
   
 - **self.info.options**: Contains all the declared options, always as string values.
   E.j: ``self.info.options.shared``
   
You need to modify the ``self.info.settings`` and ``self.info.options``. You can assign any string value, there is no restriction.
For example, If you are sure your package ABI compatibility is fine for GCC versions > 4.5 and < 5.0, (just an example, not a real case) you can do this:


.. code-block:: python

	from conans import ConanFile, CMake, tools
	from conans.model.version import Version
	
	class PkgConan(ConanFile):
	    name = "pkg"
	    version = "1.0"
	    settings = "os", "compiler", "build_type", "arch"
	
	    def package_id(self):
	        v = self.settings.compiler.version.value # ".value" will return a comparable "Version" object
	        if self.settings.compiler == "GCC" and (v >= "4.5" and v < "5.0"):
	            self.info.settings.compiler.version = "GCC 4 between 4.5 and 5.0"
	
We have set the ``self.info.settings.compiler.version`` with a crazy value, it's not really important, could be any string, the only important thing is that won't change for any GCC[4.5-5.0].
Let's check that it works properly, lets install the package for GCC 4.5:

	
.. code-block:: bash

	> conan export myuser/mychannel
	> conan install pkg/1.0@myuser/mychannel -s compiler=GCC -s compiler.version=4.5
	
	Requirements
	    pkg/1.0@myuser/mychannel from local
	Packages
	    pkg/1.0@myuser/mychannel:mychannel:e08cd734dea06769613cef12e337fb9555e17480
	
	ERROR: Can't find a 'pkg/1.0@myuser/mychannel' package for the specified options and settings
	

We can see that the computed package ID is ``e08cd734dea06769613cef12e337fb9555e17480``. What would happen if we specify GCC 4.6?


	
.. code-block:: bash

	> conan install pkg/1.0@myuser/mychannel -s compiler=GCC -s compiler.version=4.6
	
	Requirements
	    pkg/1.0@myuser/mychannel from local
	Packages
	    pkg/1.0@myuser/mychannel:mychannel:e08cd734dea06769613cef12e337fb9555e17480

Same result, the required package is ``e08cd734dea06769613cef12e337fb9555e17480``. Now we can try with GCC 4.4 (<4.5).

.. code-block:: bash

	> conan install pkg/1.0@myuser/mychannel -s compiler=GCC -s compiler.version=4.6
	
	Requirements
	    pkg/1.0@myuser/mychannel from local
	Packages
	    pkg/1.0@myuser/mychannel:mychannel:7d02dc01581029782b59dcc8c9783a73ab3c22dd


Now the computed package ID is different, that means that we need a different binary package for GCC 4.4

The same way we have adjusted the ``self.info.settings`` we can adjust the ``self.info.options`` if we detect some compatibilities between the different packages.


.. _controlling_requires_compatibility:

Using package_id() to control requires compatibility
----------------------------------------------------

The ``self.info`` object also have a ``requires`` object. A dictionary with the requirements info. E.j ``self.info.requires["MyOtherLib"]``.
    
- Each requirement info has the following `read only` fields:
   
   - ``full_name``: Full require's name. E.j **MyOtherLib**
   - ``full_version``: Full require's version. E.j **1.2**
   - ``full_user``: Full require's user. E.j **my_user**
   - ``full_channel``: Full require's channel. E.j **stable**
   - ``full_package_id``: Full require's package ID. E.j **c6d75a...**
   
- The following are used in the SHA1 generation so they are useful to `control the package ID`:
   
   - ``name``: By default same value as full_name. E.j **MyOtherLib**
   - ``version``: By default the major version representation of the full_version. E.j **1.Y** for a **1.2** full_version field and **1.Y.Z** for a **1.2.3** full_version field. 
   - ``user``: By default None (doesn't affect to package ID)
   - ``channel``: By default None (doesn't affect to package ID)
   - ``package_id``: By default None (doesn't affect to package ID)
  
Controlling the dependencies' compatibility requires to take into account two factors:

 - The versioning schema followed by our requirements (semver?, custom?)
 - Type of library being built and type of library being reused (shared: so, dll, dylib, static).


Versioning schema
+++++++++++++++++
 
Example
^^^^^^^

 I'm creating a conan recipe ``Mylib/1.0``. That recipe requires ``MyOtherLib/2.0``. I've built my binary packages (for several different compiler versions)
 for both MyLib and MyOtherLib (all static libraries) and they are all available in my conan server.
 
 Then I do some improvements to ``MyOtherLib`` and I release a new version ``MyOtherLib/2.1``. I also generate and upload some new binary packages for the new ``MyOtherLib/2.1`` library, obviously 
 those packages will have different IDs.
 
 So, I edit my ``Mylib/1.0`` conanfile.py file and change the require to ``MyOtherLib/2.1``. 
 
 The question is... **Should I rebuild all my Mylib/1.0 packages?**
 
 As they are all static libraries, the final consumer (the developer creating a project) will link against ``Mylib/1.0`` and ``MyOtherLib/2.1`` (MyOtherLib/2.1 because of the package
 manager transitivity) libraries, so in the first instance, it seems that you never need to rebuild ``Mylib/1.0``. 
 That's because a static library is never embedded by other static library, are always different files. 
 
 Now think about the ``header files``. The final consumer will **#include** the header files from **Mylib/1.0**, so it seems it's not a problem either.
 
 But it's not always true! When we built from sources ``Mylib/1.0``, this library is also #including the header files from ``MyOtherLib/2.1``, the binary compatibility will be only guaranteed 
 if the ``MyOtherLib/2.1`` header files have not changed. For example, a function parameter declared in ``Mylib/1.0`` could have changed between 2.0 and 2.1:
 
 **MyOtherLib/2.0 => myheader.h**
 
 .. code-block:: cpp
 
 	int addition (int a, int b);
 
 
 **MyOtherLib/2.1 => myheader.h**
  
 .. code-block:: cpp
 
 	int addition (unsigned int a, unsigned int b);	
 


 In this case we have to rebuild all our ``Mylib/1.0`` packages. That means that the computed package ID for ``Mylib/1.0`` have to change.



How does conan manage versioning schema?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default conan suppose **semver** schema, that means, if a version changes from **2.0** to **2.1** conan suppose that the API is compatible (headers not changing).
In the same way if a version changes from **2.1.10** to **2.1.11** conan supposes that it's API compatible too. Those rules are defined by `semver <http://semver.org/>`_.

If you are not following `semver <http://semver.org/>`_. You can adjust your versioning schema with the ``package_id()`` method, manipulating the requires:


.. code-block:: python

	from conans import ConanFile, CMake, tools
	from conans.model.version import Version
	
	class PkgConan(ConanFile):
	    name = "Mylib"
	    version = "1.0"
	    settings = "os", "compiler", "build_type", "arch"
	    requires = "MyOtherLib/2.0@lasote/stable"
	
	    def package_id(self):
	        myotherlib = self.info.requires["MyOtherLib"]
	        
	        # Any change in the MyOtherLib version will change current Package ID
	        myotherlib.version = myotherlib.full_version
	        
	        # Changes in major and stable versions will change the Package ID but
	        # only a MyOtherLib revision won't. E.j: From 1.2.3 to 1.2.89 won't change.
	        myotherlib.version = myotherlib.full_version.minor()
	        
	        
There are some other helpers that we can use for specify our requires compatibility not directly related with the version, 
you can decide that the **channel** and the **user** also affects the binary compatibility, or even the require package ID 
can change your package ID:


.. code-block:: python

	from conans import ConanFile, CMake, tools
	from conans.model.version import Version
	
	class PkgConan(ConanFile):
	    name = "Mylib"
	    version = "1.0"
	    settings = "os", "compiler", "build_type", "arch"
	    requires = "MyOtherLib/2.0@lasote/stable"
	
	    def package_id(self):

	        # Default behavior, only major release changes the package ID
	        self.info.requires["MyOtherLib"].semver_mode()
	        
	        # Any change in the require version will change the package ID
	        self.info.requires["MyOtherLib"].full_version_mode()
	        
	        # Any change in the MyOtherLib version, user or channel will affect our package ID
	        self.info.requires["MyOtherLib"].full_recipe_mode()
	        
	     	# Any change in the MyOtherLib version, user or channel or Package ID will affect our package ID
	        self.info.requires["MyOtherLib"].full_package_mode()
	        
	        # The requires won't affect at all to the package ID
	        self.info.requires["MyOtherLib"].unrelated_mode()
	

You can also adjust the requirement info object properties manually:

.. code-block:: python

	def package_id(self):
        myotherlib = self.info.requires["MyOtherLib"]
		
        # Same as myotherlib.semver_mode()
        myotherlib.name = myotherlib.full_name
        myotherlib.version = myotherlib.full_version.stable()
        myotherlib.user = myotherlib.channel = myotherlib.package_id = None

        # Only the channel (and the name) matters
        myotherlib.name = myotherlib.full_name
        myotherlib.user = myotherlib.package_id = myotherlib.version = None
        myotherlib.channel = myotherlib.full_channel
        
        
        

You can check the generated **conaninfo.txt** file. The [requires], [options] and [settings] are took into account to generate the SHA1, 
This is a typical default semver requiring:

 .. code-block:: text

    [requires]
       MyOtherLib/2.Y.Z
   
    [full_requires]
       MyOtherLib/2.2@demo/testing:73bce3fd7eb82b2eabc19fe11317d37da81afa56
 


Library types: Shared, static, header only
++++++++++++++++++++++++++++++++++++++++++
 
Examples
^^^^^^^^

- ``Mylib/1.0`` is a shared library, embedding a static ``MyOtherLib/2.0``. When I release a new ``MyOtherLib/2.1`` version: Do I need to rebuild ``Mylib/1.0``?
  
   Yes, always, because the implementation is embedded in the ``Mylib/1.0`` shared library. If we always want to rebuild our library, even if the channel changes (we assume a channel
   change could mean a source code change):

.. code-block:: python

    def package_id(self):
        # Any change in the MyOtherLib version, user or channel or Package ID will affect our package ID
        self.info.requires["MyOtherLib"].full_package()
	   

- ``Mylib/1.0`` is a shared library, and requires another shared library to link with ``MyOtherLib/2.0``, if I release a new ``MyOtherLib/2.1`` version, Do I need to rebuild ``Mylib/1.0``?
  
  It depends, only if the headers have changed, if we are following ``semver`` for ``MyOtherLib/2.1`` we don't need to change anything, but otherwise we need to choose the better for us:


.. code-block:: python

    def package_id(self):
        # Any change in the MyOtherLib version, user or channel or Package ID will affect our package ID
        self.info.requires["MyOtherLib"].full_package()

        # Or any change in the MyOtherLib version, user or channel will affect our package ID
        self.info.requires["MyOtherLib"].full_recipe()
	   	

- ``Mylib/1.0`` is a static library, and requires a ``header only`` library ``MyOtherLib/2.0``, if I release a new ``MyOtherLib/2.1`` version, Do I need to rebuild ``Mylib/1.0``?
  
   Yes, by definition if a header only library changes, the headers are changing. If we know that the channel never implies a source code change (this is our workflow):


.. code-block:: python

    def package_id(self):

        self.info.requires["MyOtherLib"].full_package()
        self.info.requires["MyOtherLib"].channel = None # Channel doesn't change out package ID
