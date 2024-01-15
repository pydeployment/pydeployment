# PyDeployment

Deploy Python projects with ease.

---

PyDeployment provides an easy way to package Python projects on Windows, macOS,
and Linux. This project is a wrapper that leverages existing software to take
your project from repository to executable file. If you can run it with Python,
you can deploy it with PyDeployment.

Read the [User Guide](user-guide/README.md) to learn about installing and using
PyDeployment.

## How PyDeployment Works

PyDeployment uses [PyInstaller](https://github.com/pyinstaller/pyinstaller) to
create an application directory. This created directory is then bundled into
the preferred distribution method for the platform.

* On Windows, [NSIS](https://nsis.sourceforge.io/) is used to create an
installer (EXE).
* On macOS, the hdiutil command is used to create an Apple disk image (DMG).
* On Linux, [appimagetool](https://github.com/AppImage/appimagetool) is used to
create an AppImage.

## Examples
The following examples showcase build systems which utilize PyDeployment to build
their applications. These examples are themselves template repositories
available for use.

*Examples are in progress*

<!-- * [Hello World Tk](https://github.com/zevlee/hello-world-tk) -->
<!-- * [Hello World GTK](https://github.com/zevlee/hello-world-gtk) -->
<!-- * [Hello World Qt](https://github.com/zevlee/hello-world-qt) -->
