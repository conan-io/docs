<a id="devops-package-promotions"></a>

# Package promotions

Package promotions are the recommended devops practice to handle quality, maturity or stages of packages
in different technologies, and of course, also for Conan packages.

The principle of package promotions is that there are multiple server package repositories defined and
packages are uploaded and copied among repositories depending on the stage. For
example we could have two different server package repositories called “testing” and “release”:

#### NOTE
**Best practices**

- Using different `user/channel` to try to denote maturity is strongly discouraged. It was described in the early
  Conan 1 days years ago, before the possibility of having multiple repositories, but it shouldn’t be used anymore.
- Packages should be completely immutable across pipelines and stages, a package cannot rename or change its `user/channel`,
  and re-building it from source to have a new `user/channel` is also a strongly discourage devops practice.

Between those repositories there will be some quality gates. In our case, some packages will be
put in the “testing” repository, for the QA team to test them, for example `zlib/1.3.1` and `openssl/3.2.2`:

When the QA team tests and approves these packages, they can be promoted to the “release” repository.
Basically, a promotion is a copy of the packages, including all the artifacts and metadata from the
“testing” to the “release” repository.

There are different ways to implement and execute a package promotion. Artifactory has some APIs that can be
used to move individual files or folders. The [Conan extensions repository](https://github.com/conan-io/conan-extensions)
contains the `conan art:promote` command that can be used to promote Conan “package lists” from one
server repository to another repository.

If we have a package list `pkglist.json` that contains the above `zlib/1.3.1` and `openssl/3.2.2` packages, then
the command would look like:

```bash
$ conan art:promote pkglist.json --from=testing --to=release --url=https://<url>/artifactory --user=<user> --password=<password>
```

Note that the `conan art:promote` command doesn’t work with ArtifactoryCE, Pro editions of Artifactory are needed.
The promote functionality can be implemented in these cases with a simple download+upload flow:

```bash
# Promotion using Conan download/upload commands
# (slow, can be improved with art:promote custom command)
$ conan download --list=promote.json -r=testing --format=json > downloaded.json
$ conan upload --list=downloaded.json -r=release -c
```

After the promotion from “testing” to “release” repository, the packages would be like:

#### NOTE
**Best practices**

- In modern package servers such as Artifactory package artifacts are **deduplicated**, that is, they do not
  take any extra storage when they are copied in different locations, including different repositories.
  The **deduplication** is checksum based, so the system is also smart to avoid re-uploading existing artifacts.
  This is very important for the “promotions” mechanism: this mechanism is only copying some metadata, so
  it can be very fast and it is storage efficient. Pipelines can define as many repositories and promotions
  as necessary without concerns about storage costs.
- Promotions can also be done in JFrog platform with `Release Bundles`. The [Conan extensions repository](https://github.com/conan-io/conan-extensions)
  also contains one command to generate a release bundle (that can be promoted using the Artifatory API).

#### SEE ALSO
- [Using package lists examples](https://docs.conan.io/2//examples/commands/pkglists.html.md#examples-commands-pkglists)
- [Promotions usage in CI](https://docs.conan.io/2//ci_tutorial/tutorial.html.md#ci-tutorial)
