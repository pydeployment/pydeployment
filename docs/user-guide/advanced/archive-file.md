# Package as an Archive File

An alternative packaging method.

---

Instead of the preferred distribution method for the platform, you can choose
to package the output of PyInstaller as an archive file. On Windows, the file
will be a ZIP file. On macOS and Linux, the file will be a tarball compressed
with LZMA (TXZ).

To use this option, set the `ARCHIVE` option to "True" or any non-empty string.
Alternatively, use the `--archive` option on the command line.
