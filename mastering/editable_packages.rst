Packages in editable mode [EXPERIMENTAL]
========================================

When working in big projects with several functionalities interconnected it is recomended to avoid
the one-and-only huge project approach in favor of several libraries each one of them specialized
in a set of common tasks, even maintained by dedicated teams. This approach helps to isolate
and reuse code, helps with compiling times and reduces the likelihood of including files that
not correspond to the API of the required library.

Nevertheless, in some case, it is useful to work in several libraries at the same time and see how
the changes in one of them are propagated to the others. Following the
:ref:`local workflow<package_dev_flow>` an user can execute the commands :command:`conan source`,
:command:`conan install`, :command:`conan build` and :command:`conan package`, but in order to
get the changes ready for a consumer library, it is needed the :command:`conan create` that will
actually trigger a build to generate the binaries in the cache and will copy them and the needed
headers to the directories specified in the ``package_info`` method of the *conanfile.py*. For each
change in this library that the user wants to be reflected in a consumer package, Conan has to
recreate the artifacts and copy all the stuff to the cache.

What about if you just can tell Conan where to find the headers and the artifacts ready for
consumption in your local working directory? Not need to package, just tell Conan to use those
artifacts you have just generated with your IDE, sounds good? This is what the feature
*editable packages* will do for you.

Let's see this feature over an example where a developer is creating a ``CoolApp`` but at the same
time he/she wants to work on ``cool/version@user/dev`` which is tightly coupled to the app.

Setting it all up
-----------------

The package ``cool/version@user/dev`` is already working, the developer has the sources in a
local folder, he/she is using whatever method to build and develop locally and can perform
a :command:`conan create . libCool/version@user/dev` to create the package.

Also, there is a *conanfile.txt* (or a more complex recipe) for the application ``CoolApp`` that
has ``cool/version@user/dev`` among its requirements. When building this application, the
resources of ``cool`` are used from the Conan local cache.

Put a package in editable mode
------------------------------

To avoid creating the package ``cool/version@user/dev`` in the cache for every change, we can
create **a link from the package in the cache to the local working directory**:

.. code-block:: bash

    $ conan link <path/to/local/dev/libcool> cool/version@user/dev

and we need a file to tell Conan what is the layout of your local project in order to provide the
proper paths to the build system. There are several ways to achieve this objective:

 * A file next to the *conanfile.py* with the name *.conan_layout*:

   .. code-block:: ini

       [includedirs]
       src/core/include
       src/cmp_a/include

       [libdirs]
       build/{settings.build_type}/{options.shared}

       [bindirs]
       build/{settings.build_type}/{options.shared}

 * A file inside the Conan cache in the path *layouts/default*. As this file can contain information
   for several packages, each section must declare which packages it applies to, this is achieved
   using a *namespace* with the name of the package or the wildcard ``*``:

   .. code-block:: ini

       [cool:includedirs]
       src/core/include
       src/cmp_a/include

       [*:libdirs]
       build/{settings.build_type}/{options.shared}

       [*:bindirs]
       build/{settings.build_type}/{options.shared}


   This file can be very handy inside a company where all the packages have the same layout.

As you can see, you can use some **placeholders** inside these files that will be substituted with
the values of the ``settings`` and the ``options`` of the package.

Regarding the precedence if both files are present, Conan will use the one inside the repository if
present, then the one in the Conan cache, and if none is available, Conan will fallback to the
directories defined in the ``package_info`` method of the recipe itself but relative to the path
where the editable package has been linked to.

Using a package in editable mode
--------------------------------

Once a package is in editable mode it is used **system wide** by Conan (by every Conan client that
uses the same cache), no changes are required in the consumers. Every :command:`conan install`
command that requires our editable ``cool/version@user/dev`` package will use the paths to
the local directory and the changes made to this project will be taken into account by the
packages using its headers or linking against it.

Revert the editable mode
------------------------

In order to revert the editable mode just remove the link using:

.. code-block:: bash

    $ conan link --remove cool/version@user/dev

It will remove the link (the local directory won't be affected) and all the packages using this
requirement will use the one in the cache again.

.. warning::

   Packages that are built using an editable package in its graph upstreams can generate binaries
   and packages incompatible with the released version of the editable package. Avoid uploading
   these packages without re-creating them with the in-cache version of all the libraries.


.. note::

   This is an experimental feature and it is in its early stage, it can suffer changes on its
   interface, behavior or be totally removed. But, if you start to use it, we would very
   pleased to hear from your experience and receive feedback. Thanks.
