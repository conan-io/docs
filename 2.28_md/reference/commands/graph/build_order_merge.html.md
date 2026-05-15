# conan graph build-order-merge

```text
$ conan graph build-order-merge -h
usage: conan graph build-order-merge [-h] [-f FORMAT] [--out-file OUT_FILE]
                                     [-v [{quiet,error,warning,notice,status,verbose,debug,v,trace,vv}]]
                                     [-cc CORE_CONF] [--file [FILE]]
                                     [--reduce]

Merge more than 1 build-order file.

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
  --file [FILE]         Files to be merged
  --reduce              Reduce the build order, output only those to build.
                        Use this only if the result will not be merged later
                        with other build-order

```

As described in the `conan graph build-order` command, there are 2 types of order `recipe` and `configuration`.
Only build-orders of the same type can be merged together, otherwise the command will return an error.

Note that only build-orders that haven’t been reduced with `--reduce` can be merged.

The result of merging the different input files can be also reduced with the `conan graph build-order-merge --reduce`
argument, and the behavior will be the same, leave only the elements that need to be built from source.

When 2 or more “build-order” files are merged, the resulting merge contains a `profiles` section like:

```json
"profiles": {
    "build_order_win": {
        "args": "-pr:h=\"profile1\" -s:h=\"os=Windows\" ..."
    },
    "build_order_nix": {
        "args": "-pr:h=\"profile2\" -s:h=\"os=Linux\" ..."
    }
}
```

With the `build_order_win` and `build_order_nix` being the “build-order” filenames that were used as inputs to the merge, and which will be referenced in the `filenames` field of every `package` in the build order. This way, it is easier to obtain the necessary command line arguments to build a specific package binary in the build-order when building multiple configurations.

Note that when a merged build order containing multilpe `filenames` something like:

```json
{
    "package_id": "efa83b160a55b033c4ea706ddb980cd708e3ba1b",
    "context": "build",
    "binary": "Build",
    "filenames": [
        "build_order_win",
        "build_order_nix"
    ],
    "build_args": "--tool-requires=dep/0.1 --build=dep/0.1",
    "info": {
        "settings": {
            "build_type": "Release"
        }
    }
}

"profiles": {
    "build_order_win": {
        "args": "-pr:h=\"profile1\" -s:h=\"os=Windows\" ..."
    },
    "build_order_nix": {
        "args": "-pr:h=\"profile2\" -s:h=\"os=Linux\" ..."
    }
}
```

Then, the `filename` to be used is the first one, in this case `build_order_win`, because the `context` and `build_args` arguments matches this profile information. The other filenames are provided as a reference to which other individual build-order files had this `package_id` listed for build.
