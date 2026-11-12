# Reference models

<a id="conan-api-model-recipereference"></a>

### *class* RecipeReference(name=None, version=None, user=None, channel=None, revision=None, timestamp=None)

An exact (no version-range, no alias) reference of a recipe,
it represents a reference of the form `name/version[@user/channel][#revision][%timestamp]`.
Should be enough to locate a recipe in the cache or in a server, and
validation will be external to this class, at specific points (export, api, etc).

The attributes should be regarded as immutable, and should not be modified by the user.

#### name *: str*

Name of the reference

#### version *: [Version](https://docs.conan.io/2//reference/tools/scm/version.html.md#conan.tools.scm.Version)*

Version of the reference

#### user

User of the reference, if any

#### channel

Channel of the reference, if any

#### revision

Revision of the reference, if any

#### timestamp

Timestamp of the reference, if any

#### *static* loads(rref)

Instantiates an object from a string, in the form:
`name/version[@user/channel][#revision][%timestamp]`

#### validate_ref(allow_uppercase=False)

Check that the reference is valid, and raise a `ConanException` if not.

#### matches(pattern, is_consumer)

fnmatches the reference against the provided pattern.

* **Parameters:**
  * **pattern** (*str*) – the pattern to match against, it can contain wildcards,
    and can start with `!` or `~` to negate the match.
    A special value of `&` will return a match only of `is_consumer` is `True`
  * **is_consumer** (*bool*) – if `True`, the pattern `&` will match this reference.
