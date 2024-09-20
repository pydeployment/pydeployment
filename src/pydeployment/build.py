from argparse import Namespace
from collections.abc import Callable
from importlib.resources import files
from os import access, chmod, makedirs, W_OK
from os.path import abspath, basename, exists, join
from pathlib import Path
from platform import machine
from shutil import Error as ShutilError, move, rmtree
from stat import S_IWUSR
from typing import Any, Dict, List
from venv import create
from . import DISPLAY_ORDER, PYEXE, PYI_VERSION, run_command
from .logger import logger


class Build:
    """
    Base build class

    :param config: Configuration
    :type config: argparse.Namespace
    """
    def __init__(self, config: Namespace) -> None:
        """
        Constructor
        """
        self.config = config
        self.logger = logger
        self.logger.setLevel(self.config.LOG)
        self.dir = abspath(files(__package__))
        self.arch = machine()
        if self.is_set("VENV"):
            self.venv = self.config.VENV
        else:
            self.venv = abspath(join("build", "venv"))
        self.py = join(self.venv, PYEXE)
        self.package = self.config.FILENAME
        if self.config.VERSION:
            self.package += f"-{self.config.VERSION}"
        self.package += f"-{self.arch}"
        if self.is_set("PYI_VERSION"):
            self.pyi_version = self.config.PYI_VERSION
        else:
            self.pyi_version = PYI_VERSION
        # Remove --distpath option from PyInstaller arguments
        if "--distpath" in self.config.PYI_ARGS:
            args = self.config.PYI_ARGS.split()
            index = args.index("--distpath")
            for i in range(2):
                args.pop(index)
            self.config.PYI_ARGS = " ".join(args)

    def override_platform_vars(self, prefix: str) -> int:
        """
        Override variables specific to the platform, denoted by `prefix`

        :param prefix: Prefix to check
        :type prefix: str
        :return: Return code
        :rtype: int
        """
        for key in vars(self.config).keys():
            if key.startswith(prefix):
                setattr(
                    self.config,
                    key.removeprefix(prefix),
                    getattr(self.config, key)
                )
        return 0

    def validate_pyi_arg(self, opts: List[str], arg: str) -> int:
        """
        Check if the PyInstaller arguments string contains any of the options
        in `opts` and if not then add the first option and `arg` to the
        end of the arguments string but before `--` as this option is used to
        parse spec file arguments

        :param opts: Options to check
        :type opts: List[str]
        :param arg: Argument to add
        :type arg: str
        :return: Return code
        :rtype: int
        """
        args = self.config.PYI_ARGS.split()
        if all(opt not in args for opt in opts):
            try:
                index = args.index("--")
                for item in (arg, opts[0]):
                    args.insert(index, item)
                self.config.PYI_ARGS = " ".join(args)
            except ValueError:
                self.config.PYI_ARGS += f" {opts[0]} {arg}"
        return 0

    def is_set(self, key: str) -> bool:
        """
        Check if a value in the config namespace exists and is not empty

        :param key: Key to check
        :type key: str
        :return: True if a key in the config exists and is not empty
        :rtype: bool
        """
        return bool(hasattr(self.config, key) and getattr(self.config, key))

    def calc_dir_size(self, path: str) -> int:
        """
        Calculate the size in kilobytes of the directory at `path`

        :param path: Path to directory
        :type path: str
        :return: Size of directory in kilobytes
        :rtype: int
        """
        # Size of directory
        directory = Path(path).stat().st_size
        # Size of contents
        contents = sum(file.stat().st_size for file in Path(path).rglob("*"))
        return max((directory + contents) // 1024, 1024)

    def run_command(
            self,
            cmd: str,
            method: Callable[[str], None]=None,
            **kwargs: Dict[str, Any]
        ) -> str:
        """
        Run a command

        :param cmd: Command to run
        :type cmd: str
        :param method: Logger method
        :type method: Callable[[str], None]
        :param kwargs: Keyword arguments to pass to `run_command` function
        :type kwargs: Dict[str, Any]
        :return: Command output
        :rtype: str
        """
        self.logger.debug(f"Command: {cmd}")
        output = ""
        for line in run_command(cmd, **kwargs):
            output += line
            if method:
                method(line.rstrip())
        return output.rstrip()

    def run_pyinstaller(self, target: str) -> int:
        """
        Run PyInstaller with the given target file `target`

        :param target: Path to target file
        :type target: str
        :return: Return code
        :rtype: int
        """
        self.logger.info("Running PyInstaller")
        log = self.config.LOG if self.config.LOG != "WARNING" else "WARN"
        cmd = f"{self.py} -OO -m PyInstaller --noconfirm --log {log} {target}"
        if self.is_set("PYI_ARGS"):
            cmd += f" {self.config.PYI_ARGS}"
        self.run_command(cmd, None)
        if self.config.MODE == "PY":
            basename_py = basename(target.removesuffix(".py"))
            args = self.config.PYI_ARGS.split()
            for opt in ("-n", "--name"):
                if opt in args:
                    index = args.index(opt)
                    basename_py = args[index + 1]
            if "--specpath" in args:
                index = args.index("--specpath")
                basename_py = join(args[index + 1], basename_py)
            generated_spec = f"{basename_py}.spec"
            move(generated_spec, "build")
        self.logger.debug("Finished running PyInstaller")
        return 0

    def _validate_paths(self) -> int:
        """
        Check that all relevant paths in the configuration exist

        :return: Return code
        :rtype: int
        """
        keys = (
            "ICON", "LICENSE", "VENV", "REQUIREMENTS", "APPDATA",
            "APPIMAGETOOL", "ENTI", "NSIS", "MAKENSIS"
        )
        for key in keys:
            if self.is_set(key):
                path = getattr(self.config, key)
                if not exists(path):
                    self.logger.error(f"{path} not found")
                    return 1
        return 0

    def _format_options(self) -> str:
        """
        Format build options for display

        :return: Build options in a format for display
        :rtype: str
        """
        cfg = vars(self.config)
        display = {
            k: cfg[k] for k in DISPLAY_ORDER if k in cfg.keys() and cfg[k]
        }
        options = "OPTIONS:\n{\n"
        options += "".join(f"\t{k}: {v}\n" for k, v in display.items())
        options += "}"
        return options

    def _confirm_delete_dirs(self) -> int:
        """
        Ask user for confirmation to delete build directories
        
        :return: Return code
        :rtype: int
        """
        dirs = []
        for builddir in ("build", "dist"):
            if exists(builddir):
                dirs.append(builddir)
        builddirs = ", ".join(dirs)
        self.logger.warning(
            f"Continuing will delete the directories: {builddirs}"
        )
        if not self.config.NO_CONFIRM and self.config.LOG != "ERROR":
            response = input("Continue (Y/n)? ").upper()
        else:
            response = "Y"
        if response == "Y":
            self._clean()
            return 0
        else:
            return 1

    def _set_up_venv(self) -> int:
        """
        Set up a Python virtual environment

        :return: Return code
        :rtype: int
        """
        self.logger.info(
            f"Setting up virtual environment: {self.venv}"
        )
        create(
            self.venv,
            system_site_packages=True,
            clear=True,
            with_pip=True,
            upgrade_deps=True
        )
        if self.is_set("REQUIREMENTS"):
            self.run_command(
                f"{self.py} -m pip install -r {self.config.REQUIREMENTS}",
                self.logger.info
            )
        cmd = f"{self.py} -m pip install pyinstaller"
        if self.pyi_version:
            cmd += f"=={self.pyi_version}"
        self.run_command(cmd, self.logger.info)
        self.logger.debug(f"Set up virtual environment: {self.venv}")
        return 0

    def _clean(self) -> int:
        """
        Delete build artifacts

        :return: Return code
        :rtype: int
        """
        self.logger.debug("Deleting build artifacts")
        for builddir in ("build", "dist"):
            if not exists(builddir):
                continue
            self.logger.debug(f"Deleting {builddir}")
            # Address potential access permission error on Windows
            for file in Path(builddir).rglob("*"):
                if not access(file, W_OK):
                    chmod(file, S_IWUSR)
            rmtree(builddir)
            self.logger.debug(f"Deleted {builddir}")
        self.logger.debug("Build artifacts deleted")
        return 0

    def _move_app(self, package: str) -> int:
        """
        Move created app
        
        :param package: Package name
        :type package: str
        :return: Return code
        :rtype: int
        """
        self.logger.debug(f"Moving {package} to {self.config.OUTDIR}")
        path = join(self.config.OUTDIR, basename(package))
        makedirs(self.config.OUTDIR, exist_ok=True)
        try:
            move(package, path)
        except ShutilError as e:
            self.logger.error(e)
            return 1
        self.logger.debug(f"Package moved to {path}")
        return 0

    def run(self) -> int:
        """
        Build the package

        :return: Return code
        :rtype: int
        """
        # Validate paths
        result = self._validate_paths()
        if result:
            return result
        # Display build options
        self.logger.info(self._format_options())
        if self.config.LOG == "DEBUG" or self.config.LOG == "INFO":
            if not self.config.NO_CONFIRM:
                response = input("Confirm build (Y/n)? ").upper()
                if response != "Y":
                    return 1
        # Delete existing build directories
        if exists("build") or exists("dist"):
            result = self._confirm_delete_dirs()
            if result:
                return result
        # Set up virtual environment
        if not self.is_set("VENV"):
            self._set_up_venv()
        # Build package
        if not self.config.ARCHIVE:
            package = self.make_app()
        else:
            package = self.make_arc()
        if isinstance(package, int):
            return package
        # Delete build artifacts
        if not self.config.NO_CLEAN:
            self._clean()
        # Move application
        result = self._move_app(package)
        if result:
            return result
        self.logger.info(f"{basename(package)} built successfully")
        return 0
