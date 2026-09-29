# Package pipeline: multi configuration using lockfiles

In the previous example, we built both `Debug` and `Release` package binaries for `ai/1.1.0`. In real world scenarios the binaries to build would be different platforms (Windows, Linux, embedded), different architectures, and very often it will not be possible to build them in the same machine, requiring different computers.

The previous example had an important assumption: the dependencies of `ai/1.1.0` do not change at all during the building process. In many scenarios, this assumption will not hold, for example if there are any other concurrent CI jobs, and one succesfull job publishes a new `mathlib/1.1` version in the `develop` repo.

Then it is possible that one build of `ai/1.1.0`, for example, the one running in the Linux servers starts earlier and uses the previous `mathlib/1.0` version as dependency, while the Windows servers start a bit later, and then their build will use the recent `mathlib/1.1` version as dependency. This is a very undesirable situation, having binaries for the same `ai/1.1.0` version using different dependencies versions. This can lead in later graph resolution problems, or even worse, get to the release with different behavior for different platforms.

The way to avoid this discrepancy in dependencies is to force the usage of the same dependencies versions and revisions, something that can be done with [lockfiles](https://docs.conan.io/2//tutorial/versioning/lockfiles.html.md#tutorial-versioning-lockfiles).

Creating and applying lockfiles is relatively straightforward. The process of creating and promoting the configurations will be identical to the previous section, but just applying the lockfiles.

## Creating the lockfile

Let’s make sure as usual that we start from a clean state:

```bash
$ conan remove "*" -c  # Make sure no packages from last run
```

Then we can create the lockfile `conan.lock` file:

```bash
# Capture a lockfile for the Release configuration
$ conan lock create . -s build_type=Release --lockfile-out=conan.lock
# extend the lockfile so it also covers the Debug configuration
# in case there are Debug-specific dependencies
$ conan lock create . -s build_type=Debug --lockfile=conan.lock --lockfile-out=conan.lock
```

Note that different configurations, using different profiles or settings could result in different dependency graphs. A lockfile file can be used to lock the different configurations, but it is important to iterate the different configurations/profiles and capture their information in the lockfile.

#### NOTE
The `conan.lock` is the default argument, and if a `conan.lock` file exists, it might be automatically used by `conan install/create` and other graph commands. This can simplify many of the commands, but this tutorial is showing the full explicit commands for clarity and didactical reasons.

The `conan.lock` file can be inspected, it will be something like:

```json
{
    "version": "0.5",
    "requires": [
        "mathlib/1.0#f2b05681ed843bf50d8b7b7bdb5163ea%1724319985.398"
    ],
    "build_requires": [],
    "python_requires": [],
    "config_requires": []
}
```

As we can see, it is locking the `mathlib/1.0` dependency version and revision.

With the lockfile, creating the different configurations is exactly the same, but providing the `--lockfile=conan.lock` argument to the `conan create` step, it will guarantee that `mathlib/1.0#f2b05681ed843bf50d8b7b7bdb5163ea` will always be the exact dependency used, irrespective if there exist new `mathlib/1.1` versions or new revisions available. The following builds could be launched in parallel but executed at different times, and still they will always use the same `mathlib/1.0` dependency:

```bash
$ cd ai  # If you were not inside "ai" folder already
$ conan create . --build="missing:ai/*" --lockfile=conan.lock -s build_type=Release --format=json > graph.json
$ conan list --graph=graph.json --graph-binaries=build --format=json > built.json
$ conan remote enable packages
$ conan upload -l=built.json -r=packages -c --format=json > uploaded_release.json
$ conan remote disable packages
```

```bash
$ conan create . --build="missing:ai/*" --lockfile=conan.lock -s build_type=Debug --format=json > graph.json
$ conan list --graph=graph.json --graph-binaries=build --format=json > built.json
$ conan remote enable packages
$ conan upload -l=built.json -r=packages -c --format=json > uploaded_debug.json
$ conan remote disable packages
```

Note the only modification to the previous example is the addition of `--lockfile=conan.lock`. The promotion will also be identical to the previous one:

```bash
# aggregate the package list
$ conan pkglist merge -l uploaded_release.json -l uploaded_debug.json --format=json > uploaded.json

$ conan remote enable packages
$ conan remote enable products
# Promotion using Conan download/upload commands
# (slow, can be improved with art:promote custom command)
$ conan download --list=uploaded.json -r=packages --format=json > promote.json
$ conan upload --list=promote.json -r=products -c
$ conan remote disable packages
$ conan remote disable products
```

And the final result will be the same as in the previous section, but this time just with the guarantee that both `Debug` and `Release` binaries were built using exactly the same `mathlib` version:

Now that we have the new `ai/1.1.0` binaries in the `products` repo, we can consider the `packages pipeline` finished and move to the next section, and build and check our products to see if this new `ai/1.1.0` version integrates correctly.
