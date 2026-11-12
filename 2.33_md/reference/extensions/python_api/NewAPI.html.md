# New API

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

#### WARNING
Subapis **must not** be initialized by themselves. They are intended to be
accessed only through the main [ConanAPI](https://docs.conan.io/2//reference/extensions/python_api/ConanAPI.html.md#reference-python-api-conan-api) attributes.

### *class* NewAPI(conan_api)

#### save_template(template: str, defines=None, output_folder=None, force=False)

Save the `template` files in the `output_folder`, replacing the template variables
with the `defines`

* **Parameters:**
  * **template** – The name of the template to use, either built-in ones or those available under `<conan_home>/templates/command/new/<template>`
  * **defines** – A list with the `k=v` variables to replace in the template
  * **output_folder** – The folder where the template files will be saved, cwd if `None`
  * **force** – If `True`, overwrite the files if they already exist, otherwise raise an error
