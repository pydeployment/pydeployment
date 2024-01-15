# Getting Started

Installation and basic usage.

---

## Requirements

PyDeployment requires [Python](https://www.python.org/) version `3.10` or higher and
a recent version of [pip](https://pip.pypa.io/en/stable/installation/).

## Installing PyDeployment

Install PyDeployment with pip using the following command.

```
pip install --user pydeployment
```

## Basic Usage

Use the command `pydeploy` with a Python script or
[PyInstaller spec file](https://pyinstaller.org/en/stable/spec-files.html) as
the target file.

```
pydeploy myapp.py
```

PyDeployment will run PyInstaller and package the resulting output into the
preferred distribution format of the platform on which PyDeployment was run.

* On Windows, [NSIS](https://nsis.sourceforge.io/) is used to create an
installer (EXE).
* On macOS, the hdiutil command is used to create an Apple disk image (DMG).
* On Linux, [appimagetool](https://github.com/AppImage/appimagetool) is used to
create an AppImage.

Read [Build Options](build-options.md) to learn about the values you can set
for your project.
