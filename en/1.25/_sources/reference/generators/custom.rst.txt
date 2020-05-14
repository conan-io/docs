:orphan:

.. _custom_generator:

Custom generator
================

Don't see a generator that suit your needs? You can create a custom generator package and use it in your recipes!

Basically a generator is a class that extends ``Generator`` and implements two properties:

- ``filename`` (Required): Should return the name of the file that will be generated
- ``content`` (Required): Should return the contents of the file with the desired format.

The **name of the generator** itself will be taken literally from the class name. In the example below, the name will be
``MyGeneratorName``:

.. code-block:: python

    from conans.model import Generator


    class MyGeneratorName(Generator):

        @property
        def filename(self):
            return "mygenerator.file"
    
        @property
        def content(self):     
            return "whatever contents the generator produces"

If you want to create a generator that creates more than one file, you can leave the ``filename`` property empty and return a dictionary of
filenames and contents in the ``content`` property, like this:

.. code-block:: python
   :caption: *conanfile.py*

    from conans import ConanFile
    from conans.model import Generator


    class MultiGenerator(Generator):

        @property
        def content(self):
            return {"filename1.txt": "contents of file1",
                    "filename2.txt": "contents of file2"}  # any number of files

        @property
        def filename(self):
            pass
    
    class MyCustomGeneratorPackage(ConanFile):
        name = "MultiGeneratorPkg"
        version = "0.1"
        url = "https://github.com/..."
        license = "MIT"

This class should be included in a *conanfile.py* that must contain also a ``ConanFile`` class that implements the package itself, with the
name of the package, the version, etc. This class typically has no ``source()``, ``build()``, ``package()``, and even the ``package_info()``
method is overridden as it doesn't have to define any include paths or library paths. Then, it will work as a regular package.

Attributes
----------

Ready only attributes available for use in the ``Generator`` class.

conanfile
+++++++++

To get the information from the requirements and the environment:

+-----------------------------------------+------------------------------------------------------------------------------------------------+
| Variable                                | Description                                                                                    |
+=========================================+================================================================================================+
| self.conanfile.deps_cpp_info            | :ref:`deps_cpp_info_attributes_reference`                                                      |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| self.conanfile.deps_env_info            | :ref:`deps_env_info_attributes_reference`                                                      |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| self.conanfile.deps_user_info           | :ref:`deps_user_info_attributes_reference`                                                     |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| self.conanfile.env                      | Dictionary with the applied environment variables declared in the requirements                 |
+-----------------------------------------+------------------------------------------------------------------------------------------------+

output_path
+++++++++++

Path to the output folder where the files of the generator will be created.

.. seealso::

    Check :ref:`dyn_generators`.
