.. _integrations_github:

|github_logo| GitHub
====================

.. include:: ../common/experimental_warning.inc

The Conan `GitHub Actions <https://github.com/features/actions>`_ integration allows you to setup
Conan client in your GitHub Actions workflows in a simple and effective way.

The project can be found through its `GitHub marketplace page <https://github.com/marketplace/actions/setup-conan-environment>`_, or by
its `GitHub source page <https://github.com/conan-io/setup-conan>`_ directly.

In order to use the integration, you need to add a step in your workflow YAML file. The integration will
install the Conan client and set up the environment for you.
The integration can also customize the following parameters:

- **Conan version**: You can specify the Conan version to install. By default, the latest stable version is installed.
- **Configuration URLs**: A list of configuration URLs to download and install in Conan home. By default, no configuration is installed.
- **Conan Audit Token**: The :ref:`audit<devops_audit>` token used for the audit command to scan vulnerabilities in packages. By default, no token is used.
- **Conan home path**: It controls the location of the Conan home folder. By default, no custom path is used.
- **Cache Conan packages**: You can cache all your packages present in your Conan cache automatically. By default, no cache is used.
- **Python version**: You can specify the Python version to be installed with Conan, the same will be available in the environment. By default, Python 3.10 is installed.

The integration is available for all platforms supported by GitHub Actions, including Linux, Windows, and macOS.

Examples
--------

Scanning for vulnerabilities in packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

  Please, do not share your Conan audit token with anyone, neither expose it in your code.

First, you need to set up the Conan audit token in your GitHub secrets.
Then, you can use the following example to scan for vulnerabilities in a package:

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
        conan audit list openssl/1.1.1w
        conan audit scan .

The following example shows the configured providers, scans the package ``openssl/1.1.1w``, and scans all dependencies listed in a conanfile.py present in the current directory.


Installing Conan configuration and build packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, a custom Conan configuration is installed from a URL.
The cached packages are from previous builds are restored from the cache.
Then the conanfile.py is built and uploaded to the Conan server.


.. code-block:: yaml
   :caption: .github/workflows/ci.yml

   steps:
    - name: Consume Conan Action
      uses: conan-io/setup-conan@v1
      with:
        config_urls: https://mycompany.com/conan/configs.git
        cache_packages: true

    - name: Build Conan package
      # The profile myprofile is installed from the configuration
      run: |
        conan create conanfile.py -pr:a myprofile --build=missing

    - name: Update Conan package
      run: |
        conan remote login artifactory developer -p ${{ secrets.MY_CONAN_PASSWORD }}
        conan upload "*" --confirm --remote artifactory

This example shows how to build a Conan package and upload it to a remote server.
It's important to note that `cache_packages` is set to true, which means that all
packages present in the Conan cache will be cached automatically for a next build in GitHub Actions.
Also, the remote information is expected from the configuration installed from the URL.
The remote authentication is done using the GitHub secrets, which is a secure way to store sensitive information.


.. |github_logo| image:: ../images/integrations/conan-github-logo.png
