from argparse import Namespace
from collections.abc import Callable
from logging import Logger
from os import environ
from os.path import abspath, exists
from pathlib import PosixPath
from platform import system
from typing import Iterator, Optional, Tuple
from pytest import fixture, mark
from _pytest.monkeypatch import MonkeyPatch
from . import *


@fixture(autouse=True)
def change_test_dir(tmp_path: PosixPath, monkeypatch: MonkeyPatch) -> None:
    """
    Fixture to change the current working directory to the test directory

    :param tmp_path: Temporary path
    :type tmp_path: pathlib.PosixPath
    :param monkeypatch: Monkeypatch fixture
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    """
    if exists(".env"):
        environ["ENV_FILE"] = abspath(".env")
    monkeypatch.chdir(tmp_path)


@fixture
def run_cmd() -> Callable[[str], Iterator[str]]:
    """
    Fixture for the run command function

    :return: Run command function
    :rtype: Callable[[str], Iterator[str]]
    """
    return run_command


@fixture
def arg_parser() -> ArgParser:
    """
    Fixture for an instance of the ArgParser class

    :return: Instance of ArgParser with all possible options
    :rtype: pydeployment.arg_parser.ArgParser
    """
    parser = ArgParser()
    parser._add_linux_args()
    parser._add_macos_args()
    parser._add_windows_args()
    return parser


@fixture
def logger() -> Logger:
    """
    Fixture for the build logger

    :return: Build logger
    :rtype: logging.Logger
    """
    return logger_


@fixture
def tmp_file(
        tmp_path: PosixPath
    ) -> Callable[[str, Optional[str]], Tuple[str, Optional[str]]]:
    """
    Fixture for a function to create a temporary directory and file

    :param tmp_path: Temporary path
    :type tmp_path: pathlib.PosixPath
    :return: Temporary file function
    :rtype: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    def file(
            dir_: str="tmp",
            path: Optional[str]=None
        ) -> Tuple[str, Optional[str]]:
        """
        Create a temporary directory and file

        :param dir_: Directory name
        :type dir_: str
        :param path: File name
        :type path: Optional[str]
        :return: Tuple of directory and file paths
        :rtype: Tuple[str, Optional[str]]
        """
        d = tmp_path / dir_
        d.mkdir()
        vals = [str(d)]
        if path:
            p = d / path
            p.write_text("print()", encoding="utf-8")
            vals.append(str(p))
        else:
            vals.append(None)
        return vals
    return file


@fixture
def build_config() -> BuildConfig:
    """
    Fixture for an instance of the BuildConfig class

    :return: Instance of BuildConfig for the system OS
    :rtype: pydeployment.build_config.BuildConfig
    """
    return BuildConfig(system())


@fixture
def config(
        build_config: BuildConfig,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> Namespace:
    """
    Fixture for a test build configuration

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    :return: Test configuration
    :rtype: argparse.Namespace
    """
    d, p = tmp_file(dir_="app", path="app.py")
    vals = (
        ("LOG", "INFO"),
        ("NO_CONFIRM", True),
        ("FILENAME", "tmp"),
        ("APPNAME", "tmp"),
        ("ID", "id.not.found.tmp"),
        ("OUTDIR", d),
        ("TARGET", p)
    )
    cfg = build_config.get_config(skip_validation=True)
    for attr, val in vals:
        setattr(cfg, attr, val)
    return cfg


@fixture
def py() -> str:
    """
    Fixture for the path to the python executable within a virtual environment

    :return: Relative path to python executable
    :rtype: str
    """
    return PYEXE


@fixture
def build(config: Namespace) -> Build:
    """
    Fixture for an instance of the Build class

    :param config: Test configuration
    :type config: argparse.Namespace
    :return: Instance of Build
    :rtype: pydeployment.build.Build
    """
    return Build(config)


@fixture
def build_linux(config: Namespace) -> BuildLinux:
    """
    Fixture for an instance of the BuildLinux class

    :param config: Test configuration
    :type config: argparse.Namespace
    :return: Instance of BuildLinux
    :rtype: pydeployment.build.BuildLinux
    """
    return BuildLinux(config)


@fixture
def build_macos(config: Namespace) -> BuildMacos:
    """
    Fixture for an instance of the BuildMacos class

    :param config: Test configuration
    :type config: argparse.Namespace
    :return: Instance of BuildMacos
    :rtype: pydeployment.build.BuildMacos
    """
    return BuildMacos(config)


@fixture
def build_windows(config: Namespace) -> BuildWindows:
    """
    Fixture for an instance of the BuildWindows class

    :param config: Test configuration
    :type config: argparse.Namespace
    :return: Instance of BuildWindows
    :rtype: pydeployment.build.BuildWindows
    """
    return BuildWindows(config)


@fixture
def mock_build_config() -> BuildConfig:
    """
    Fixture for the BuildConfig class to be used for mocking the `get_config`
    method

    :return: BuildConfig class
    :rtype: pydeployment.build_config.BuildConfig
    """
    return BuildConfig


@fixture
def main() -> Callable[[], int]:
    """
    Fixture for the main function

    :return: Main function
    :rtype: Callable[[], int]
    """
    return main_
