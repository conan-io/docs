.. _integrations_github:

|github_logo| GitHub
====================

.. include:: ../common/experimental_warning.inc

The Conan `GitHub Actions <https://github.com/features/actions>`_ integration allows you to setup
Conan client in your GitHub Actions workflows in a simple and effective way.

The project can be found on its `GitHub marketplace page <https://github.com/marketplace/actions/setup-conan-environment>`_, or
its `GitHub source page <https://github.com/conan-io/setup-conan>`_ directly.

To use the integration, add a step in your workflow YAML file. The integration will
install the Conan client and set up the environment for you.

You can customize the following parameters:

- **Conan version**: Specify the Conan version to install (e.g., `2.15.1`). Default: latest stable.
- **Configuration URLs**: A list of configuration URLs to download and install in Conan home. By default, no configuration is installed.
- **Conan Audit Token**: The :ref:`audit<devops_audit>` token used for the audit command to scan vulnerabilities in packages. By default, no token is used.
- **Conan home path**: Set a custom location for the Conan home folder. By default, no custom path is used.
- **Cache Conan packages**: Cache all packages in your Conan cache automatically and re-use them in a next build. By default, no cache is used.
- **Python version**: You can specify the Python version to be installed with Conan, the same will be available in the environment. By default, Python 3.10 is installed.

The integration is available for all platforms supported by GitHub Actions, including Linux, Windows, and macOS.

Examples
--------

Scanning for vulnerabilities in packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

  Do not share your Conan audit token or expose it in your code. Always use GitHub secrets for sensitive data.

First, you need to set up the Conan audit token in your GitHub secrets.
Then, use the following example to scan for vulnerabilities in a package:

.. code-block:: yaml
   :caption: .github/workflows/ci.yml

   steps:
    - name: Consume Conan Action
      uses: conan-io/setup-conan@v1
      with:
        audit_token: ${{ secrets.MY_CONAN_AUDIT_TOKEN }}

    - name: Scan for vulnerabilities
      run: |
        conan audit provider list
        conan audit list openssl/3.4.1
        conan audit scan .

This example lists configured providers, scans the package ``openssl/3.4.1``, and scans all dependencies in a `conanfile.py` in the current directory.

Installing Conan configuration and building packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example installs a custom Conan configuration from a URL,
restores cached packages from previous builds, builds the `conanfile.py`, and uploads it to the Conan server.

.. code-block:: yaml
   :caption: .github/workflows/ci.yml

   steps:
    - name: Consume Conan Action
      uses: conan-io/setup-conan@v1
      with:
        config_urls: https://mycompany.com/conan/configs.git
        cache_packages: true

    - name: Build Conan package
      run: |
        conan create . -pr:a myprofile --build=missing

    - name: Update Conan package
      run: |
        conan remote login artifactory developer -p ${{ secrets.MY_CONAN_PASSWORD }}
        conan upload "*" --confirm --remote artifactory

In this example, `cache_packages` is set to true, so all packages in the Conan cache are cached for the next build.
Remote information is expected from the configuration installed from the URL. Remote authentication uses GitHub secrets for security.
The remote authentication is done using the GitHub secrets, which is a secure way to store sensitive information.


.. |github_logo| image:: ../images/integrations/conan-github-logo.png
