<a id="conan-tools-scm-version"></a>

# Version

This is a helper class to work with versions, it splits the version string based on dots and hyphens.
It exposes all the version components as properties and offers total ordering through compare operators.

```python
 compiler_lower_than_12 = Version(self.settings.compiler.version) < "12.0"

 is_legacy = Version(self.version) < 2
```

### *class* Version(value, qualifier=False)

This is NOT an implementation of semver, as users may use any pattern in their versions.
It is just a helper to parse “.” or “-” and compare taking into account integers when possible

## Attributes

The `Version` class offers ways to access the different parts of the version number:

### main

Get all the main digits.

```python
v = Version("1.2.3.4-alpha.3+b1")
assert [str(i) for i in v.main] == ['1', '2', '3', '4', '5']
```

### major

Get the major digit.

```python
v = Version("1.2.3.4-alpha.3+b1")
assert str(v.major) == "1"
```

### minor

Get the minor digit.

```python
v = Version("1.2.3.4-alpha.3+b1")
assert str(v.minor) == "2"
```

### patch

Get the patch digit.

```python
v = Version("1.2.3.4-alpha.3+b1")
assert str(v.patch) == "3"
```

### micro

Get the micro digit.

```python
v = Version("1.2.3.4-alpha.3+b1")
assert str(v.micro) == "4"
```

### pre

Get the pre-release digit.

```python
v = Version("1.2.3.4-alpha.3+b1")
assert str(v.pre) == "alpha.3"
```

### build

Get the build digit.

```python
v = Version("1.2.3.4-alpha.3+b1")
assert str(v.build) == "b1"
```

## Methods

The `Version` class implements the following methods:

### in_range

Check if the version is in the specified range.

```python
assert Version("1.0").in_range(">=1.0 <2")
assert not Version("1.0").in_range(">1.0 <2")

assert not Version("1.0-rc").in_range(">=1.0 <2.0")
assert Version("1.0-rc").in_range(">=1.0 <2.0", resolve_prerelease=True)
```
