<a id="developing-packages"></a>

# Developing packages locally

As we learned in [previous sections](https://docs.conan.io/2//tutorial/creating_packages.html.md#tutorial-creating-packages) of the tutorial,
the most straightforward way to work when developing a Conan package is to run
**conan create**. This means that every time it is run, Conan performs a series of
costly operations in the Conan cache, such as downloading, decompressing, copying sources,
and building the entire library from scratch. Sometimes, especially with large libraries,
while we are developing the recipe, these operations cannot be performed every time.

This section will first show the **Conan local development flow**, that is, working on
packages in your local project directory without having to export the contents of the
package to the Conan cache first.

We will also cover how other packages can consume packages under development using
**editable mode**.

Finally, we will explain the **Conan package layouts** in depth. It is the key feature that
makes it possible to work with Conan packages in the Conan cache or locally without making
any changes.

* [Package Development Flow](https://docs.conan.io/2//tutorial/developing_packages/local_package_development_flow.html.md)
* [Packages in editable mode](https://docs.conan.io/2//tutorial/developing_packages/editable_packages.html.md)
* [Understanding the Conan Package layout](https://docs.conan.io/2//tutorial/developing_packages/package_layout.html.md)
* [Workspaces](https://docs.conan.io/2//tutorial/developing_packages/workspaces.html.md)
