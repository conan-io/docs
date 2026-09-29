# Profiles API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* ProfilesAPI(conan_api, api_helpers)

#### get_default_host()

* **Returns:**
  the path to the default “host” profile, either in the cache or as defined
  by the user in configuration

#### get_default_build()

* **Returns:**
  the path to the default “build” profile, either in the cache or as
  defined by the user in configuration

#### get_profile(profiles, settings=None, options=None, conf=None, cwd=None, context=None)

Computes a Profile as the result of aggregating all the user arguments, first it
loads the “profiles”, composing them in order (last profile has priority), and
finally adding the individual settings, options (priority over the profiles)

#### get_path(profile, cwd=None, exists=True)

* **Returns:**
  the resolved path of the given profile name, that could be in the cache,
  or local, depending on the “cwd”

#### list()

List all the profiles file sin the cache
:return: an alphabetically ordered list of profile files in the default cache location

#### *static* detect()

* **Returns:**
  an automatically detected Profile, with a “best guess” of the system settings
