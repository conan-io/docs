<a id="conan-tools-scm-git"></a>

# Git

The `Git` helper is a thin wrapper over the `git` command. It can be used for different purposes:

- Obtaining the current tag in the `set_version()` method to assign it to `self.version`
- Clone sources in third-party or open source package recipes in the `source()` method (in general, doing a `download()` or `get()` to fetch release tarballs will be preferred)
- Capturing the “scm” coordinates (url, commit) of your own package sources in the `export()` method, to be able to reproduce a build from source later, retrieving the code in the `source()` method. See the [example of git-scm capture](https://docs.conan.io/2//examples/tools/scm/git/capture_scm/git_capture_scm.html.md#examples-tools-scm-git-capture).

The `Git()` constructor receives the current folder as argument, but that can be changed if necessary, for example, to clone the sources of some repo in `source()`:

```python
def source(self):
   git = Git(self)  # by default, the current folder "."
   git.clone(url="<repourl>", target="target") # git clone url target
   # we need to cd directory for next command "checkout" to work
   git.folder = "target"                       # cd target
   git.checkout(commit="<commit>")             # git checkout commit
```

An alternative, equivalent approach would be:

```python
def source(self):
   git = Git(self, "target")
   # Cloning in current dir, not a children folder
   git.clone(url="<repourl>", target=".")
   git.checkout(commit="<commit>")
```

### *class* Git(conanfile, folder='.', excluded=None)

Git is a wrapper for several common patterns used with *git* tool.

* **Parameters:**
  * **conanfile** – Conanfile instance.
  * **folder** – Current directory, by default `.`, the current working directory.
  * **excluded** – Files to be excluded from the “dirty” checks. It will compose with the
    configuration `core.scm:excluded` (the configuration has higher priority).
    It is a list of patterns to `fnmatch`.

#### run(cmd, hidden_output=None)

Executes `git <cmd>`

* **Returns:**
  The console output of the command.

#### get_commit(repository=False)

* **Parameters:**
  **repository** – By default gets the commit of the defined folder, use repo=True to get
  the commit of the repository instead.
* **Returns:**
  The current commit, with `git rev-list HEAD -n 1 -- <folder>`.
  The latest commit is returned, irrespective of local not committed changes.

#### get_remote_url(remote='origin')

Obtains the URL of the remote git remote repository, with `git remote -v`

**Warning!**
Be aware that This method will get the output from `git remote -v`.
If you added tokens or credentials to the remote in the URL, they will be exposed.
Credentials shouldn’t be added to git remotes definitions, but using a credentials manager
or similar mechanism. If you still want to use this approach, it is your responsibility
to strip the credentials from the result.

* **Parameters:**
  **remote** – Name of the remote git repository (‘origin’ by default).
* **Returns:**
  URL of the remote git remote repository.

#### commit_in_remote(commit, remote='origin')

Checks that the given commit exists in the remote, with `branch -r --contains <commit>`
and checking an occurrence of a branch in that remote exists.

* **Parameters:**
  * **commit** – Commit to check.
  * **remote** – Name of the remote git repository (‘origin’ by default).
* **Returns:**
  True if the given commit exists in the remote, False otherwise.

#### is_dirty(repository=False)

Returns if the current folder is dirty, running `git status -s`
The `Git(..., excluded=[])` argument and the `core.scm:excluded` configuration will
define file patterns to be skipped from this check.

* **Parameters:**
  **repository** – By default checks if the current folder is dirty. If repository=True
  it will check the root repository folder instead, not the current one.
* **Returns:**
  True, if the current folder is dirty. Otherwise, False.

#### get_url_and_commit(remote='origin', repository=False)

This is an advanced method, that returns both the current commit, and the remote repository url.
This method is intended to capture the current remote coordinates for a package creation,
so that can be used later to build again from sources from the same commit. This is the behavior:

* If the repository is dirty, it will raise an exception. Doesn’t make sense to capture coordinates
  of something dirty, as it will not be reproducible. If there are local changes, and the
  user wants to test a local conan create, should commit the changes first (locally, not push the changes).
* If the repository is not dirty, but the commit doesn’t exist in the given remote, the method
  will return that commit and the URL of the local user checkout. This way, a package can be
  conan create created locally, testing everything works, before pushing some changes to the remote.
* If the repository is not dirty, and the commit exists in the specified remote, it will
  return that commit and the url of the remote.

**Warning!**
Be aware that This method will get the output from `git remote -v`.
If you added tokens or credentials to the remote in the URL, they will be exposed.
Credentials shouldn’t be added to git remotes definitions, but using a credentials manager
or similar mechanism. If you still want to use this approach, it is your responsibility
to strip the credentials from the result.

* **Parameters:**
  * **remote** – Name of the remote git repository (‘origin’ by default).
  * **repository** – By default gets the commit of the defined folder, use repo=True to get
    the commit of the repository instead.
* **Returns:**
  (url, commit) tuple

#### get_repo_root()

Get the current repository top folder with `git rev-parse --show-toplevel`

* **Returns:**
  Repository top folder.

#### clone(url, target='', args=None, hide_url=True)

Performs a `git clone <url> <args> <target>` operation, where target is the target directory.

* **Parameters:**
  * **url** – URL of remote repository.
  * **target** – Target folder.
  * **args** – Extra arguments to pass to the git clone as a list.
  * **hide_url** – Hides the URL from the log output to prevent accidental
    credential leaks. Can be disabled by passing `False`.

#### fetch_commit(url, commit, hide_url=True)

Experimental: does a single commit fetch and checkout, instead of a full clone,
should be faster.

* **Parameters:**
  * **url** – URL of remote repository.
  * **commit** – The commit ref to checkout.
  * **hide_url** – Hides the URL from the log output to prevent accidental
    credential leaks. Can be disabled by passing `False`.

#### checkout(commit)

Checkouts the given commit using `git checkout <commit>`.

* **Parameters:**
  **commit** – Commit to checkout.

#### included_files()

Run `git ls-files --full-name --others --cached --exclude-standard` to the get the list
: of files not ignored by `.gitignore`

* **Returns:**
  List of files.

#### coordinates_to_conandata(repository=False)

Capture the “url” and “commit” from the Git repo, calling `get_url_and_commit()`, and then
store those in the `conandata.yml` under the “scm” key. This information can be
used later to clone and checkout the exact source point that was used to create this
package, and can be useful even if the recipe uses `exports_sources` as mechanism to
embed the sources.

* **Parameters:**
  **repository** – By default gets the commit of the defined folder, use repository=True to get
  the commit of the repository instead.

#### checkout_from_conandata_coordinates()

Reads the “scm” field from the `conandata.yml`, that must contain at least “url” and
“commit” and then do a `clone(url, target=".")`, `fetch <commit>`, followed by a `checkout(commit)`.
