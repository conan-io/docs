Conditional settings, options and requirements
==============================================

Remember, in your ``conanfile.py`` you have also access to the options of your dependencies,
and you can use them to:

* Add requirements dynamically
* Change values of options

The **configure** method is the right place to change values of options and settings.

Here is an example of what we could do in our **configure method**:

.. code-block:: python

      ...
      requires = "Poco/1.7.8p3@pocoproject/stable" # We will add OpenSSL dynamically "OpenSSL/1.0.2d@lasote/stable"
      ...

      def configure(self):
          # We can control the options of our dependencies based on current options
          self.options["OpenSSL"].shared = self.options.shared

          # Maybe in windows we know that OpenSSL works better as shared (false)
          if self.settings.os == "Windows":
             self.options["OpenSSL"].shared = True

             # Or adjust any other available option
             self.options["Poco"].other_option = "foo"

          # We could check the presence of an option
          if "shared" in self.options:
              pass

      def requirements(self):
          # Or add a new requirement!
          if self.options.testing:
             self.requires("OpenSSL/2.1@memsharded/testing")
          else:
             self.requires("OpenSSL/1.0.2d@lasote/stable")


.. seealso:: Check the section :ref:`Reference/conanfile.py/configure(), config_options() <method_configure_config_options>` to find out more.
