from argparse import Namespace
from glob import glob
from os import makedirs, symlink
from os.path import basename, isdir, join, relpath, splitext
from shutil import copy, make_archive, move
from . import LINUX_DESKTOP_KEYS as KEYS
from .build import Build


class BuildLinux(Build):
    """
    Linux build class

    :param config: Configuration dictionary
    :type config: argparse.Namespace
    """
    def __init__(self, config: Namespace) -> None:
        """
        Constructor
        """
        super().__init__(config=config)
        self.dir = join(self.dir, "linux")
        # Override variables with platform-specific variables
        self.override_platform_vars("LINUX_")
        # Handle defaults
        if not self.is_set("ICON"):
            self.config.ICON = join(self.dir, "default.png")
        if not self.is_set("APPIMAGETOOL"):
            self.config.APPIMAGETOOL = self._get_appimagetool()
        if not self.is_set("RUNTIME_FILE"):
            self.config.RUNTIME_FILE = self._get_appimage_runtime()

    def _get_appimagetool(self) -> str:
        """
        Get appimagetool

        :return: Path to appimagetool
        :rtype: str
        """
        tool = f"appimagetool-{self.arch}.AppImage"
        return join(self.dir, "appimagetool", tool)

    def _get_appimage_runtime(self) -> str:
        """
        Get AppImage runtime

        :return: Path to AppImage runtime
        :rtype: str
        """
        runtime = f"runtime-{self.arch}"
        return join(self.dir, "appimagetool", runtime)

    def _make_desktop_file(self, appdir: str, apprun: str) -> int:
        """
        Make a desktop file at destination `appdir` including all environment
        variables from `KEYS` which are set

        :param appdir: Path to app directory
        :type appdir: str
        :param apprun: Name of executable file
        :type apprun: str
        :return: Return code
        :rtype: int
        """
        # Path to desktop file
        path = join(appdir, "usr", "share", "applications")
        makedirs(path)
        path = join(path, f"{self.config.ID}.desktop")
        self.logger.debug(f"Creating desktop file: {basename(path)}")
        # Handle desktop entry defaults
        defaults = {
            "Type": "Application",
            "Name": self.config.APPNAME,
            "Exec": apprun,
            "Categories": "Utility"
        }
        for k, v in defaults.items():
            if not self.is_set(k):
                setattr(self.config, k, v)
        # Special case for icon file
        if not self.is_set("Icon"):
            self.config.Icon = basename(splitext(self.config.ICON)[0])
        # Special case for version
        setattr(self.config, "X-AppImage-Version", self.config.VERSION)
        with open(path, "w") as desktop:
            desktop.write("[Desktop Entry]\n")
            for key in KEYS:
                if self.is_set(key):
                    val = getattr(self.config, key)
                    desktop.write(f"{key}={val}\n")
            desktop.close()
        self.logger.debug(f"Created desktop file: {basename(path)}")
        self.logger.debug("Creating symbolic link to desktop file")
        symlink(relpath(path, appdir), join(appdir, basename(path)))
        self.logger.debug("Created symbolic link to desktop file")
        return 0

    def _add_appdata(self, appdir: str) -> int:
        """
        Add AppStream metadata file to the app directory `appdir`

        :param appdir: Path to app directory
        :type appdir: str
        :return: Return code
        :rtype: int
        """
        datadir = join(appdir, "usr", "share", "metainfo")
        self.logger.debug(f"Creating data directory: {datadir}")
        makedirs(datadir)
        self.logger.debug(f"Created data directory: {datadir}")
        self.logger.debug(f"Copying {self.config.APPDATA} to {datadir}")
        copy(self.config.APPDATA, datadir)
        self.logger.debug(f"Copied {self.config.APPDATA} to {datadir}")
        return 0

    def _make_app_from_appdir(self, appdir: str) -> str:
        """
        Given an app directory `appdir`, make an AppImage

        :param appdir: Path to app directory
        :type appdir: str
        :return: Package filename
        :rtype: str
        """
        self.logger.info(f"Packaging app: {basename(appdir)}")
        # Rename executable to AppRun
        self.logger.debug("Renaming executable to AppRun")
        apprun = basename(appdir)
        move(join(appdir, apprun), join(appdir, "AppRun"))
        self.logger.debug("Renamed executable to AppRun")
        # Create desktop file
        self._make_desktop_file(appdir, apprun)
        # Copy icon file to app directory
        self.logger.debug(f"Copying icon file to {basename(appdir)}")
        copy(self.config.ICON, appdir)
        self.logger.debug(f"Copied icon file to {basename(appdir)}")
        # Create a symbolic link for .DirIcon
        self.logger.debug(f"Creating symbolic link for .DirIcon")
        symlink(basename(self.config.ICON), join(appdir, ".DirIcon"))
        self.logger.debug(f"Created symbolic link for .DirIcon")
        # Add appstream metadata
        if self.is_set("APPDATA"):
            self._add_appdata(appdir)
        # Run appimagetool
        self.logger.info("Running appimagetool")
        package = f"{self.package}.AppImage"
        appname = package.removesuffix(f"-{self.arch}.AppImage")
        verbose = "-v" if self.config.LOG == "DEBUG" else ""
        if self.config.RUNTIME_FILE:
            runtime = f"--runtime-file {self.config.RUNTIME_FILE}"
        else:
            runtime = ""
        # Set environment
        env = {
            "APPIMAGETOOL_APP_NAME": appname,
            "ARCH": self.arch
        }
        self.run_command(
            f"{self.config.APPIMAGETOOL} {verbose} {runtime} {appdir}",
            self.logger.debug, env=env
        )
        self.logger.debug(f"Packaged app: {package}")
        return package

    def make_app(self) -> str | int:
        """
        Make an AppImage

        :return: Package filename or return code
        :rtype: str | int
        """
        self.run_pyinstaller(self.config.TARGET)
        appdir = glob(join("dist", "*"))[0]
        if not isdir(appdir):
            self.logger.error(
                "PyInstaller appears to have created a one-file bundled "
                "executable. Be sure to create a one-folder bundle instead."
            )
            return 1
        return self._make_app_from_appdir(appdir)

    def _make_arc_from_appdir(self, appdir: str) -> str:
        """
        Given an app directory `appdir`, make an archive

        :param appdir: Path to app directory
        :type appdir: str
        :return: Package filename
        :rtype: str
        """
        self.logger.info(f"Packaging app: {basename(appdir)}")
        package = f"{self.package}-linux.tar.xz"
        if self.is_set("LICENSE"):
            copy(self.config.LICENSE, appdir)
        self.logger.info("Packaging app into archive")
        make_archive(package.removesuffix(".tar.xz"), "xztar", appdir)
        self.logger.debug(f"Packaged app: {package}")
        return package

    def make_arc(self) -> str:
        """
        Make an archive

        :return: Package filename
        :rtype: str
        """
        self.run_pyinstaller(self.config.TARGET)
        appdir = "dist"
        return self._make_arc_from_appdir(appdir)
