from argparse import ArgumentParser
from typing import Optional
from . import __version__


class ArgParser(ArgumentParser):
    """
    Class to parse command line arguments

    :param system: Name of system OS (Linux, Darwin, or Windows)
    :type system: Optional[str]
    """
    def __init__(self, system: Optional[str]=None) -> None:
        """
        Constructor
        """
        super().__init__(
            prog="pydeploy",
            description="PyDeployment - Deploy Python projects with ease"
        )
        # PyDeployment version
        self.add_argument(
            "-v", "--version",
            action="version",
            version=f"PyDeployment {__version__}"
        )
        # Universal arguments
        self.add_argument(
            "--log",
            action="store",
            help="Set the log level",
            dest="LOG",
            choices=("DEBUG", "INFO", "WARNING", "ERROR"),
            default="INFO"
        )
        self.add_argument(
            "-y", "--no-confirm",
            action="store_true",
            help="Do not ask for confirmation",
            dest="NO_CONFIRM",
            default=False
        )
        self.add_argument(
            "--no-clean",
            action="store_true",
            help="Do not clean build artifacts",
            dest="NO_CLEAN",
            default=False
        )
        self.add_argument(
            "--archive",
            action="store_true",
            help="Package as an archive file",
            dest="ARCHIVE",
            default=False
        )
        self.add_argument(
            "-f", "--filename",
            action="store",
            help="Output filename",
            dest="FILENAME",
            default=None
        )
        self.add_argument(
            "-a", "--appname",
            action="store",
            help="Application name",
            dest="APPNAME",
            default=None
        )
        self.add_argument(
            "--id",
            action="store",
            help="Application ID",
            dest="ID",
            default=None
        )
        self.add_argument(
            "--appv", "--app-version",
            action="store",
            help="Application version",
            dest="VERSION",
            default=None
        )
        self.add_argument(
            "--author",
            action="store",
            help="Author",
            dest="AUTHOR",
            default=None
        )
        self.add_argument(
            "--publisher",
            action="store",
            help="Publisher",
            dest="PUBLISHER",
            default=None
        )
        self.add_argument(
            "-d", "--description",
            action="store",
            help="Application description",
            dest="DESCRIPTION",
            default=None
        )
        self.add_argument(
            "--pyi-version",
            action="store",
            help="PyInstaller version to be used",
            dest="PYI_VERSION",
            default=None
        )
        self.add_argument(
            "-i", "--icon",
            action="store",
            help="Path to icon file",
            dest="ICON",
            default=None
        )
        self.add_argument(
            "-l", "--license",
            action="store",
            help="Path to license file",
            dest="LICENSE",
            default=None
        )
        self.add_argument(
            "-o", "--outdir",
            action="store",
            help="Path to output directory",
            dest="OUTDIR",
            default=None
        )
        self.add_argument(
            "-r", "--requirements",
            action="store",
            help="Path to pip requirements file",
            dest="REQUIREMENTS",
            default=None
        )
        self.add_argument(
            "--venv",
            action="store",
            help="Path to Python virtual environment",
            dest="VENV",
            default=None
        )
        # Positional argument for the spec file
        self.add_argument(
            "TARGET",
            action="store",
            nargs="*",
            help="Path to Python file(s) or PyInstaller spec file"
        )
        # Add OS-specific arguments
        match system:
            case "Linux":
                self._add_linux_args()
            case "Darwin":
                self._add_macos_args()
            case "Windows":
                self._add_windows_args()

    def _add_linux_args(self) -> None:
        """
        Add Linux-specific arguments
        """
        self.add_argument(
            "--appdata",
            action="store",
            help="Path to AppStream metadata file",
            dest="APPDATA",
            default=None
        )
        self.add_argument(
            "--appimagetool",
            action="store",
            help="Path to appimagetool",
            dest="APPIMAGETOOL",
            default=None
        )
        self.add_argument(
            "--runtime-file",
            action="store",
            help="Path to AppImage runtime",
            dest="RUNTIME_FILE",
            default=None
        )

    def _add_macos_args(self) -> None:
        """
        Add macOS-specific arguments
        """
        self.add_argument(
            "-E", "--enti", "--entitlements",
            action="store",
            help="Path to entitlements file",
            dest="ENTI",
            default=None
        )
        self.add_argument(
            "-C", "--cert", "--certificate",
            action="store",
            help="Common Name of Certificate",
            dest="CERT",
            default=None
        )
        self.add_argument(
            "-K", "--keyc", "--keychain-profile",
            action="store",
            help="Name of stored Keychain Profile",
            dest="KEYC",
            default=None
        )
        self.add_argument(
            "-A", "--apid", "--apple-id",
            action="store",
            help="Apple ID",
            dest="APID",
            default=None
        )
        self.add_argument(
            "-T", "--tmid", "--team-id",
            action="store",
            help="Team ID",
            dest="TMID",
            default=None
        )
        self.add_argument(
            "-P", "--pass", "--password",
            action="store",
            help="App-specific Password",
            dest="PASS",
            default=None
        )

    def _add_windows_args(self) -> None:
        """
        Add Windows-specific arguments
        """
        self.add_argument(
            "--nsis",
            action="store",
            help="Path to NSIS template file",
            dest="NSIS",
            default=None
        )
        self.add_argument(
            "--makensis",
            action="store",
            help="Path to makensis binary",
            dest="MAKENSIS",
            default=None
        )
