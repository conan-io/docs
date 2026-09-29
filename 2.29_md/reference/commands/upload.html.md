<a id="reference-commands-upload"></a>

# conan upload

Use this command to upload recipes and binaries to Conan repositories. For more
information on how to work with Conan repositories, please check the [dedicated
section](https://docs.conan.io/2//tutorial/conan_repositories.html.md#conan-repositories).

```text
$ conan upload -h
usage: conan upload [-h] [-f FORMAT] [--out-file OUT_FILE]
                    [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                    [-cc CORE_CONF] [-p PACKAGE_QUERY] -r REMOTE
                    [--only-recipe] [--force] [--check] [-c] [--dry-run]
                    [--allow-disabled] [-l LIST] [-m METADATA]
                    [pattern]

Upload packages to a remote.

By default, all the matching references are uploaded (all revisions).
By default, if a recipe reference is specified, it will upload all the revisions for all the
binary packages, unless --only-recipe is specified. You can use the "latest" placeholder at the
"reference" argument to specify the latest revision of the recipe or the package.

positional arguments:
  pattern               A pattern in the form
                        'pkg/version#revision:package_id#revision', e.g:
                        "zlib/1.2.13:*" means all binaries for zlib/1.2.13. If
                        revision is not specified, it is assumed latest one.

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Select the output format: json
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
  -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                        Only upload packages matching a specific query. e.g:
                        os=Windows AND (arch=x86 OR compiler=gcc)
  -r REMOTE, --remote REMOTE
                        Upload to this specific remote
  --only-recipe         Upload only the recipe/s, not the binary packages.
  --force               Force the upload of the artifacts even if the revision
                        already exists in the server
  --check               Perform an integrity check, using the manifests,
                        before upload
  -c, --confirm         Upload all matching recipes without confirmation
  --dry-run             Do not execute the real upload (experimental)
  --allow-disabled      Allow uploading to disabled remote
  -l LIST, --list LIST  Package list file
  -m METADATA, --metadata METADATA
                        Upload the metadata, even if the package is already in
                        the server and not uploaded

```

The `conan upload` command can upload packages to 1 server repository specified by the `-r=myremote` argument.

It has 2 possible and mutually exclusive inputs:
- The `conan upload <pattern>` pattern-based matching of recipes, with a pattern similar to the `conan list <pattern>`.
- The `conan upload --list=<pkglist>` that will upload the artifacts specified in the `pkglist` json file

If the `--format=json` formatter is specified, the result will be a “PackageList”, compatible with other Conan commands, for example the `conan remove` command, so it is possible to concatenate different commands using the generated json file. The resulting “PackageList” also includes the URLs where each file has been or will be uploaded, providing additional context for automation or inspection purposes. See the [Packages Lists examples](https://docs.conan.io/2//examples/commands/pkglists.html.md#examples-commands-pkglists).

The `--dry-run` argument will prepare the packages for upload, zip files if necessary, check in the server to see what needs to be uploaded and what is already in the server, but it will not execute the actual upload.

## Upload policies and efficient uploads

The `conan upload` commmand performs a check in the server to see if the local Conan packages in the cache already exist in the server or not. This is done by comparing the local `recipe-revision` and `package-revision` against the existing server ones. If they already exist in the server, the actual upload can be skipped, as the revision system uses the artifacts checksums, so it is guaranteed that the same artifacts already exist in the server.

If for some reason it is desired to force the full transfer of the artifacts from the local filesystem to the server again, and assuming the server has overwrite/delete permissions (necessary for an overwrite), then the `conan upload --force` can be used. That will force a new upload to the server.

Uploading an older existing revision to the server with `--force` doesn’t guarantee that such a revision will be made the latest one in the server, that is to update its timestamp to the current time. This behavior might depend on the server configuration.
For example in **Artifactory** the default configuration, due to historic reasons and Conan 1.X compatibility the behavior is as follows:

- If the `conan upload --force` happens before 60 seconds of the original upload, it is not made latest.
- If the `conan upload --force` happens after 60 seconds of the original upload, it is made latest.

The time limit can be configured with `artifactory.conan.index.timestamp.override.threshold.millis`, for example, to completely opt-out of this behavior and `conan upload --force` not changing the revision timestamp and consequently never making it the latest, it is possible to define `artifactory.conan.index.timestamp.override.threshold.millis=Long.MAX_VALUE`.

#### NOTE
In general, the `conan upload --force` argument shouldn’t be used in regular production pipelines. It is more intended for exceptional cases, like fixing some corrupted package.

## Upload configurations

There are different configurations and parameters that can affect the uploads:

- The recipe `upload_policy = "skip"` attribute is intended to skip the upload of binaries for that package, only the recipe will ever be uploaded. This attribute is used for exceptional cases where a package can only be built in the installation machine, for example “system” package wrappers
- `core.scm:local_url`: By default allows to store local folders as remote url, but not upload them. Use ‘allow’ for allowing upload and ‘block’ to completely forbid it. By default `scm` captures that are not reproducible, that is, that point to a local folder, will be blocked at upload time. This configuration can avoid that block, but please note that this is not recommended in the general case, as those packages won’t be able to be reproduce later, as their sources are pointing to a local machine folder that will dissapear.
- `core.sources:upload_url`: Remote URL to upload backup sources to. If the “backup-sources” system is configured with this URL, then the `conan upload` command will also upload the associated downloaded sources to this backup-sources repository.
- `core.upload:compression_format`: The compression format used when uploading Conan packages. Possible values: ‘zst’, ‘xz’, ‘gz’ (default=gz)\`. Recall that `zst` requires at least Python>=3.14 to work. With this configuration, it is possible to change the compression format for Conan stored artifacts.
- `core.upload:parallel`: Number of concurrent threads to upload packages. Using this conf, it is possible to upload packages in parallel. By default, or when set to a value less than `2`, no parallelization will take place, and any other value will be the number of parallel threads to utilize.
- `core.upload:retry`: (int, default: 1) Number of retries in case of failure when uploading to Conan server
- `core.upload:retry_wait`: (int, default: 5s) Seconds to wait between upload attempts to Conan server

#### SEE ALSO
- [Uploading packages tutorial](https://docs.conan.io/2//tutorial/conan_repositories/uploading_packages.html.md#uploading-packages)
- [Working with Conan repositories](https://docs.conan.io/2//tutorial/conan_repositories.html.md#conan-repositories)
- [Managing remotes with conan remote command](https://docs.conan.io/2//reference/commands/remote.html.md#reference-commands-remote)
- [Uploading metadata files](https://docs.conan.io/2//devops/metadata.html.md#devops-metadata).
