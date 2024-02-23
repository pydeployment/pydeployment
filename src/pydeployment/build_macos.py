from argparse import Namespace
from glob import glob
from os import sep, symlink
from os.path import basename, dirname, join
from re import sub
from shutil import copy, make_archive, move
from .build import Build


class BuildMacos(Build):
    """
    macOS build class

    :param config: Configuration dictionary
    :type config: argparse.Namespace
    """
    def __init__(self, config: Namespace) -> None:
        """
        Constructor
        """
        super().__init__(config=config)
        self.dir = join(self.dir, "macos")
        # Override variables with platform-specific variables
        self.override_platform_vars("MACOS_")
        # Handle defaults
        defaults = {
            "ICON": "default.icns",
            "ENTI": "entitlements.plist"
        }
        for k, v in defaults.items():
            if not self.is_set(k):
                setattr(self.config, k, join(self.dir, v))
        # Add to PyInstaller command line arguments
        if self.config.MODE == "PY":
            self.validate_pyi_arg(["-i", "--icon"], self.config.ICON)
            if not self.config.ARCHIVE:
                self.validate_pyi_arg(["-w", "--windowed", "--noconsole"], "")

    def _notarize_app(self, appdir: str) -> int:
        """
        Notarize the app at `appdir`

        :param appdir: Path to app bundle
        :type appdir: str
        :return: Return code
        :rtype: int
        """
        self.logger.info(f"Notarizing: {basename(appdir)}")
        zip = f"{self.package}.zip"
        self.run_command(
            f"ditto -ck --sequesterRsrc --keepParent '{appdir}' '{zip}'",
            None
        )
        if self.is_set("KEYC"):
            self.logger.info(f"Using keychain profile: {self.config.KEYC}")
            self.run_command(
                f"xcrun notarytool submit '{zip}' "
                f"--keychain-profile '{self.config.KEYC}' "
                "--wait",
                self.logger.info
            )
        elif all((
            self.is_set("APID"), self.is_set("TMID"), self.is_set("PASS")
        )):
            self.logger.info(f"Using Apple ID: {self.config.APID}")
            self.run_command(
                f"xcrun notarytool submit '{zip}' "
                f"--apple-id '{self.config.APID}' "
                f"--team-id '{self.config.TMID}' "
                f"--password '{self.config.PASS}' "
                "--wait",
                self.logger.info
            )
        else:
            return 1
        self.run_command(f"xcrun stapler staple '{appdir}'", self.logger.info)
        self.logger.debug(f"Notarized: {basename(appdir)}")
        return 0

    def _build_dmg(self, appdir: str) -> str:
        """
        Build DMG for the app bundle located at `appdir`

        :param appdir: Path to app bundle
        :type appdir: str
        :return: Path to built DMG
        :rtype: str
        """
        package = f"{self.package}.dmg"
        self.logger.info(f"Building DMG: {package}")
        # Create a directory to be converted to DMG
        dmg = join("build", "build.dmg")
        self.run_command(
            f"hdiutil create -size {self.calc_dir_size(appdir)}k -fs HFS+ "
            f"-volname '{self.config.APPNAME}' -o '{dmg}'",
            self.logger.info
        )
        # Get the name of the DMG directory
        output = self.run_command(f"hdiutil attach '{dmg}'", self.logger.info)
        dmgdir = output.split("\t")[-1]
        # Move the app bundle to the DMG directory
        self.logger.debug(f"Moving {basename(appdir)} to {dmgdir}")
        move(appdir, dmgdir)
        self.logger.debug(f"Moved {basename(appdir)} to {dmgdir}")
        # Create a symbolic link to Applications directory
        src = join(sep, "Applications")
        self.logger.debug(f"Creating symbolic link: {src} at {dmgdir}")
        symlink(src, join(dmgdir, basename(src)))
        self.logger.debug(f"Created symbolic link: {src} at {dmgdir}")
        # Copy icon to the DMG directory
        self.logger.debug(f"Setting icon: {basename(self.config.ICON)}")
        volumeicon = join(dmgdir, ".VolumeIcon.icns")
        copy(self.config.ICON, volumeicon)
        self.run_command(f"SetFile -c icnC '{volumeicon}'", None)
        self.run_command(f"SetFile -a C '{dmgdir}'", None)
        self.logger.debug(f"Set icon: {basename(self.config.ICON)}")
        # Detach DMG directory
        self.run_command(f"hdiutil detach '{dmgdir}'", self.logger.info)
        # Convert DMG file to immutable DMG
        self.run_command(
            f"hdiutil convert '{dmg}' -format UDZO -o '{package}'",
            self.logger.info
        )
        self.logger.debug(f"Built DMG: {package}")
        return package

    def _make_app_from_appdir(self, appdir: str) -> str:
        """
        Given an app directory `appdir`, make a DMG with an app bundle

        :param appdir: Path to app directory
        :type appdir: str
        :return: Package filename
        :rtype: str
        """
        self.logger.info(f"Packaging app: {basename(appdir)}")
        # Check if using stored keychain profile for notarization
        uses_keyc = self.is_set("KEYC")
        # Check if using app-specific password for notarization
        uses_apid = all((
            self.is_set("APID"), self.is_set("TMID"), self.is_set("PASS")
        ))
        # Notarize app
        if self.is_set("CERT") and any((uses_keyc, uses_apid)):
            self._notarize_app(appdir)
        # Build DMG
        package = self._build_dmg(appdir)
        self.logger.debug(f"Packaged app: {package}")
        return package

    def _sub(self, pattern: str, repl: str, path: str) -> int:
        """
        Replace all text matching everything after `pattern` but before a
        comma, close parenthesis, or new line with `repl` for the file at
        `path`

        :param pattern: Pattern to match
        :type pattern: str
        :param repl: String to insert
        :type repl: str
        :param path: Path to file
        :type path: str
        :return: Return code
        :rtype: int
        """
        contents = open(path, "r").read()
        # Matches string between `pattern` at the beginning and anything but a
        # comma or close parenthesis at the end
        expr = f"(?<={pattern})(.*)(?<![,)])"
        if contents != sub(expr, repl, contents):
            with open(path, "w") as file:
                file.write(sub(expr, repl, contents))
                file.close()
        return 0

    def make_app(self) -> str:
        """
        Make a DMG with an app bundle

        :return: Package filename
        :rtype: str
        """
        if self.config.MODE == "SPEC":
            basename_spec = basename(self.config.TARGET.removesuffix(".spec"))
            build_spec = join(
                dirname(self.config.TARGET),
                f"{basename_spec}~.spec"
            )
            copy(self.config.TARGET, build_spec)
            self._sub("version=", f"'{self.config.VERSION}'", build_spec)
            if self.is_set("CERT"):
                self._sub(
                    "codesign_identity=", f"'{self.config.CERT}'", build_spec
                )
            self._sub(
                "entitlements_file=", f"'{self.config.ENTI}'", build_spec
            )
            self._sub(
                "bundle_identifier=", f"'{self.config.ID}'", build_spec
            )
            self.run_pyinstaller(build_spec)
            move(build_spec, "build")
        else:
            if self.is_set("CERT"):
                self.validate_pyi_arg(
                    ["--codesign-identity"], f"'{self.config.CERT}'"
                )
            self.validate_pyi_arg(
                ["--osx-entitlements-file"], f"'{self.config.ENTI}'"
            )
            self.validate_pyi_arg(
                ["--osx-bundle-identifier"], f"'{self.config.ID}'"
            )
            self.run_pyinstaller(self.config.TARGET)
        appdir = glob(join("dist", "*.app"))[0]
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
        package = f"{self.package}-macos.tar.xz"
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
