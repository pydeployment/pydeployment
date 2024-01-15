# Using the Command Line

Set build options on the command line.

---

You can use the command line to set build options.

## Format

Setting a value on the
command line takes the form `Option Value` where `Option` is the build option
and `Value` is its value. Take care to enclose values containing white space
with quotes.

## Example

The following commands will all set `my_app.py` to have the filename `'myapp'`,
the app name `'My App'`, and the version `'0.1.0'`.

```
pydeploy -f myapp -a 'My App' --appv 0.1.0 my_app.py
```

```
pydeploy my_app.py -f myapp -a 'My App' --appv 0.1.0
```

```
pydeploy -f myapp my_app.py -a 'My App' --appv 0.1.0
```

As you can see, the ordering of the arguments doesn't matter with a notable
exception: when
[passing arguments to PyInstaller](../advanced/passing-args-to-pyi.md).
