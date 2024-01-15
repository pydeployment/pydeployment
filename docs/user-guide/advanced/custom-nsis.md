# Using a Custom NSIS File

Use a custom NSIS template file.

---

You can use a custom NSIS script rather than the one provided by PyDeployment by
specifying the path to the file to `NSIS` in the environment file or `--nsis`
on the command line. If you wish to use the variables provided by PyDeployment,
be sure to include the following header at the top of the file.

```
!define /file APPDIR "APPDIR"
!define /file FILENAME "FILENAME"
!define /file APPNAME "APPNAME"
!define /file VERSION "VERSION"
!define /file AUTHOR "AUTHOR"
!define /file PUBLISHER "PUBLISHER"
!define /file DESCRIPTION "DESCRIPTION"
!define /file ICON "ICON"
!define /file LICENSE "LICENSE"
!define /file INSTALLSIZE "INSTALLSIZE"
!define /file ARCH "ARCH"
```
