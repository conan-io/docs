<a id="reference-config-files-remotes-json"></a>

# remotes.json

The **remotes.json** file is located in the Conan user home directory, e.g.,  *[CONAN_HOME]/remotes.json*.

The default file created by Conan looks like this:

```json
{
 "remotes": [
  {
   "name": "conancenter",
   "url": "https://center2.conan.io",
   "verify_ssl": true
  }
 ]
}
```

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

Essentially, it tells Conan where to list/upload/download the recipes/binaries from the remotes specified by their URLs.

The fields for each remote are:

* `name` (Required, `string` value): Name of the remote. This name will be used in commands
  like [conan list](https://docs.conan.io/2//reference/commands/list.html.md#reference-commands-list), e.g., **conan list zlib/1.3.1 --remote my_remote_name**.
* `url` (Required, `string` value): indicates the URL to be used by Conan to search for the recipes/binaries.
* `verify_ssl` (Required, `bool` value): Verify SSL certificate of the specified url.
* `disabled` (Optional, `bool` value, `false` by default): If the remote is enabled or not to be used by commands
  like search, list, download and upload. Notice that a disabled remote can be used to authenticate against it even
  if it’s disabled.
* `allowed_packages`: (Optional, `list` of `string` values): List of recipes that are allowed to be
  downloaded from this remote. If the list is empty or not present, all packages are allowed. Uses fnmatch rules.
* `recipes_only`: (Optional, `bool` value, `false` by default): If true, only recipes will be
  downloaded from this remote, no binaries will be downloaded.

#### SEE ALSO
- [How to manage SSL (TLS) certificates](https://docs.conan.io/2//reference/config_files/global_conf.html.md#reference-config-files-global-conf-ssl-certificates)
- [How to manage remotes.json through CLI: conan remotes](https://docs.conan.io/2//reference/commands/remote.html.md#reference-commands-remote).
- [How to use your own secrets manager for Conan remotes logins](https://docs.conan.io/2//reference/extensions/authorization_plugins.html.md#reference-extensions-authorization-plugin).
