<a id="contribute-conancenter"></a>

# Contributing to Conan Center

#### NOTE
**Default Remote Update in Conan 2.9.2**

Starting from **Conan version 2.9.2**, the default remote has been changed to
https://center2.conan.io. The previous default remote https://center.conan.io is
now frozen and will no longer receive updates. It is recommended to update your remote
configuration to use the new default remote to ensure access to the latest recipes and
package updates (for more information, please read this [post](https://blog.conan.io/2024/09/30/Conan-Center-will-stop-receiving-updates-for-Conan-1.html)).

If you still have the deprecated remote configured as the default, please update using
the following command:

```bash
conan remote update conancenter --url="https://center2.conan.io"
```

Contribution of packages to ConanCenter is done via pull requests to the Github repository
in [https://github.com/conan-io/conan-center-index](https://github.com/conan-io/conan-center-index). The C3I (ConanCenter Continuous
Integration) service will build binaries automatically from those pull requests, and once
merged, will upload them to ConanCenter package repository.

Read more about how to [submit a pull request to conan-center-index](https://github.com/conan-io/conan-center-index/tree/master/docs/adding_packages) source
repository.
