<a id="conan-repositories"></a>

# Working with Conan repositories

We already [learned how to download and use packages](https://docs.conan.io/2//tutorial/consuming_packages.html.md#tutorial-consuming-packages)
from [Conan Center](https://conan.io/center) that is the official repository for open
source Conan packages. We also [learned how to create our own packages](https://docs.conan.io/2//tutorial/creating_packages.html.md#tutorial-creating-packages) and store them in the Conan local cache for reusing later.
In this section, we cover how you can use Conan repositories to upload your
recipes and binaries and store them for later use on another machine, project, or for
sharing purposes.

First, we will cover how you can setup a Conan repository locally (you can skip this part
if you already have a Conan remote configured). Then, we will explain how to upload
packages to your own repositories and how to operate when you have multiple Conan remotes
configured. We will also briefly cover how you can contribute to the Conan Center
central repository.

Finally, we will explain the local_recipes_index, a special type of remote that allows
the use of a source folder with recipes as a Conan remote repository.

# Table of contents

* [Setting up a Conan remote](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes.html.md)
* [Uploading Packages](https://docs.conan.io/2//tutorial/conan_repositories/uploading_packages.html.md)
* [Contributing to Conan Center](https://docs.conan.io/2//tutorial/conan_repositories/conan_center.html.md)
* [Local Recipes Index Repository](https://docs.conan.io/2//tutorial/conan_repositories/setup_local_recipes_index.html.md)

#### NOTE
The Conan 2 Essentials training course is available for free at the JFrog Academy,
which covers the same topics as this documentation but in a more interactive way.
You can access it [here](https://academy.jfrog.com/path/conan-cc-package-manager?utm_source=Conan+Docs).
