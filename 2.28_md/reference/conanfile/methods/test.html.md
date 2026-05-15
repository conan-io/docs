<a id="reference-conanfile-methods-test"></a>

# test()

The `test()` method is only used for **test_package/conanfile.py**.
It will execute immediately after `build()` has been called, and its goal is to run some executable or tests on binaries to prove the package is correctly created.
Note that it is intended to be used as a test of the package: the headers are found, the libraries are found,
it is possible to link, etc. But it is **not intended** to run unit, integration or functional tests.

It usually takes the form of:

```python
def test(self):
    if can_run(self):
        cmd = os.path.join(self.cpp.build.bindir, "example")
        self.run(cmd, env="conanrun")
```

#### SEE ALSO
- See [the “testing packages” tutorial](https://docs.conan.io/2//tutorial/creating_packages/test_conan_packages.html.md#tutorial-creating-test) for more information.
- The [test_package_folder attribute](https://docs.conan.io/2//reference/conanfile/attributes.html.md#conan-conanfile-attributes-test-package-folder) allows defining a different default location of the test-package instead of the default `test_package` folder.
