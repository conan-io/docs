<a id="reference-commands-report"></a>

# conan report

The `conan report` command contains subcommands that return information about packages and libraries.

```text
$ conan report -h
usage: conan report [-h] [--out-file OUT_FILE]
                    [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                    [-cc CORE_CONF]
                    {diff} ...

Gets information about the recipe and its sources.

positional arguments:
  {diff}                sub-command help
    diff                Get the difference between two recipes with their
                        sources. It can be used to compare two different
                        versions of the same recipe, or two different recipe
                        revisions. Each old/new recipe can be specified by a
                        path to a conanfile.py and a companion reference, or
                        by a reference only. If only a reference is specified,
                        it will be searched in the local cache, or downloaded
                        from the specified remotes. If no revision is
                        specified, the latest revision will be used.

options:
  -h, --help            show this help message and exit
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True

```

## conan report diff

```text
$ conan report diff -h
usage: conan report diff [-h] [-f FORMAT] [--out-file OUT_FILE]
                         [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                         [-cc CORE_CONF] [-op OLD_PATH] -or OLD_REFERENCE
                         [-np NEW_PATH] -nr NEW_REFERENCE [-r REMOTE]

Get the difference between two recipes with their sources. It can be used to
compare two different versions of the same recipe, or two different recipe
revisions. Each old/new recipe can be specified by a path to a conanfile.py
and a companion reference, or by a reference only. If only a reference is
specified, it will be searched in the local cache, or downloaded from the
specified remotes. If no revision is specified, the latest revision will be
used.

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Select the output format: json, html
  --out-file OUT_FILE   Write the output of the command to the specified file
                        instead of stdout.
  -v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]
                        Level of detail of the output. Valid options from less
                        verbose to more verbose: -vquiet, -verror, -vwarning,
                        -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                        -vvv or -vtrace
  -cc CORE_CONF, --core-conf CORE_CONF
                        Define core configuration, overwriting global.conf
                        values. E.g.: -cc core:non_interactive=True
  -op OLD_PATH, --old-path OLD_PATH
                        Path to the old recipe if comparing a local recipe is
                        desired
  -or OLD_REFERENCE, --old-reference OLD_REFERENCE
                        Old reference, e.g. 'mylib/1.0'. If used on its own,
                        it can contain a revision, which will be resolved to
                        the latest one if not provided, but it will be ignored
                        if a path is specified. If used with a path, it will
                        be used to create the reference for the recipe to be
                        compared.
  -np NEW_PATH, --new-path NEW_PATH
                        Path to the new recipe if comparing a local recipe is
                        desired
  -nr NEW_REFERENCE, --new-reference NEW_REFERENCE
                        New reference, e.g. 'mylib/1.0'. If used on its own,
                        it can contain a revision, which will be resolved to
                        the latest one if not provided, but it will be ignored
                        if a path is specified. If used with a path, it will
                        be used to create the reference for the recipe to be
                        compared.
  -r REMOTE, --remote REMOTE
                        Look in the specified remote or remotes server

```

The `conan report diff` command gets the differences between two recipes, also comparing their sources.
This functionality allows you to compare either two versions of the same recipe or two entirely different recipes.
Each recipe (old and new) can be identified in one of two ways: by providing both the path to its `conanfile.py` and
its reference, or by specifying just the reference.

When only a reference is given, Conan will first search for the recipe in the local cache; if it is not found, it will
attempt to download it from the configured remotes. If no revision is explicitly provided, Conan will
default to using the latest available revision.

### **Examples**

#### Remote Reference vs Remote Reference

If we want to compare versions 1.0 and 2.0 of mylib that are available on our my-remote remote, it would be:

```bash
$ conan report diff --old-reference="mylib/1.0" --new-reference="mylib/2.0" -r=my-remote
```

#### Remote Reference vs Local Reference

Let’s suppose we’re making changes to the recipe or adding a new version, and we want to compare our changes against a
version that is in the remote. The version that is not on the remote requires the path to the recipe in order to compare
it. If it’s the old version that we’re modifying and it’s not found in the remotes, we would use `--old-path`:

```bash
$ conan report diff --old-reference="mylib/1.0" --old-path="path/to/recipe" --new-reference="mylib/2.0"
```

If, on the other hand, it’s the new version that we’re modifying then we would use `--new-path`:

```bash
$ conan report diff --old-reference="mylib/1.0" --new-reference="mylib/2.0" --new-path="path/to/recipe"
```

#### Local Reference vs Local Reference

Finally, if we’re modifying both versions, we’ll need to provide both paths. They may or may not be the same.

```bash
$ conan report diff --old-reference="mylib/1.0" --old-path="path/to/recipe" --new-reference="mylib/2.0" --new-path="path/to/recipe"
```

#### Specifying revision

The command allows you to specify the revision of the package you want to compare. By default, it uses the latest
revision, but by providing a revision, you can target the exact package you want to compare. This makes it possible
to do things like compare two identical versions with different revisions in order to check for differences between
them.

```bash
$ conan report diff --old-reference="mylib/1.0#oldrev" --new-reference="mylib/1.0#newrev"
```

### Available formatters

#### Text Formatter

By default, it displays this format, which is the format provided by a `git diff` between the packages.

#### JSON Formatter

You can obtain the result in JSON format, providing a structured output that is perfect for consumption by other
scripts.

```bash
$ conan report diff --old-reference="mylib/1.0" --new-reference="mylib/2.0" --format=json
```

#### HTML Formatter

The HTML format generates a small self-contained static web page in a single HTML file. This page lets you conveniently
visualize the changes in the recipe as well as the changes in the source files of your libraries. It contains filters
to include and exclude keywords and shortcuts to all the changed files.

```bash
$ conan report diff --old-reference="zlib/1.3" --new-reference="zlib/1.3.1" --format=html > diff.html
```

[![image](images/conan-report-diff_html.png)](../../_images/conan-report-diff_html.png)
