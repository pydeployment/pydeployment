# PyDeployment
PyDeployment provides an easy way to package Python projects on Windows, macOS,
and Linux. This project is a wrapper that leverages existing software to take
your project from repository to executable file. If you can run it with Python,
you can ship it with PyDeployment.

## How PyDeployment Works
PyDeployment uses [PyInstaller](https://github.com/pyinstaller/pyinstaller) to
create an application directory. This created directory is then bundled into
the preferred distribution method for the platform.
* On Windows, [NSIS](https://nsis.sourceforge.io/) is used to create an
installer (EXE).
* On macOS, the hdiutil command is used to create an Apple disk image (DMG).
* On Linux, [appimagetool](https://github.com/AppImage/appimagetool) is used to
create an AppImage.

## Installing PyDeployment
Install PyDeployment with pip using the following command.

```
pip install --user pydeployment
```

## Quick Start
After installing PyDeployment, use the `pydeploy` command and either a Python
script or a PyInstaller
[spec file](https://pyinstaller.org/en/stable/spec-files.html) as the target.

```
pydeploy myapp.py
```

## Documentation
Documentation for using PyDeployment can be found on the project
[website](https://pydeployment.github.io/pydeployment).

## Examples
The following examples showcase build systems which utilize PyDeployment to build
their applications. These examples are themselves template repositories
available for use.

* [Hello World Tk](https://github.com/zevlee/hello-world-tk)
* [Hello World GTK](https://github.com/zevlee/hello-world-gtk)
* [Hello World Qt](https://github.com/zevlee/hello-world-qt)
