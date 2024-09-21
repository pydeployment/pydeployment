# Using a Custom Appimagetool Binary

Specify your own appimagetool binary.

---

Although appimagetool binaries are included with PyDeployment, you can instead
choose to use your own appimagetool binary by providing the path to the binary
to `APPIMAGETOOL` in the environment file or `--appimagetool` on the command
line.

Additionally, you can choose your own AppImage runtime by providing the path to
the file to `RUNTIME_FILE` in the environment file or `--runtime-file` on the
command line. If you specify the value to be an empty string (i.e. `""`), then
the latest runtime will be downloaded, which is the default behavior of the
appimagetool binary.

For compatibility purposes, you can choose to extract the appimagetool binary
before running it. This is useful in cases where PyDeployment is run inside a
container or on a machine where FUSE is not available. To use this option, set
the `APPIMAGE_EXTRACT_AND_RUN` option to "True" or any non-empty string.
Alternatively, use the `--appimage-extract-and-run` option on the command line.
