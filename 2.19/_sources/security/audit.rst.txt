.. _security_audit:

Scanning dependencies with conan audit
======================================

A new command, `conan audit`, was added in **Conan 2.14**. It provides a built-in way to
**scan your dependencies for known CVEs**.

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

.. seealso::

    - `JFrog Academy Conan 2 Essentials: Scanning C++ packages for Vulnerabilities using Conan Audit <https://academy.jfrog.com/conan-2-essentials/2164300?utm_source=Conan+Docs>`__
    - For detailed reference documentation on all ``conan audit`` subcommands and their
      options, consult the :ref:`conan audit command reference
      <reference_commands_audit>`.
    - Read more in the dedicated `blog post
      <https://blog.conan.io/introducing-conan-audit-command/>`_.
