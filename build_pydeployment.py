from argparse import ArgumentParser
from glob import glob
from os.path import dirname, exists, join
from shutil import rmtree
from sys import exit
from venv import create
from src.pydeployment import PYEXE, run_command
from src.pydeployment.logger import logger


class BuildPyDeployment:
    """
    Class to build PyDeployment
    """
    def __init__(self) -> None:
        """
        Constructor
        """
        parser = self._set_up_parser()
        self.args = parser.parse_args()
        self.logger = logger
        self.logger.setLevel(self.args.LOG)
        self.srcdir = dirname(__file__)

    def _set_up_parser(self) -> ArgumentParser:
        """
        Set up argument parser
        
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        """
        parser = ArgumentParser(
            prog="build_pydeployment.py",
            description="Build PyDeployment"
        )
        parser.add_argument(
            "--log",
            action="store",
            help="Set the log level",
            dest="LOG",
            choices=("DEBUG", "INFO", "WARNING", "ERROR"),
            default="INFO"
        )
        parser.add_argument(
            "--no-clean",
            action="store_true",
            help="Do not clean build artifacts",
            dest="NO_CLEAN",
            default=False
        )
        parser.add_argument(
            "-o", "--outdir",
            action="store",
            help="Path to output directory",
            dest="OUTDIR",
            default="dist"
        )
        return parser

    def _run_command(self, cmd: str) -> int:
        """
        Run a command

        :param cmd: Command to run
        :type cmd: str
        :return: Return code
        :rtype: int
        """
        self.logger.debug(f"Command: {cmd}")
        for line in run_command(cmd):
            self.logger.info(line.rstrip())
        return 0

    def _set_up_venv(self) -> int:
        """
        Set up a Python virtual environment

        :return: Return code
        :rtype: int
        """
        venv = join(self.srcdir, "build")
        self.logger.info(f"Setting up virtual environment: {venv}")
        self.py = join(venv, PYEXE)
        create(venv, clear=True, with_pip=True, upgrade_deps=True)
        self.logger.debug(f"Installing pip dependency: build")
        self._run_command(f"{self.py} -m pip install build")
        self.logger.debug(f"Set up virtual environment: {venv}")
        return 0

    def _build_pip(self) -> int:
        """
        Build PyDeployment as a pip project

        :return: Return code
        :rtype: int
        """
        self.logger.info("Building pip project")
        self._run_command(
            f"{self.py} -m build -o {self.args.OUTDIR} {self.srcdir}"
        )
        self.logger.debug("Built pip project")
        return 0

    def _clean(self) -> int:
        """
        Delete build directories

        :return: Return code
        :rtype: int
        """
        builddirs = (
            join(self.srcdir, "build"),
            glob(join(self.srcdir, join("src", "*.egg-info")))[0]
        )
        for builddir in builddirs:
            self.logger.debug(f"Removing {builddir}")
            rmtree(builddir)
            self.logger.debug(f"Removed {builddir}")
        return 0

    def main(self) -> int:
        """
        Build PyDeployment

        :return: Return code
        :rtype: int
        """
        result = self._set_up_venv()
        if result:
            return 1
        result = self._build_pip()
        if result:
            return 1
        if not self.args.NO_CLEAN:
            self.logger.debug("Removing build directories")
            result = self._clean()
            if result:
                return 1
            self.logger.debug("Removed build directories")
        self.logger.info("PyDeployment built successfully")
        return 0


if __name__ == "__main__":
    bd = BuildPyDeployment()
    exit(bd.main())
