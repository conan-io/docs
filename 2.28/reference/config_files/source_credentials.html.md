<a id="reference-config-files-source-credentials"></a>

# source_credentials.json

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

When a `conanfile.py` recipe downloads some sources from other servers with the `download()` or the `get()` helpers like:

```python
def source(self):
    # Immutable source .zip
    download(self, f"https://server/that/need/credentials/files/tarballname-{self.version}.zip", "downloaded.zip")
    # Also the ``get()`` function, as it internally calls ``download()``
```

These downloads would be typically anonymous for open-source third party libraries in the internet, but it
is also possible that some proprietary code in a private organization or provided by a vendor would require
some kind of authentication.

For this purpose the `source_credentials.json` file can be provided in the Conan cache. This file
has the following format, in which every `credentials` entry should have a `url` that defines the
URL that should match the recipe one. If the recipe URL starts with the given one in the credentials files,
then the credentials will be injected. If the file provides multiple credentials for multiple URLs, they
will be evaluated in order until the first match happens. If no match is found, no credentials will be injected.
A custom [auth plugin](https://docs.conan.io/2//reference/extensions/authorization_plugins.html.md#reference-extensions-authorization-plugin) can also be used to retrieve credentials
directly from your own secrets manager.

It has to be noted that the `source_credentials` applies only to files downloaded with the `tools.files`
`download()` and `get()` helpers, but it won’t be used in other cases. To provide credentials for Conan repos,
the `credentials.json` file should be used instead, see [credentials.json](https://docs.conan.io/2//reference/config_files/credentials.html.md#reference-config-files-credentials).

```json
{
    "credentials": [
        {
            "url": "https://server/that/need/credentials",
            "token": "mytoken"
        }
    ]
}
```

Using the `token` field, will add an `Authorization = Bearer {token}` header. This would be the preferred
way of authentication, as it is typically more secure than using user/password.

If for some reason HTTP-Basic auth with user/password is necessary it can be provided with the `user` and
`password` fields:

```json
{
    "credentials": [
        {
            "url": "https://server/that/need/credentials",
            "user": "myuser",
            "password": "mypassword"
        }
    ]
}
```

As a general rule, hardcoding secrets like passwords in files is strongly discouraged. To avoid it, the
`source_credentials.json` file is always rendered as a jinja template, so it can do operations like
getting environment variables `os.getenv()`, allowing the secrets to be configured at the system or CI
level:

```jinja
{% set mytk = os.getenv('mytoken') %}
{
    "credentials": [
        {
            "url": "https://server/that/need/credentials",
            "token": "{{mytk}}"
        }
    ]
}
```

Note that `mytoken` environment variable must be defined, otherwise `mytk=None`, and
that will translate to a literal `token="None"` that is obviously an invalid token and
will cause an authentication failure. If you want to condition the existence of the credential
itself, you need to protect the whole credential entry (both `url`, and `token`) with a
`{% if mytk %}-{% endif %}` block.

In some special cases, the server might need some specific custom headers. You can also specify them using a `headers` dictionary.

```json
{
    "credentials": [
        {
            "url": "https://server/that/need/credentials",
            "token": "mytoken",
            "headers": {"my-header-1": "my-value-1", "my-header-2": "my-value-2"}
        }
    ]
}
```

#### NOTE
**Best practices**

- Avoid using URLs that encode tokens or user/password authentication in the `conanfile.py` recipes. These URLs can easily leak into logs, and
  can be more difficult to fix in case of credentials changes (this is also valid for Git repositories URLs and clones,
  better use other Git auth mechanisms like ssh-keys)

#### SEE ALSO
- [How to use your own secrets manager for your source server logins](https://docs.conan.io/2//reference/extensions/authorization_plugins.html.md#reference-extensions-authorization-plugin).
