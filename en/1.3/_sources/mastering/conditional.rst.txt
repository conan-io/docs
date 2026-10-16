Conditional settings, options and requirements
==============================================

Remember, in your ``conanfile.py`` you have also access to the options of your dependencies,
and you can use them to:

* Add requirements dynamically
* Change values of options

The **configure** method might be used to hardcode dependencies options values. 
It is strongly discouraged to use it to change the settings values, please remember that ``settings``
are a configuration *input*, so it doesn't make sense to modify it in the recipes.

Also, for options, a more flexible solution is to define dependencies options values in the ``default_options``,
not in the ``configure()`` method, as this would allow to override them. Hardcoding them in the ``configure()``
method won't allow that and thus won't easily allow conflict resolution. Use it only when it is absolutely
necessary that the package dependencies use those options.

Here is an example of what we could do in our **configure method**:

.. code-block:: python

      ...
      requires = "Poco/1.9.0@pocoproject/stable" # We will add OpenSSL dynamically "OpenSSL/1.0.2d@lasote/stable"
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
