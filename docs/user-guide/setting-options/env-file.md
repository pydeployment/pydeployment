# Using an Environment File

Place build options in a file.

---

You can place your build options in a file to avoid needing to list them out
constantly.

## Setting the Environment File

By default, PyDeployment pulls values from the environment file named `.env` in
the current working directory. You can specify a different environment file
with the environment variable `ENV_FILE` set to the path to your desired
environment file. For example, on Windows, you can use the following command
to pull values from an environment file named `env_values.txt` located in the
current working directory.

```
cmd /C "set ENV_FILE=env_values.txt pydeploy myapp.py"
```

The equivalent command on macOS and Linux would be the following.

```
env ENV_FILE=env_values.txt pydeploy myapp.py
```

## Format

The environment file is a text file where each line takes the form `Name=Value`
where `Name` is the name of the build option and `Value` is its value. Take
care to enclose values containing white space with quotes.

## Platform-Specific Options

You can set platform-specific options by prefixing variables in the environment
file with their platform. The prefixes are `WINDOWS_`, `MACOS_`, and `LINUX_`
for Windows, macOS, and Linux, respectively.

A common use case for platform-specific options is with the `ICON` option.

```
WINDOWS_ICON=myapp.ico
MACOS_ICON=myapp.icns
LINUX_ICON=myapp.png
```

Using this technique, you can easily keep all of your build options in a single
file.
