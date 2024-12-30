# Build Options

List of all possible options to set.

---

PyDeployment recognizes the following build options. See
[Setting Build Options](setting-options/README.md) for details on how to set
these options.

## Universal Build Options

| Option | Name | Type | Description | Default |
| :--    | :--  | :--  | :--         | :--     |
| `--log` | `LOG` | text | Set the log level. Can choose among `'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`. Setting the log level to `'WARNING'` avoids asking the user for confirmation of the build. Setting the log level to `'ERROR'` also avoids asking the user for confirmation to delete preexisting build artifacts. | `'INFO'` |
| `-y`, `--no-confirm` | `NO_CONFIRM` | boolean | Do not ask for confirmation. Automatically proceeds with build and deletes preexisting build artifacts. | `False` |
| `--no-clean` | `NO_CLEAN` | boolean | Do not delete build artifacts after completing the build process. | `False` |
| `--archive` | `ARCHIVE` | boolean | Package as an archive file. See [Package as an Archive File](advanced/archive-file.md). | `False` |
| `-f`, `--filename` | `FILENAME` | text | Output filename without version and architecture. Must not contain white space or any other characters which are disallowed in file names. | Basename of the Python script or PyInstaller spec file. |
| `-a`, `--appname` | `APPNAME` | text | Application name. | The value of `FILENAME` |
| `--id` | `ID` | text | Application ID. Should follow reverse DNS format. | `'id.not.found.'` + The value of `FILENAME` |
| `--appv`, `--app-version` | `VERSION` | text | Application version. | None |
| `--author` | `AUTHOR` | text | Author. | None |
| `--publisher` | `PUBLISHER` | text | Publisher. | The value of `AUTHOR` |
| `-d`, `--description` | `DESCRIPTION` | text | Application description. | None |
| `--pyi-version` | `PYI_VERSION` | text | PyInstaller version to be used. | The latest version of PyInstaller |
| `-i`, `--icon` | `ICON` | path | Path to icon file. | Path to the PyDeployment logo |
| `-l`, `--license` | `LICENSE` | path | Path to license file. | Path pointing to a single-line temporary text file with the content: `'Copyright (c) '` + the value of `AUTHOR` |
| `-o`, `--outdir` | `OUTDIR` | path | Path to output directory. | `'dist'` |
| `-r`, `--requirements` | `REQUIREMENTS` | path | Path to pip requirements file. The listed packages will be installed along with PyInstaller. This option is ignored if `VENV` is set. | None |
| `--venv` | `VENV` | path | Path to Python virtual environment. See [Using a Custom Virtual Environment](advanced/custom-venv.md). | None |

## Windows Build Options

| Option | Name | Type | Description | Default |
| :--    | :--  | :--  | :--         | :--     |
| `--nsis` | `NSIS` | path | Path to NSIS file. See [Using a Custom NSIS File](advanced/custom-nsis.md). | Path to PyDeployment's default NSIS file `'build.nsi'` |
| `--makensis` | `MAKENSIS` | path | Path to makensis binary. See [Using a Custom Makensis Binary](advanced/custom-makensis.md). | Path to PyDeployment's included makensis binary `makensis.exe` |

## macOS Build Options

See [macOS Notarization](advanced/macos-notarization.md) to learn about these
options and how they are used.

| Option | Name | Type | Description | Default |
| :--    | :--  | :--  | :--         | :--     |
| `-E`, `--enti`, `--entitlements` | `ENTI` | path | Path to entitlements file. | Path to PyDeployment's default entitlements file `'entitlements.plist'`
| `-C`, `--cert`, `--certificate` | `CERT` | text | Common Name of Certificate. | None |
| `-K`, `--keyc`, `--keychain-profile` | `KEYC` | text | Name of stored Keychain Profile. | None |
| `-A`, `--apid`, `--apple-id` | `APID` | text | Apple ID. | None |
| `-T`, `--tmid`, `--team-id` | `TMID` | text | Team ID. | None |
| `-P`, `--pass`, `--password` | `PASS` | text | App-specific Password. | None |

## Linux Build Options

| Option | Name | Type | Description | Default |
| :--    | :--  | :--  | :--         | :--     |
| `--appdata` | `APPDATA` | path | Path to AppStream metadata file. File name should be in the form: The value of `ID` + `'.appdata.xml'`. | None |
| `--appimagetool` | `APPIMAGETOOL` | path | Path to appimagetool. See [Using a Custom Appimagetool Binary](advanced/custom-appimagetool.md). | Path to PyDeployment's included appimagetool `'appimagetool-*.AppImage'`, whichever one matches the architecture of the system. |
| `--runtime-file` | `RUNTIME_FILE` | path | Path to AppImage runtime. See [Using a Custom Appimagetool Binary](advanced/custom-appimagetool.md). | Path to PyDeployment's included AppImage runtime `'runtime-*'`, whichever one matches the architecture of the system. |
