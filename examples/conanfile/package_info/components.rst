.. _examples_conanfile_package_info_components:

Define components for Conan packages that provide multiple libraries
====================================================================

At the :ref:`section of the tutorial about the package_info()
method<creating_packages_package_info>` we learned how to define the information in a
package for consumers. Information like the library names or the include and library
folders. For the tutorial we were creating a package with only one library, that was the
one that consumers linked against. For some cases, libraries provide their functionalities
separated into different *components*. Those components could be consumed indenpendently
and in some cases they may require other components from the same library or others. Think
for example in a library like OpenSSL that provides *libcrypto* and *libssl* and *libssl*
depends on *libcrypto*.

Conan provides a way to abstract this information using the ``components`` attribute of the
``CppInfo`` object to define the information for each separate component of a Conan
package. Also, consumers can select specific components to link against them but not the
rest of the package.

Let's see an example of a game-engine library that provides several components like
*algorithms*, *ai*, *rendering* and *network*. The *ai* and *rendering* both depend on the
*algorithms* component.

game-engine package
-------------------