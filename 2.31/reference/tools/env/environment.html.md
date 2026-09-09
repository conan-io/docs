<a id="conan-tools-env-environment-model"></a>

# Environment

`Environment` is a generic class that helps to define modifications to the environment variables.
This class is used by other tools like the conan.tools.gnu [Autotools](https://docs.conan.io/2//reference/tools/gnu/autotools.html.md#conan-tools-gnu-build-helper) helpers and
the [VirtualBuildEnv](https://docs.conan.io/2//reference/tools/env/virtualbuildenv.html.md#conan-tools-env-virtualbuildenv) and [VirtualRunEnv](https://docs.conan.io/2//reference/tools/env/virtualrunenv.html.md#conan-tools-env-virtualrunenv)
generator. It is important to highlight that this is a generic class, to be able to use it, a specialization
for the current context (shell script, bat file, path separators, etc), a `EnvVars` object needs to be obtained
from it.

## Variable declaration

```python
from conan.tools.env import Environment

def generate(self):
    env = Environment()
    env.define("MYVAR1", "MyValue1")  # Overwrite previously existing MYVAR1 with new value
    env.append("MYVAR2", "MyValue2")  # Append to existing MYVAR2 the new value
    env.prepend("MYVAR3", "MyValue3") # Prepend to existing MYVAR3 the new value
    env.remove("MYVAR3", "MyValue3")  # Remove the MyValue3 from MYVAR3
    env.unset("MYVAR4")               # Remove MYVAR4 definition from environment

    # And the equivalent with paths
    env.define_path("MYPATH1", "path/one")  # Overwrite previously existing MYPATH1 with new value
    env.append_path("MYPATH2", "path/two")  # Append to existing MYPATH2 the new value
    env.prepend_path("MYPATH3", "path/three") # Prepend to existing MYPATH3 the new value
```

The “normal” variables (the ones declared with `define`, `append` and `prepend`) will be appended with a space,
by default, but the `separator` argument can be provided to define a custom one.

The “path” variables (the ones declared with `define_path`, `append_path` and `prepend_path`) will be appended
with the default system path separator, either `:` or `;`, but it also allows defining which one.

## Generation of environment files

The generation of environment script files (like `envfile.bat|.sh|.ps1|.env`) can be done indirectly
by the `EnvVars` class, which can be obtained with:

```python
from conan.tools.env import Environment

env1 = Environment()
...
envvars = env1.vars(self)  # An EnvVars object
# Generate a .bat|.sh|.ps1|.env file depending on current
# settings and Conan configuration
envars.save_script("mybuild")
# or decide to be explicit and generate some of the files:
envvars.save_dotenv("myenv.env")
```

These files can be used also automatically by subsequent `self.run()` calls.
For more information see the `EnvVars` class documentation.

## Composition

Environments can be composed:

```python
from conan.tools.env import Environment

env1 = Environment()
env1.define(...)
env2 = Environment()
env2.append(...)

env1.compose_env(env2) # env1 has priority, and its modifications will prevail
```

## Obtaining environment variables

You can obtain an `EnvVars` object with the `vars()` method like this:

```python
from conan.tools.env import Environment

def generate(self):
    env = Environment()
    env.define("MYVAR1", "MyValue1")
    envvars = env.vars(self, scope="build")
    # use the envvars object
```

The default `scope` is equal `"build"`, which means that if this `envvars` generate a script to
activate the variables, such script will be automatically added to the `conanbuild.sh|bat` one, for
users and recipes convenience. Conan generators use `build` and `run` scope, but it might be possible
to manage other scopes too.

## Environment definition

There are some other places where `Environment` can be defined and used:

- In recipes `package_info()` method, in new `self.buildenv_info` and `self.runenv_info`, this
  environment will be propagated via `VirtualBuildEnv` and `VirtualRunEnv` respectively to packages
  depending on this recipe.
- In generators like `AutootoolsDeps`, `AutotoolsToolchain`, that need to define environment for the
  current recipe.
- In profiles `[buildenv]` section.
- In profiles `[runenv]` section.

The definition in `package_info()` is as follow, taking into account that both `self.buildenv_info` and `self.runenv_info`
are objects of `Environment()` class.

```python
from conan import ConanFile

class App(ConanFile):
    name = "mypkg"
    version = "1.0"
    settings = "os", "arch", "compiler", "build_type"

    def package_info(self):
        # This is information needed by consumers to build using this package
        self.buildenv_info.append("MYVAR", "MyValue")
        self.buildenv_info.prepend_path("MYPATH", "some/path/folder")

        # This is information needed by consumers to run apps that depends on this package
        # at runtime
        self.runenv_info.define("MYPKG_DATA_DIR", os.path.join(self.package_folder,
                                                               "datadir"))
```

### Reference

### *class* Environment

Generic class that helps to define modifications to the environment variables.

#### dumps()

* **Returns:**
  A string with a profile-like original definition, not the full environment
  values

#### define(name, value, separator=' ')

Define name environment variable with value value

* **Parameters:**
  * **name** – Name of the variable
  * **value** – Value that the environment variable will take
  * **separator** – The character to separate appended or prepended values

#### unset(name)

clears the variable, equivalent to a unset or set XXX=

* **Parameters:**
  **name** – Name of the variable to unset

#### append(name, value, separator=None)

Append the value to an environment variable name

* **Parameters:**
  * **name** – Name of the variable to append a new value
  * **value** – New value
  * **separator** – The character to separate the appended value with the previous value. By default it will use a blank space.

#### append_path(name, value)

Similar to “append” method but indicating that the variable is a filesystem path. It will automatically handle the path separators depending on the operating system.

* **Parameters:**
  * **name** – Name of the variable to append a new value
  * **value** – New value

#### prepend(name, value, separator=None)

Prepend the value to an environment variable name

* **Parameters:**
  * **name** – Name of the variable to prepend a new value
  * **value** – New value
  * **separator** – The character to separate the prepended value with the previous value

#### prepend_path(name, value)

Similar to “prepend” method but indicating that the variable is a filesystem path. It will automatically handle the path separators depending on the operating system.

* **Parameters:**
  * **name** – Name of the variable to prepend a new value
  * **value** – New value

#### remove(name, value)

Removes the value from the variable name.

* **Parameters:**
  * **name** – Name of the variable
  * **value** – Value to be removed.

#### compose_env(other)

Compose an Environment object with another one.
`self` has precedence, the “other” will add/append if possible and not
conflicting, but `self` mandates what to do. If `self` has `define()`, without
placeholder, that will remain.

* **Parameters:**
  **other** (class:Environment) – the “other” Environment

#### vars(conanfile, scope='build')

* **Parameters:**
  * **conanfile** – Instance of a conanfile, usually `self` in a recipe
  * **scope** – Determine the scope of the declared variables.
* **Returns:**
  An EnvVars object from the current Environment object

#### deploy_base_folder(package_folder, deploy_folder)

Make the paths relative to the deploy_folder
