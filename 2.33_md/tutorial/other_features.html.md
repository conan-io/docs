<a id="other-important-features"></a>

# Other important Conan features

## python_requires

It is possible to reuse code from other recipes using the [python_requires feature](https://docs.conan.io/2//reference/extensions/python_requires.html.md#reference-extensions-python-requires).

If you maintain many recipes for different packages that share some common logic and you don’t want to repeat the code in every recipe, you can put that common code in a Conan `conanfile.py`, upload it to your server, and have other recipe conanfiles do a `python_requires = "mypythoncode/version"` to depend on it and reuse it.

<a id="other-important-features-pkglist"></a>

## Packages lists

It is possible to manage a list of packages, recipes and binaries together with the “packages-list” feature.
Several commands like `upload`, `download`, and `remove` allow receiving a list of packages file as an input, and they can do their operations over that list.
A typical use case is to “upload to the server the packages that have been built in the last `conan create`”, which can be done with:

```bash
$ conan create . --format=json > build.json
$ conan list --graph=build.json --graph-binaries=build --format=json > pkglist.json
$ conan upload --list=pkglist.json -r=myremote -c
```

See the [examples in this section](https://docs.conan.io/2//examples/commands/pkglists.html.md#examples-commands-pkglists).

## Removing unused packages from the cache

#### WARNING
The (lru) least recently used feature is in **preview**.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

The Conan cache does not implement any automatic expiration policy, so its size will be always increasing unless
packages are removed or the cache is removed from time to time. It is possible to remove recipes and packages
that haven’t been used recently, while keeping those that have been used in a given time period (Least Recently Used LRU policy).
This can be done with the `--lru` argument to `conan remove` and `conan list` commands:

```bash
# remove all binaries (but not recipes) not used in the last 4 weeks
$ conan remove "*:*" --lru=4w -c
# remove all recipes that have not been used in the last 4 weeks (with their binaries)
$ conan remove "*" --lru=4w -c
```

Note that the LRU time follows the rules of the `remove` command. If we are removing recipes with a `"*"` pattern, only
the LRU times for recipes will be checked. If a recipe has been recently used, it will keep all the binaries, and if the recipe
has not been recently used, it will remove itself and all its binaries. If we use a `"*:*"` pattern, it will check for binaries only,
and remove those unused, but always leaving the recipe.

Using `conan list` first (take into account that `conan list` do not default to list all revisions, as opposed to `remove`,
so it is necessary to explicit the `#*` to select all revisions if that is the intention) it is possible to create a list of
least recently used packages:

```bash
# List all unused (last 4 weeks) recipe revisions
$ conan list "*#*" --lru=4w --format=json > old.json
# Remove those recipe revisions (and their binaries)
$ conan remove --list=old.json -c
```

See commands help [conan remove](https://docs.conan.io/2//reference/commands/remove.html.md#reference-commands-remove) and [conan list](https://docs.conan.io/2//reference/commands/list.html.md#reference-commands-list).
