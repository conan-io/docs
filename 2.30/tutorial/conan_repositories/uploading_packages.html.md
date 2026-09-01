<a id="uploading-packages"></a>

# Uploading Packages

In the previous section, we learned how to [set up a Conan repository](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes.html.md#setting-up-conan-remotes). Now we will go through the process of uploading both recipes
and binaries to this remote and store them for later use on another machine, project, or
for sharing purposes.

First, check if the remote you want to upload to is already in your current remote list:

```bash
$ conan remote list
```

You can search any remote in the same way as you search your Conan local cache. Actually,
many Conan commands optionally accept a specific remote:

```bash
$ conan search "*" -r=my_local_server
```

Now, upload the package recipe and all the packages to your remote. In this example, we
are using our `my_local_server` remote, but you could use any other:

```bash
$ conan upload hello -r=my_local_server
```

Now try again to read the information from the remote. We refer to it as remote, even if
it is running on your local machine, as it could be running on another server in your LAN:

```bash
$ conan search hello -r=my_local_server
```

Now we can check if we can download the packages and use them in a project. For that purpose, we first
have to **remove the local copies**, otherwise the remote packages will not be downloaded. Since we
have just uploaded them, they are identical to the local ones.

```bash
$ conan remove hello -c
$ conan list hello
```

Now, to install the uploaded package from the Conan repository just run:

```bash
$ conan install --requires=hello/1.0 -r=my_local_server
```

You can check whether the package exists on your local computer again with:

```bash
$ conan list hello
```

#### SEE ALSO
- [JFrog Academy Conan 2 Essentials Module 2, Lesson 13: Working with Conan Repositories](https://academy.jfrog.com/path/conan-cc-package-manager/conan-2-essentials-module-2-package-creation-and-uploading?utm_source=Conan+Docs)
- [conan upload command reference](https://docs.conan.io/2//reference/commands/upload.html.md#reference-commands-upload)
- [conan remote command reference](https://docs.conan.io/2//reference/commands/remote.html.md#reference-commands-remote)
- [conan search command reference](https://docs.conan.io/2//reference/commands/search.html.md#reference-commands-search)
