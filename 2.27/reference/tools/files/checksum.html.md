# conan.tools.files checksums

## conan.tools.files.check_md5()

### check_md5(conanfile, file_path, signature)

Check that the specified `MD5` hash of the `file_path` matches the actual hash.
If doesn’t match it will raise a `ConanException`.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **file_path** – Path of the file to check.
  * **signature** – Expected MD5 hash.

## conan.tools.files.check_sha1()

### check_sha1(conanfile, file_path, signature)

Check that the specified `SHA-1` hash of the `file_path` matches the actual hash.
If doesn’t match it will raise a `ConanException`.

* **Parameters:**
  * **conanfile** – Conanfile object.
  * **file_path** – Path of the file to check.
  * **signature** – Expected SHA-1 hash.

## conan.tools.files.check_sha256()

### check_sha256(conanfile, file_path, signature)

Check that the specified `SHA-256` hash of the `file_path` matches the actual hash.
If doesn’t match it will raise a `ConanException`.

* **Parameters:**
  * **conanfile** – Conanfile object.
  * **file_path** – Path of the file to check.
  * **signature** – Expected SHA-256 hash.
