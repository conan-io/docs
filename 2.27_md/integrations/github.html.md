<a id="integrations-github"></a>

# ![github_logo](images/integrations/conan-github-logo.png) GitHub

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The Conan [GitHub Actions](https://github.com/features/actions) integration allows you to setup
Conan client in your GitHub Actions workflows in a simple and effective way.

The project can be found on its [GitHub marketplace page](https://github.com/marketplace/actions/setup-conan-client), or
its [GitHub source page](https://github.com/conan-io/setup-conan) directly.

To use the integration, add a step in your workflow YAML file. The integration will
install the Conan client and set up the environment for you.

You can customize the following parameters:

- **Conan version**: Specify the Conan version to install (e.g., 2.15.1). Default: latest stable.
- **Configuration URLs**: A list of configuration URLs to download and install in Conan home. By default, no configuration is installed.
- **Conan Audit Token**: The [audit](https://docs.conan.io/2//devops/audit.html.md#devops-audit) token used for the audit command to scan vulnerabilities in packages. By default, no token is used.
- **Conan home path**: Set a custom location for the Conan home folder. By default, no custom path is used.
- **Cache Conan packages**: Cache all packages in your Conan cache automatically and re-use them in a next build. By default, no cache is used.
- **Python version**: You can specify the Python version to be installed with Conan, the same will be available in the environment. By default, Python 3.10 is installed.

The integration is available for all platforms supported by GitHub Actions, including Linux, Windows, and macOS.

## Examples

This section provides some examples of how to use the integration in your GitHub Actions workflows.

### Scanning Packages for Vulnerabilities in a Nightly Build

#### WARNING
Do not share your Conan audit token or expose it in your code. Always use GitHub secrets for sensitive data.

First, you need to set up the Conan audit token in your [GitHub secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions).
Then, use the following example to scan for vulnerabilities in a package and its dependencies:

```yaml
name: Nightly security scan
on:
  schedule:
    - cron: "0 0 * * *"

jobs:
  scan-vulnerabilities:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install and setup Conan
        uses: conan-io/setup-conan@v1
        with:
          audit_token: ${{ secrets.MY_CONAN_AUDIT_TOKEN }}

      - name: Scan for vulnerabilities with Conan Audit
        run: |
          conan audit scan .
```

This example scans all dependencies in a `conanfile.py` in the current directory.
Note that it uses a [GitHub schedule](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule) to run the scan every day at midnight, this is in the case of
using the free service token, to avoid hitting the daily limits, but still having security checks every day.

### Installing Conan configuration and building packages

This example installs a custom Conan configuration from a URL,
restores cached packages from previous builds, builds the package defined in the `conanfile.py`, and uploads it to the Conan server.

```yaml
name: Build and upload Conan package
on:
  push:
    branches:
      - 'main'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install and setup Conan
        uses: conan-io/setup-conan@v1
        with:
          config_urls: https://mycompany.com/conan/configs.git
          cache_packages: true

      - name: Build and upload package
        run: |
          conan create . -pr:a myprofile --build=missing
          conan remote login artifactory developer -p ${{ secrets.MY_CONAN_PASSWORD }}
          conan upload "*" --confirm --remote artifactory
```

In this example, the action’s option `cache_packages` is set to true, so all packages in the Conan cache are cached for the next build.
Remote information is expected from the configuration installed from the URL pointed by the option `config_urls`.
Remote authentication uses GitHub secrets for security. The remote authentication is done using the GitHub secrets, which is a secure way to store sensitive information.
