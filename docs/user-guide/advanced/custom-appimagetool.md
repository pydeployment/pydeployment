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
