Package reference
+++++++++++++++++

Recipe attributes that can define the main ``pkg/version@user/channel`` package reference.


name
----

The name of the package. A valid name is all lowercase and has:

- A minimum of 2 and a maximum of 101 characters (though shorter names are recommended).
- Matches the following regex ``^[a-z0-9_][a-z0-9_+.-]{1,100}$``: so starts with alphanumeric or ``_``,
    then from 1 to 100 characters between alphanumeric, ``_``, ``+``, ``.`` or ``-``.

The name is only necessary for ``export``-ing the recipe into the local cache (``export``, ``export-pkg``
 and ``create`` commands), if they are not defined in the command line with ``--name=<pkgname>``.


version
-------

The version of the package. A valid version follows the same rules than the ``name`` attribute.
In case the version follows semantic versioning in the form ``X.Y.Z-pre1+build2``, that value might be used for requiring
this package through version ranges instead of exact versions.

The version is only strictly necessary for ``export``-ing the recipe into the local cache (``export``, ``export-pkg`` 
and ``create`` commands), if they are not defined in the command line with ``--version=<pkgversion>``

The ``version`` can be dynamically defined in the command line, and also programmatically in the recipe with the
:ref:`set_version() method<reference_conanfile_methods_set_version>`.


user
----

A valid string for the ``user`` field follows the same rules than the ``name`` attribute.
This is an optional attribute. It can be used to identify your own packages with ``pkg/version@user/channel``,
where ``user`` could be the name of your team, org or company. ConanCenter recipes don't have ``user/channel``,
so they are in the form of ``pkg/version`` only. You can also name your packages without user and channel, or using
only the user as ``pkg/version@user``.

The user can be specified in the command line with ``--user=<myuser>``


channel
-------

A valid string for the ``channel`` field follows the same rules than the ``name`` attribute.
This is an optional attribute. It is sometimes used to identify a maturity of the package ("stable", "testing"...),
but in general this is not necessary, and the maturity of packages is better managed by putting them in different
server repositories.

The user can be specified in the command line with ``--channel=<mychannel>``
