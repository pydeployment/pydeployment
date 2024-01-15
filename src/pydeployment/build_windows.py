from argparse import Namespace
from glob import glob
from os.path import abspath, basename, join 
from shutil import copy, make_archive, move
from .build import Build


class BuildWindows(Build):
    """
    Windows build class

    :param config: Configuration dictionary
    :type config: argparse.Namespace
    """
    def __init__(self, config: Namespace) -> None:
        """
        Constructor
        """
        super().__init__(config=config)
        self.dir = join(self.dir, "windows")
        # Override variables with platform-specific variables
        self.override_platform_vars("WINDOWS_")
        # Handle defaults
        defaults = {
            "ICON": "default.ico",
            "NSIS": "build.nsi"
        }
        for k, v in defaults.items():
            if not self.is_set(k):
                setattr(self.config, k, join(self.dir, v))
        if not self.is_set("MAKENSIS"):
            self.config.MAKENSIS = self._get_makensis()
        # Add to PyInstaller command line arguments
        if self.config.MODE == "PY":
            self.validate_pyi_arg(["-i", "--icon"], self.config.ICON)

    def _get_makensis(self) -> str:
        """
        Get makensis

        :return: Path to makensis
        :rtype: str
        """
        return join(self.dir, "NSISPortable", "App", "NSIS", "makensis.exe")

    def _make_app_from_appdir(self, appdir: str) -> str:
        """
        Given an app directory `appdir`, make an installer

        :param appdir: Path to app directory
        :type appdir: str
        :return: Package filename
        :rtype: str
        """
        self.logger.info(f"Packaging app: {basename(appdir)}")
        self.logger.debug(f"Copying build files")
        # Copy NSI template file
        nsis = join("build", "build.nsi")
        copy(self.config.NSIS, join("build", "build.nsi"))
        # Copy icon file
        copy(self.config.ICON, "build")
        # Copy license file
        if self.is_set("LICENSE"):
            copy(self.config.LICENSE, join("build", "LICENSE.txt"))
        self.logger.debug(f"Copied build files")
        # Create build info files
        self.logger.debug(f"Creating build info files")
        nsis_params = {
            "APPDIR": abspath(appdir),
            "FILENAME": self.config.FILENAME,
            "APPNAME": self.config.APPNAME,
            "VERSION": self.config.VERSION,
            "AUTHOR": self.config.AUTHOR,
            "PUBLISHER": self.config.PUBLISHER,
            "DESCRIPTION": self.config.DESCRIPTION,
            "ICON": basename(self.config.ICON),
            "LICENSE": "LICENSE.txt" if self.is_set("LICENSE") else None,
            "INSTALLSIZE": self.calc_dir_size(appdir),
            "ARCH": self.arch
        }
        for k, v in nsis_params.items():
            with open(join("build", k), "w") as file:
                file.write(str(v))
                file.close()
        self.logger.debug(f"Created build info files")
        self.logger.info("Running makensis")
        self.run_command(f"{self.config.MAKENSIS} {nsis}", self.logger.info)
        self.logger.debug("Finished running makensis")
        package = glob(join("build", "*.exe"))[0]
        # Move file to current working directory
        self.logger.debug(f"Moving app to current working directory")
        move(package, basename(package))
        self.logger.debug(f"Moved app to current working directory")
        self.logger.debug(f"Packaged app: {basename(package)}")
        return basename(package)

    def make_app(self) -> str:
        """
        Make an installer

        :return: Package filename
        :rtype: str
        """
        self.run_pyinstaller(self.config.TARGET)
        appdir = glob(join("dist", "*"))[0]
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
        package = f"{self.package}-windows.zip"
        if self.is_set("LICENSE"):
            copy(self.config.LICENSE, appdir)
        self.logger.info("Packaging app into archive")
        make_archive(package.removesuffix(".zip"), "zip", appdir)
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
