.. _integrations_clion:

|clion_logo| CLion
==================

Introduction
------------

There's a plugin `available in the JetBrains Marketplace
<https://plugins.jetbrains.com/plugin/11956-conan>`_ compatible with CLion versions higher
than *2022.3*. With that plugin you can browse Conan packages available in `Conan Center
<https://conan.io/center>`_, add them to your project and install them from the CLion IDE
interface.

This plugin utilizes `cmake-conan
<https://github.com/conan-io/cmake-conan/tree/develop2>`_, a `CMake dependency provider
<https://cmake.org/cmake/help/latest/guide/using-dependencies/index.html#dependency-providers>`_
for Conan. It injects ``conan_provider.cmake`` using the
``CMAKE_PROJECT_TOP_LEVEL_INCLUDES`` definition. This dependency provider will translate
the CMake configuration to Conan. For instance, if you select a *Debug* profile in CLion,
Conan will install and use the packages for *Debug*. 

Bear in mind that *cmake-conan* activates the Conan integration every time CMake calls to
``find_package()``, meaning that no library will be installed until the CMake configure
step runs. At that point, Conan will try to install the required libraries and build them
if needed. 

Also, note that as dependency providers are a relatively new feature in CMake, you will
need CMake version >= 3.24 and Conan >= 2.0.5.

Installing the plugin
---------------------

To install the new Conan CLion plugin, navigate to the JetBrains marketplace. Open CLion,
go to *Settings > Plugins*, then select the *Marketplace* tab. Search for the Conan plugin
and click on the Install button. 

|clion_install_plugin|

After restarting CLion, a new “Conan” tool tab will
appear at the bottom of the IDE.

Configuring the plugin
----------------------

Open a CMake project or create a new CMake project in CLion, as usual. Go to the “Conan”
tool tab at the bottom of the IDE. You will see that the only enabled action in the
toolbar of the plugin is the one with the ⚙️ (wheel) symbol, click on it.

|clion_configuration_1|

The first thing you should do there is configuring the Conan client executable that's
going to be used. You can point to one specifically installed in an arbitrary location on
your system or you can select *"Use Conan installed in the system"* to use the one
installed at the system level.

|clion_configuration_2|

You will find there some options marked as default. Let's go through all of them.

- First, you will see checkboxes to mark in which configurations Conan should manage the
  dependencies. In our case, as we only have the Debug configuration, it's the only one
  checked. Also, below that "Automatically add Conan support for all configurations" is
  marked by default. That means that you don't have to worry about adding Conan support to
  new build configurations because the plugin will automatically add Conan support by
  default.

- You can also see that there's a checkbox to let Conan change the default CLion settings
  and run CMake sequentially instead of running it in parallel. This is needed as the
  Conan cache is not yet concurrent up to Conan 2.0.9 version. 
  
Normally, if you are using the Conan plugin, you wouldn't want to unmark them. So leave
them and let's create our project and add the libraries to it. So, click on the OK button
and the plugin should be ready to use.

**Note:** At this point, CLion will run the configure step for CMake automatically. Since
the plugin sets up the *conan.cmake* dependency provider, a warning will appear in the
CMake output indicating that we have not added a `find_package()` to our *CMakeLists.txt*
yet. This warning will disappear after we add the necessary `find_package()` calls to the
*CMakeLists.txt* file. 

After doing the initial configuration, you will notice that the list of libraries is now
enabled and that the 🔄 (update) and 👁️ (inspect) symbols are also enabled. We will
explain them later in detail.

Using the plugin
----------------

Now that we have our plugin configured and ready, you can browse the available libraries
and install them from CLion. Let's say we want to use `libcurl
<https://curl.se/libcurl/>`_ to download an image from the Internet. Navigate to the
library list and search for *libcurl*. Some information on how to add it to CMake will be
displayed, along with a "Use in project" button. Select the version you want to use and
click the button. 

|clion_use_libcurl|

If you click on the 👁️ (inspect) icon mentioned earlier, you will see all the libraries
added to the project (in case you added more libraries). This includes basic target
information for CMake and the necessary code snippets to add to CMake to use them. 

|clion_inspect|

Conan stores information about the used packages in a *conandata.yml* file located in your
project folder. This file is read by a *conanfile.py*, also created during this process.
These files can be customized for advanced usage of the plugin, but please read the
information in the corresponding files on how to do this properly. Modify your
*CMakeLists.txt* according to the instructions, which should result in something like
this:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.15)
   project(project_name)
   set(CMAKE_CXX_STANDARD 17)
   find_package(CURL)
   add_executable(project_name main.cpp)
   target_link_libraries(project_name CURL::libcurl)

After reloading the CMake project, you should see Conan installing the libraries in the
CMake output tab.

.. seealso::

    - Check the `entry in the Conan blog about the plugin <https://blog.conan.io/introducing-new-conan-clion-plugin/>`_


.. |clion_logo| image:: ../images/integrations/clion/conan-icon-clion.png
.. |clion_install_plugin| image:: ../images/integrations/clion/clion-install-plugin.png
.. |clion_configuration_1| image:: ../images/integrations/clion/clion-configuration-1.png
.. |clion_configuration_2| image:: ../images/integrations/clion/clion-configuration-2.png
.. |clion_inspect| image:: ../images/integrations/clion/clion-inspect.png
.. |clion_use_libcurl| image:: ../images/integrations/clion/clion-use-libcurl.png
