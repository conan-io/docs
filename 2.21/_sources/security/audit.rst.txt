.. _security_audit:

Scanning dependencies with ``conan audit``
==========================================

The ``conan audit`` commands provide a built-in way to **scan your dependencies for known CVEs**.

For a step-by-step guide on authentication, usage examples, output formats, and setting up
private providers, see :ref:`Checking package vulnerabilities <devops_audit>`. In short:

1. **Register** at `audit.conan.io <https://audit.conan.io/register>`_.
2. **Activate your account** via the confirmation email you receive.
3. **Save your token**, which is displayed on the page after activation.
4. **Configure Conan to use your token**:

.. code-block:: bash

   conan audit provider auth conancenter --token=<token>

5. Run a scan:

.. code-block:: bash

   # Check a specific reference 
   conan audit list zlib/1.2.13
   
   # Scan the entire dependency graph 
   conan audit scan .  # Path to the conanfile.py/txt


This command also supports using your own JFrog Platform as a private provider for
vulnerability scanning. See the :ref:`Adding private providers
<devops_audit_private_providers>` section for more details.

Filtering queried packages
--------------------------

By default, the ``conan audit scan`` command will query all packages in the dependency graph.
You can filter the packages to be queried based on their context using the ``--context`` option,
which accepts ``"host"``, or ``"build"`` as values, and when omitted, defaults to quering both contexts.

This allows you to skip checking for CVEs in build requirements, which are not part of the final product
and therefore less relevant (but still important!) for vulnerability scanning.

It's also possible to perform this filter using the ``conan audit list`` command,
by leveraging the packages list filtering from the ``conan list`` command. For example:

.. code-block:: bash

   # Generate the dependency graph in JSON format
   $ conan graph info . --format=json > graph.json
   # Create a packages list for the resolved dependency graph, filtering to only contain the `host` context packages
   $ conan list --graph=graph.json --graph-context=host --format=json > pkglist.json
   # Scan the filtered packages list for vulnerabilities
   $ conan audit list --list=pkglist.json



.. seealso::

    - `JFrog Academy Conan 2 Essentials: Scanning C++ packages for Vulnerabilities using Conan Audit <https://academy.jfrog.com/conan-2-essentials/2164300?utm_source=Conan+Docs>`__
    - For detailed reference documentation on all ``conan audit`` subcommands and their
      options, consult the :ref:`conan audit command reference
      <reference_commands_audit>`.
    - Read more in the dedicated `blog post
      <https://blog.conan.io/introducing-conan-audit-command/>`_.
