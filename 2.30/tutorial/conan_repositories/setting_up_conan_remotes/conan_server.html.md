<a id="conan-server"></a>

# Setting up a Conan Server

#### IMPORTANT
This server is mainly used for testing (though it might work fine for small teams). We
recommend using the free [Artifactory Community Edition for C/C++](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes/artifactory/artifactory_ce_cpp.html.md#artifactory-ce-cpp)
for private development or **Artifactory Pro** as Enterprise solution.

The **Conan Server** is a free and open source server that implements Conan remote
repositories. It is a very simple application, used for testing inside the Conan client
and distributed as a separate pip package.

Install the **Conan Server** using pip:

```bash
$ pip install conan-server
```

Then you can run the server:

```bash
$ conan_server
 ***********************
 Using config: /Users/user/.conan_server/server.conf
 Storage: /Users/user/.conan_server/data
 Public URL: http://localhost:9300/v2
 PORT: 9300
 ***********************
 Bottle v0.12.24 server starting up (using WSGIRefServer())...
 Listening on http://0.0.0.0:9300/
 Hit Ctrl-C to quit.
```

#### NOTE
On Windows, you may experience problems with the server if you run it under Bash/MSYS2.
It is recommended to launch it in a regular `cmd` window.

#### SEE ALSO
* [Conan Server reference](https://docs.conan.io/2//reference/conan_server.html.md#reference-conan-server)
