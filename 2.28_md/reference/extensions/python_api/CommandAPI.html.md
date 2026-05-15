# Command API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* CommandAPI(conan_api)

This CommandAPI is useful to be able to launch full commands from the ConanAPI

Sometimes some commands are built using several calls to the ConanAPI. If we want
to reuse the same functionality, then we would have to copy all that code into our
own commands.
Instead of doing that, it is possible to call Conan commands using this API, via
the `run()` method.

#### run(cmd)

Runs another Conan command via API

* **Parameters:**
  **cmd** – Conan command to run. It can be either a string, or a list of strings.
* **Returns:**
  It will return what that command returns. Note that different commands can
  return different things, so the caller needs to process it accordingly.
