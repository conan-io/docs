<a id="integrations-jfrog"></a>

# ![jfrog_logo](images/integrations/conan-jfrog-logo.png) JFrog

## Artifactory Build Info

#### WARNING
The support of Artifactory Build Info via extension commands is not covered by [the Conan stability commitment](https://docs.conan.io/2//introduction.html.md#stability).

The [Artifactory build info](https://www.buildinfo.org/) is a recollection of the metadata of a build.
This json-formatted file includes all the details about the build broken down into segments like version history, artifacts, project
modules, dependencies, and everything that was required to create the build.

Build infos are identified with a `build name` and a `build number`, similar to how many CI services identify the builds.
They are conveniently stored in Artifactory to keep track of the build metadata to later perform different operations.

Conan does not offer built-in support for the build info format. However, we have developed some [custom commands](https://docs.conan.io/2//reference/extensions/custom_commands.html.md#reference-commands-custom-commands) at
at the [extensions repository](https://github.com/conan-io/conan-extensions) using the feature, that provides support to create and manage the build info files.

### How to install the build info extension commands

Using the dedicated repository for Conan extensions [https://github.com/conan-io/conan-extensions](https://github.com/conan-io/conan-extensions), it is as easy as:

```bash
$ conan config install https://github.com/conan-io/conan-extensions.git -sf=extensions/commands/art -tf=extensions/commands/art
```

### Generating a Build Info

A Build Info can be generated from a create or install command:

```bash
$ conan create . --format json -s build_type=Release > create_release.json
```

Then upload the created package to your repository:

```bash
$ conan upload ... -c -r ...
```

Now, using the JSON output from the create/install commands, a build info file can be generated:

```bash
$ conan art:build-info create create_release.json mybuildname_release 1 <repo> --server my_artifactory --with-dependencies > mybuildname_release.json
```

And then uploaded to Artifactory:

```bash
$ conan art:build-info upload mybuildname_aggregated.json --server my_artifactory
```

For more reference, see the full example at [https://github.com/conan-io/conan-extensions/tree/main/extensions/commands/art#how-to-manage-build-infos-in-artifactory](https://github.com/conan-io/conan-extensions/tree/main/extensions/commands/art#how-to-manage-build-infos-in-artifactory)

#### SEE ALSO
- JFrog Artifactory has a [dedicated API](https://jfrog.com/help/r/jfrog-rest-apis/build-info) to manage build infos that
  has been integrated into the custom commands for Artifactory.
- Check the `conan art:build-info` documentation for reference:
  [https://github.com/conan-io/conan-extensions/blob/main/extensions/commands/art/readme_build_info.md](https://github.com/conan-io/conan-extensions/blob/main/extensions/commands/art/readme_build_info.md)
