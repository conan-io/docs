<a id="reference-conanfile-output"></a>

# Running and output

## Output text from recipes

Use the `self.output` attribute to output text from the recipes. Do **not** use Python’s `print()` function.

### error(self, msg: str, error_type: str = None)

Indicates that a serious issue has occurred that prevents the system
or application from continuing to function correctly.

Typically, this represents a failure in the normal flow of execution,
such as a service crash or a critical exception.
Notice that if the user has set the `core:warnings_as_errors` configuration,
this will raise an exception when the output is printed,
so that the error does not pass unnoticed.

### warning(self, msg: str, warn_tag: str = None)

Highlights a potential issue that, while not stopping the system,
could cause problems in the future or under certain conditions.

Warnings signal abnormal situations that should be
reviewed but don’t necessarily cause an immediate halt in operations.
Notice that if the tag matches the pattern in the `core:warnings_as_errors` configuration,
and is not skipped, this will be upgraded to an error, and raise an exception
when the output is printed, so that the error does not pass unnoticed.

### success(self, msg: str)

Shows that an operation has been completed successfully.

This type of message is useful to confirm that key processes or tasks have finished correctly,
which is essential for good application monitoring.

### highlight(self, msg: str)

Marks or emphasizes important events or processes that need to stand out but don’t necessarily
indicate success or error.

These messages draw attention to key points that may be relevant for the user or administrator.

### info(self, msg: str, fg: str = None, bg: str = None, newline: bool = True)

Provides general information about the system or ongoing operations.

Info messages are basic and used to inform about common events,
like the start or completion of processes, without implying specific problems or achievements.

### status(self, msg: str, fg: str = None, bg: str = None, newline: bool = True)

Provides general information about the system or ongoing operations.

Info messages are basic and used to inform about common events,
like the start or completion of processes, without implying specific problems or achievements.

The following three methods are not shown by default and are usually reserved for scenarios that require a higher level
of verbosity. You can display them using the arguments `-v`, `-vv`, and `-vvv` respectively.

### verbose(self, msg: str, fg: str = None, bg: str = None)

Displays additional and detailed information that, while not critical,
can be useful for better understanding how the system is working.

This message won’t be printed unless the user has set the log level to verbose
(e.g., using the `-v` option in the command line).

It’s appropriate for gaining more context without overloading the logs with
excessive detail. Useful when more clarity is needed than a simple info.

### debug(self, msg: str, fg: str = '\\x1b[35m', bg: str = None)

With a high level of detail, it is mainly used for debugging code.

This message won’t be printed unless the user has set the log level to debug
(e.g., using the `-vv` option in the command line).

These messages provide useful information for developers, such as variable values
or execution flow details, to trace errors or analyze the program’s behavior.

### trace(self, msg: str)

This is the most extreme level of detail.

Trace messages log every little step the system takes, including function entries and exits,
variable changes, and other very specific events.

This message won’t be printed unless the user has set the log level to trace
(e.g., using the `-vvv` option in the command line).

It’s used when full visibility of everything happening in the system is required,
but should be used carefully due to the large amount of information it can generate.

These output functions will only output if the verbosity level with which Conan was launched is the same or higher than the message,
so running with `-vwarning` will output calls to `warning()` and `error()`, but not `info()`
(Additionally, the `highlight()` and `success()` methods have a `-vnotice` verbosity level)

Note that these methods return the output object again, so that you can chain output calls if needed.

Using the `core:warnings_as_errors` conf, you can make Conan raise an exception when either errors or a tagged warning matching any of the given patterns is printed.
This is useful to make sure that recipes are not printing unexpected warnings or errors.
Additionally, you can skip which warnings trigger an exception [with the core:skip_warnings conf](https://docs.conan.io/2//reference/config_files/global_conf.html.md#reference-config-files-global-conf-skip-warnings).

```text
# Raise an exception if any warning or error is printed
core:warnings_as_errors=['*']
# But skip the deprecation warnings
core:skip_warnings=['deprecated']
```

Both confs accept a list of patterns to match against the warning tags.
A special `unknown` value can be used to match any warning without a tag.

To tag a warning, use the `warn_tag` argument of the `warning()` method in your recipes:

```python
self.output.warning("Extra warning", warn_tag="custom_tag")
```

#### NOTE
Custom commands and tools are free to instantiate their own `ConanOutput` object.

Some methods have optional `fg` and `bg` arguments, these are colour codes for the foreground and background of the text,
available in the `conan.api.output.Color` class.

```python
self.output.info("This is a message", fg=Color.BLUE, bg=Color.YELLOW)
```

<a id="reference-conanfile-run"></a>

## Running commands

Recipes and helpers can use the `self.run()` method to run system commands while injecting the calls to activate the appropriate environment,
and throw exceptions when errors occur so that command errors do not pass unnoticed.
It also wraps the commands with the results of the [command wrapper plugin](https://docs.conan.io/2//reference/extensions/command_wrapper.html.md#reference-extensions-command-wrapper).

### run(self, command: str, stdout=None, cwd=None, ignore_errors=False, env='', quiet=False, shell=True, scope='build', stderr=None)

Run a command in the current package context.

* **Parameters:**
  * **command** – The command to run.
  * **stdout** – The output stream to write the command output. If `None`, it defaults to
    the standard output stream.
  * **stderr** – The error output stream to write the command error output. If `None`,
    it defaults to the standard error stream.
  * **cwd** – The current working directory to run the command in.
  * **ignore_errors** – If `True`, do not raise an error if the command returns a
    non-zero exit code.
  * **env** – The environment file to use. If empty, it defaults to `"conanbuild"` for
    when `scope` is `build` or `"conanrun"` for `run`.
    If set to `None` explicitly, no environment file will be applied,
    which is useful for commands that do not require any environment.
  * **quiet** – If `True`, suppress the output of the command.
  * **shell** – If `True`, run the command in a shell. This is passed to the
    underlying `Popen` function.
  * **scope** – The scope of the command, either `"build"` or `"run"`.

Use the `stdout` and `stderr` arguments to redirect the output of the command to a file-like object instead of the console.

```python
# Redirect stdout to a file
with open("ninja_stdout.log", "w") as stdout:
    # Redirect stderr to a StringIO object to be able to read it later
    stderr = StringIO()
    self.run("ninja ...", stdout=stdout, stderr=stderr)
```
