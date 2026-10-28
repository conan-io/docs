<a id="conan-tools-qbsprofile"></a>

# QbsProfile

The `QbsProfile` generator produces the settings file that contains toolchain information.
This file can be imported into Qbs. The `QbsProfile` generator can be used like:

```python
from conan import ConanFile

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    requires = "hello/0.1"
    generators = "QbsProfile"
```

It is also possible to use `QbsProfile` manually in the `generate()` method:

```python
from conan import ConanFile
from conan.tools.qbs import QbsProfile

class App(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    requires = "hello/0.1"

    def generate(self):
        profile = QbsProfile(self)
        profile.generate()
```

Now we can generate the file using the `conan install` command.

```text
$ conan install . --output-folder=build --build missing
```

And import it into Qbs:

```text
$ qbs config import qbs_settings.txt --settings-dir qbs
```

Note that to acutually use the imported file, Qbs should be called with `--settings-dir`:

```text
$ qbs resolve --settings-dir qbs
```

Those commands are called automatically when using the `Qbs` helper class.
.. seealso:

```default
- Check the :ref:`Qbs helper <_conan_tools_qbs_helper>` for details.
```

## Reference

### *class* QbsProfile(conanfile, profile='conan', default_profile='conan')

Qbs profiles generator.

This class generates file with the toolchain information that can be imported by Qbs.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **profile** – The name of the profile in settings. Defaults to `"conan"`.
  * **default_profile** – The name of the default profile. Defaults to `"conan"`.

#### *property* filename

The name of the generated file. Returns `qbs_settings.txt`.

#### *property* content

Returns the content of the settings file as dict of Qbs properties.

#### render()

Returns the content of the settings file as string.

#### generate()

This method will save the generated files to the conanfile.generators_folder.

Generates the “qbs_settings.txt” file. This file contains Qbs settings such as toolchain
properties and can be imported using `qbs config --import`.
