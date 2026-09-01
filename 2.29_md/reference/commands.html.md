<a id="reference-commands"></a>

# Commands

This section describes the Conan built-in commands, like `conan install` or `conan search`.

It is also possible to create user custom commands, visit [custom commands reference](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#reference-commands-custom-commands)
and these [custom command examples](https://docs.conan.io/2//examples/extensions/commands/custom_commands.html.md#examples-extensions-custom-commands)

**Consumer commands:**

- [conan cache](https://docs.conan.io/2//reference/commands/cache.html.md): Return the path of recipes and packages in the cache
- [conan config](https://docs.conan.io/2//reference/commands/config.html.md): Manage Conan configuration (remotes, settings, plugins, etc)
- [conan graph](https://docs.conan.io/2//reference/commands/graph.html.md): Obtain information about the dependency graph without fetching binaries
- [conan inspect](https://docs.conan.io/2//reference/commands/inspect.html.md): Inspect a conanfile.py to return the public fields
- [conan install](https://docs.conan.io/2//reference/commands/install.html.md): Install dependencies
- [conan list](https://docs.conan.io/2//reference/commands/list.html.md): List recipes, revisions and packages in the local cache or in remotes
- [conan lock](https://docs.conan.io/2//reference/commands/lock.html.md): Create and manage lockfiles
- [conan pkglist](https://docs.conan.io/2//reference/commands/pkglist.html.md): Manipulate package lists, merge them or find packages in remotes.
- [conan profile](https://docs.conan.io/2//reference/commands/profile.html.md): Display and manage profile files
- [conan remove](https://docs.conan.io/2//reference/commands/remove.html.md): Remove packages from the local cache or from remotes
- [conan remote](https://docs.conan.io/2//reference/commands/remote.html.md): Add, remove, login/logout and manage remote server
- [conan search](https://docs.conan.io/2//reference/commands/search.html.md): Search packages matching a name
- [conan version](https://docs.conan.io/2//reference/commands/version.html.md): Give information about the Conan client version
- [conan workspace (incubating)](https://docs.conan.io/2//reference/commands/workspace.html.md): Manage Conan workspaces
- [conan run](https://docs.conan.io/2//reference/commands/run.html.md): Execute binaries with automatic environment activation
- [conan require](https://docs.conan.io/2//reference/commands/require.html.md): Adds/removes requirements to/from your local conanfile

**Creator commands:**

- [conan build](https://docs.conan.io/2//reference/commands/build.html.md): Install package and call its build method
- [conan create](https://docs.conan.io/2//reference/commands/create.html.md): Create a package from a recipe
- [conan download](https://docs.conan.io/2//reference/commands/download.html.md): Download (without install) a single conan package from a remote server.
- [conan editable](https://docs.conan.io/2//reference/commands/editable.html.md): Allows working with a package in user folder
- [conan export](https://docs.conan.io/2//reference/commands/export.html.md): Export a recipe to the Conan package cache
- [conan export-pkg](https://docs.conan.io/2//reference/commands/export-pkg.html.md): Create a package directly from pre-compiled binaries
- [conan new](https://docs.conan.io/2//reference/commands/new.html.md): Create a new recipe from a predefined template
- [conan source](https://docs.conan.io/2//reference/commands/source.html.md): Calls the source() method
- [conan test](https://docs.conan.io/2//reference/commands/test.html.md): Test a package
- [conan upload](https://docs.conan.io/2//reference/commands/upload.html.md): Upload packages from the local cache to a specified remote

**Security Commands**

- [conan audit](https://docs.conan.io/2//reference/commands/audit.html.md): Checks for vulnerabilities in your Conan packages.
- [conan report](https://docs.conan.io/2//reference/commands/report.html.md): Get information about the packages

<a id="commands-output"></a>

**Commands Output to stdout and stderr**

Conan commands output information following a deliberate design choice that aligns with
common practices in many CLI tools and the [POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799/functions/stderr.html):

- `stdout`: For final command results (e.g., JSON, HTML).
- `stderr`: For diagnostic output, including logs, warnings, errors, and progress
  messages.

More info can be found more in the [FAQ section](https://docs.conan.io/2//knowledge/faq.html.md#faq-stdout-stderr-redirects).

**Redirecting Output to Files**

You can redirect Conan output to files using shell redirection:

```bash
$ conan install . --format=json > output.json
```

Alternatively, use the `--out-file` argument (available since Conan 2.12.0) to specify an
output file directly:

```bash
$ conan install . --format=json --out-file=output.json
```

## Command formatters

Almost all the commands have the parameter `--format xxxx` which is used to apply an output conversion.
The command formatters help users see the command output in a different way that could fit better with their needs.
Here, there are only some of the most important ones whose details are worthy of having a separate section.

- [graph-info formatter](https://docs.conan.io/2//reference/commands/formatters/graph_info_json_formatter.html.md): Show the graph information in JSON
  format. It’s used by several commands.
