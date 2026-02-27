How to use Conan as other language package manager
==================================================

Conan is a generic package manager. In the :ref:`getting started <getting_started>` section we saw how to use conan and manage a C/C++
library, like POCO.

But conan just provided some tools, related with C/C++ (like some generators and the cpp_info), to offer a better user experience. The
general basis of Conan can be used with other programming languages.

Obviously, this does not try to compete with other package managers. Conan is a C and C++ package manager, focused on C and C++
developers. But when we realized that this was possible, we thought it was a good way to showcase its power, simplicity and versatility.

And of course, if you are doing C/C++ and occasionally you need some package from other language in your workflow, as in the conan package
recipes themselves, or for some other tooling, you might find this functionality useful.

.. toctree::
   :maxdepth: 2

   other_languages_package_manager/go
   other_languages_package_manager/python