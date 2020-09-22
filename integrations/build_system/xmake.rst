## Install third-party packages

After version 2.2.5, xmake supports support for dependency libraries in third-party package managers, such as: conan, brew, vcpkg, clib and etc.

~~~lua
---xmake.lua

add_requires("CONAN::zlib/1.2.11@conan/stable", {alias = "zlib", debug = true})
add_requires("CONAN::OpenSSL/1.0.2n@conan/stable", {alias = "openssl", 
    configs = {options = "OpenSSL:shared=True"}})

target("test")
    set_kind("binary")
    add_files("src/*.c") 
    add_packages("openssl", "zlib")
~~~

After executing xmake to compile:
```
$ xmake
checking for the architecture ... x86_64
checking for the Xcode directory ... /Applications/Xcode.app
checking for the SDK version of Xcode ... 10.14
note: try installing these packages (pass -y to skip confirm)?
  -> CONAN::zlib/1.2.11@conan/stable  (debug)
  -> CONAN::OpenSSL/1.0.2n@conan/stable  
please input: y (y/n)

  => installing CONAN::zlib/1.2.11@conan/stable .. ok
  => installing CONAN::OpenSSL/1.0.2n@conan/stable .. ok

[  0%]: ccache compiling.release src/main.c
[100%]: linking.release test
```

---

## Find the conan package

XMake v2.2.6 and later versions also support finding the specified package from the conan:

~~~lua
find_packages("conan::OpenSSL/1.0.2n@conan/stable")
~~~

### Test command for finding package

We can also add a third-party package manager prefix to test:
~~~lua
xmake l find_packages conan::OpenSSL/1.0.2n@conan/stable
~~~

**Note:** It should be noted that if the find_package command is executed in the project directory with xmake.lua, there will be a cache.
If the search fails, the next lookup will also use the cached result. If you want to force a retest every time,
Please switch to the non-project directory to execute the above command.
