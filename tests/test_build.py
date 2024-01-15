from collections.abc import Callable
from contextlib import nullcontext as does_not_raise
from os import mkdir
from os.path import exists, join
from platform import machine, python_compiler
from typing import Optional, Tuple
from pytest import mark, raises
from _pytest.capture import CaptureFixture
from _pytest.python_api import RaisesContext
from . import Build


@mark.order(4)
def test_build(build: Build) -> None:
    """
    Test Build constructor

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    """
    assert build.package == f"tmp-{machine()}"
    assert "--distpath" not in build.config.PYI_ARGS


@mark.order(4)
def test_build_override_platform_vars(build: Build) -> None:
    """
    Test `override_platform_vars` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    """
    build.config.LINUX_FILENAME = "test"
    build.override_platform_vars("LINUX_")
    assert build.config.FILENAME == "test"


@mark.order(4)
@mark.parametrize(
    "pyi_args,result",
    (
        ("", " -o opt"),
        ("t", "t -o opt"),
        ("-- t", "-o opt -- t"),
        ("t -- t", "t -o opt -- t"),
        ("-o opt", "-o opt"),
        ("t --option opt", "t --option opt"),
        ("-o opt -- t", "-o opt -- t"),
        ("t --option opt -- t", "t --option opt -- t")
    )
)
def test_build_validate_pyi_arg(
        build: Build,
        pyi_args: str,
        result: str
    ) -> None:
    """
    Test `validate_pyi_arg` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    :param pyi_args: PyInstaller arguments
    :type pyi_args: str
    :param result: Expected result
    :type result: str
    """
    build.config.PYI_ARGS = pyi_args
    build.validate_pyi_arg(["-o", "--option"], "opt")
    assert build.config.PYI_ARGS == result


@mark.order(4)
def test_build_is_set(build: Build) -> None:
    """
    Test `is_set` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    """
    assert not build.is_set("ARG")
    build.config.ARG = None
    assert not build.is_set("ARG")
    build.config.ARG = "arg"
    assert build.is_set("ARG")


@mark.order(4)
def test_build_calc_dir_size(
        build: Build,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `calc_dir_size` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    d, _ = tmp_file()
    assert isinstance(build.calc_dir_size(d), int)


@mark.order(4)
@mark.parametrize(
    "command,output,exception",
    (
        ("echo test", "test", does_not_raise()),
        ("", "", raises(Exception))
    )
)
def test_build_run_command(
        build: Build,
        command: str,
        output: str,
        exception: does_not_raise | RaisesContext
    ) -> None:
    """
    Test `run_command` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    :param command: Command
    :type command: str
    :param output: Expected output
    :type output: str
    :param exception: Expected exception context
    :type exception: contextlib.nullcontext | _pytest.python_api.RaisesContext
    """
    if command and python_compiler()[:3] == "MSC":
        command = f"cmd /c {command}"
    with exception:
        assert build.run_command(command) == output


@mark.order(4)
def test_build_run_pyinstaller(
        build: Build,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]],
        capfd: CaptureFixture
    ) -> None:
    """
    Test `run_pyinstaller` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    :param capfd: Capture fixture
    :type capfd: _pytest.capture.CaptureFixture
    """
    _, p = tmp_file(path="tmp.py")
    build._set_up_venv()
    build.run_pyinstaller(p)
    output = capfd.readouterr()
    success = "INFO: Building COLLECT COLLECT-00.toc completed successfully."
    assert success in output.err


@mark.order(4)
def test_build_validate_paths(
        build: Build,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_validate_paths` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    _, p = tmp_file(path="tmp.txt")
    build.LICENSE = p
    assert build._validate_paths() == 0


@mark.order(4)
def test_build_format_options(build: Build) -> None:
    """
    Test `_format_options` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    """
    options = build._format_options()
    assert options.startswith("OPTIONS:\n{\n")
    assert options.endswith("}")


@mark.order(4)
def test_build_confirm_delete_dirs(build: Build) -> None:
    """
    Test `_confirm_delete_dirs` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    """
    assert build._confirm_delete_dirs() == 0


@mark.order(4)
def test_build_set_up_venv(
        build: Build,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]],
        py: str
    ) -> None:
    """
    Test `_set_up_venv` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    :param py: Relative path to python executable
    :type py: str
    """
    d, _ = tmp_file()
    build.venv = d
    build.py = join(build.venv, py)
    build._set_up_venv()
    assert exists(build.py) or exists(f"{build.py}.exe")


@mark.order(4)
def test_build_clean(build: Build) -> None:
    """
    Test `_clean` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    """
    assert build._clean() == 0


@mark.order(4)
def test_build_move_app(
        build: Build,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_move_app` method

    :param build: Instance of Build
    :type build: pydeployment.build.Build
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    _, p = tmp_file(path="tmp.txt")
    assert build._move_app(p) == 0
