# Passing Arguments to PyInstaller

Have PyDeployment pass arguments to PyInstaller.

---

You can have PyDeployment ignore command line arguments and instead pass them to
PyInstaller by using the separator `--`. Any arguments after the `--` separator
will be ignored by PyDeployment and passed on to PyInstaller. This is useful when
passing Python scripts to PyDeployment or when specifying parameters for a
PyInstaller spec file. In the latter case, you will need to double the `--`
separator as PyInstaller itself uses it to pass parameters to a spec file.
