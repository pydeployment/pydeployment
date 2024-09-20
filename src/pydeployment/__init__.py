from os.path import join
from platform import python_compiler
from shlex import split
from subprocess import CalledProcessError, PIPE, Popen
from typing import Any, Dict, Iterator

# PyDeployment version
__version__ = "1.1.2"
# Default version of PyInstaller. Can be set to a specific value if PyDeployment
# breaks using a future version
PYI_VERSION = None
# Python executable path
if python_compiler()[:3] == "MSC":
    PYEXE = join("Scripts", "python")
else:
    PYEXE = join("bin", "python3")
# Linux desktop file keys
LINUX_DESKTOP_KEYS = (
    "Type", "Version", "Name", "GenericName", "NoDisplay", "Comment", "Icon",
    "Hidden", "OnlyShowIn", "DBusActivatable", "TryExec", "Exec", "Path",
    "Terminal", "Actions", "MimeType", "Categories", "Implements", "Keywords",
    "StartupNotify", "StartupWMClass", "URL", "PrefersNonDefaultGPU",
    "SingleMainWindow", "X-AppImage-Version"
)
# Build option display order
DISPLAY_ORDER = (
    "NO_CONFIRM", "NO_CLEAN", "ARCHIVE", "FILENAME", "APPNAME", "ID",
    "VERSION", "AUTHOR", "PUBLISHER", "DESCRIPTION", "PYI_VERSION", "ICON",
    "LICENSE", "OUTDIR", "REQUIREMENTS", "VENV", "APPDATA", "APPIMAGETOOL",
    "RUNTIME_FILE", *LINUX_DESKTOP_KEYS, "ENTI", "CERT", "KEYC", "APID",
    "TMID", "PASS", "NSIS", "MAKENSIS", "TARGET", "PYI_ARGS"
)


def run_command(cmd: str, **kwargs: Dict[str, Any]) -> Iterator[str]:
    """
    Generator function yielding command outputs
    
    :param cmd: Command
    :type cmd: str
    :param kwargs: Keyword arguments to pass to `subprocess.Popen`
    :type kwargs: Dict[str, Any]
    :return: Output line
    :rtype: Iterator[str]
    """
    if python_compiler()[:3] == "MSC":
        command = cmd.split()
    else:
        command = split(cmd)
    process = Popen(command, stdout=PIPE, shell=False, text=True, **kwargs)
    for line in iter(process.stdout.readline, ""):
        yield line
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise CalledProcessError(return_code, cmd)
