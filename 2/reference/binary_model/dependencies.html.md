<a id="reference-binary-model-dependencies"></a>

# The effect of dependencies on `package_id`

When a given package depends on a another package and uses it, the effect of dependencies can be different based on the package types:

For libraries:

- **Non-embed mode**: When an application or a shared library depends on another shared library, or when a static library depends on another static library, the “consumer” library does not do a copy of the binary artifacts of the “dependency” at all. We call it non-embed mode, the dependency binaries are not being linked or embedded in the consumer. This assumes that there are not inlined functionalities in the dependency headers, and the headers are pure interface and not implementation.
- **Embed mode**: When an application or a shared library depends on a header-only or a static-library, the dependencies binaries are copied or partially copied (depending on the linker) in the consumer binary. Also when a static library depends on a header-only library, it is considered that there will be embedding in the consumer binary of such headers, as they will also contain the implementation, it is impossible that they are a pure interface.

For applications (`tool_requires`):

- **Build mode**: When some package uses a `tool_requires` of another package, the binary artifacts in the dependency are never copied or embedded.

## Non-embed mode

When we list the binaries of a package like `openssl` with dependencies:

```bash
$ conan list openssl/3.1.2:* -r=conancenter
conancenter
  openssl
    openssl/3.1.2
      revisions
        8879e931d726a8aad7f372e28470faa1 (2023-09-13 18:52:54 UTC)
          packages
            0348efdcd0e319fb58ea747bb94dbd88850d6dd1  # package_id
              info
                options
                  shared: True
                ...
                requires
                  zlib/1.3.Z
```

This binary was a `shared` library, linking with `zlib` as a shared library.
This means it was using “non-embed” mode. The default of non-embed mode is `minor_mode`, which means:

- All `zlib` patch versions will be mapped to the same `zlib/1.3.Z`. This means that if our `openssl/3.1.2` package binary `0348efdcd0e319fb58ea747bb94dbd88850d6dd1` binary is considered binary compatible with all `zlib/1.3.Z` versions (for any `Z`), and will not require to rebuild the `openssl` binary.
- New `zlib` minor versions, like `zlib/1.4.0` will result in a “minor-mode” identifier like `zlib/1.4.Z`, and then, it will require a new `openssl/3.1.2` package binary, with a new `package_id`

#### NOTE
There was a bug in Conan versions previous to Conan 2.28 in this **non-embed mode**, in which transitive dependencies could affect the `package_id` of consumers,
even if they were not direct dependencies, they were not being embedded, and they were not propagating headers to it. This was causing sub-optimal behavior, that could require
some unnecessary builds from source for new `package_ids`. To avoid breaking existing users, this bug fix was introduced as opt-in via
policies:

- If a recipe defines `required_conan_version = ">=2.28"` or higher, it will automatically enable the new fixed `package_id` computation.
  Recipes that don’t update their required Conan version will still use the older `package_id`.
- If the global configuration in `global.conf` defines the `core:policies=["required_conan_version>=2.28"]` it will have the same behavior,
  enabling this bugfix for all packages. See the [documentation for policies](https://docs.conan.io/2//reference/policies.html.md#reference-policies) for more information.
- The recommendation is to activate the new behavior via policies. It will save resources like build time, and it will also be more future-proof,
  future Conan versions might enable this behavior unconditionally.

## Embed mode

The following commands illustrate the concept of embed-mode. We create a `dep/0.1` package with a static library, and then we create a `app/0.1` package with an executable that links with static library inside `dep/0.1`. We can use the `conan new` command for quickly creating these two packages:

```bash
$ mkdir dep && cd dep
$ conan new cmake_lib -d name=dep -d version=0.1
$ conan create . -tf=""
$ cd .. && mkdir app && cd app
$ conan new cmake_exe -d name=app -d version=0.1 -d requires=dep/0.1
$ conan create .
dep/0.1: Hello World Release!
...
app/0.1: Hello World Release!
```

If we now list the `app/0.1` binaries, we will see the binary just created:

```bash
  $ conan list app/0.1:*
  Local Cache
    app/0.1
      revisions
        632e236936211ac2293ec33339ce582b (2023-09-25 22:34:17 UTC)
          packages
            3ca530d20914cf632eb00efbccc564da48190314
              info
                settings
                  ...
                requires
                  dep/0.1#d125304fb1fb088d5b92d4f8135f4dff:9bdee485ef71c14ac5f8a657202632bdb8b4482b
```

It is now visible that the `app/0.1` package-id depends on the full identifier of the `dep/0.1` dependency, that includes both its recipe revision and `package_id`.

If we do a change now to the `dep` code, and re-create the `dep/0.1` package , even if we don’t bump the version, it will create a new recipe revision:

```bash
$ cd ../dep
# Change the "src/dep.cpp" code to print a new message, like "Hello Moon"
$ conan create . -tf=""
# New recipe revision dep/0.1#1c90e8b8306c359b103da31faeee824c
```

So if we try now to install `app/0.1` binary, it will fail with a “missing binary” error:

```text
  $ conan install --requires=app/0.1
  ERROR: Missing binary: app/0.1:ef2b5ed33d26b35b9147c90b27b217e2c7bde2d0

  app/0.1: WARN: Can't find a 'app/0.1' package binary 'ef2b5ed33d26b35b9147c90b27b217e2c7bde2d0' for the configuration:
  [settings]
  ...
  [requires]
  dep/0.1#1c90e8b8306c359b103da31faeee824c:9bdee485ef71c14ac5f8a657202632bdb8b4482b

  ERROR: Missing prebuilt package for 'app/0.1'
```

As the `app` executable links with the `dep` static library, it needs to be rebuilt to include the latest changes, even if `dep/0.1` didn’t bump its version, `app/0.1` depends on “embed-mode” on `dep/0.1`, so it wil use down to the `package_id` of such dependency identifier.

Let’s build the new `app/0.1` binary:

```bash
  $ cd ../app
  $ conan create .
  dep/0.1: Hello Moon Release!  # Message changed to Moon
  ...
  app/0.1: Hello World Release!
```

Now we will have two `app/0.1` different binaries:

```bash
  $ conan list "app/0.1:*"
  Local Cache
    app
      app/0.1
        revisions
          632e236936211ac2293ec33339ce582b (2023-09-25 22:49:32 UTC)
            packages
              3ca530d20914cf632eb00efbccc564da48190314
                info
                  settings
                    ...
                  requires
                    dep/0.1#d125304fb1fb088d5b92d4f8135f4dff:9bdee485ef71c14ac5f8a657202632bdb8b4482b
              ef2b5ed33d26b35b9147c90b27b217e2c7bde2d0
                info
                  settings
                    ...
                  requires
                    dep/0.1#1c90e8b8306c359b103da31faeee824c:9bdee485ef71c14ac5f8a657202632bdb8b4482b
```

We will have these two different binaries, one of them linking with the first revision of the `dep/0.1` dependency (with the “Hello World” message), and the other binary with the other `package_id` linked with the second revision of the `dep/0.1` dependency (with the “Hello Moon” message).

The above described mode is called `full_mode`, and it is the default for the `embed_mode`.
