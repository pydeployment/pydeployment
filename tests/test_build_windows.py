from collections.abc import Callable
from os import mkdir
from os.path import exists
from platform import system
from shutil import move
from typing import Optional, Tuple
from pytest import mark
from . import BuildWindows

windows = mark.skipif(system() != "Windows", reason="System does not match.")


@mark.order(7)
@windows
def test_build_windows(build_windows: BuildWindows) -> None:
    """
    Test BuildWindows constructor

    :param build_windows: Instance of BuildWindows
    :type build_windows: pydeployment.build.BuildWindows
    """
    assert exists(build_windows.config.ICON)
    assert exists(build_windows.config.NSIS)


@mark.order(7)
@windows
def test_build_windows_get_makensis(build_windows: BuildWindows) -> None:
    """
    Test `_get_makensis` method

    :param build_windows: Instance of BuildWindows
    :type build_windows: pydeployment.build.BuildWindows
    """
    assert exists(build_windows._get_makensis())


@mark.order(7)
@windows
def test_build_windows_make_app_from_appdir(
        build_windows: BuildWindows,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_make_app_from_appdir` method

    :param build_windows: Instance of BuildWindows
    :type build_windows: pydeployment.build.BuildWindows
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    # Create build directory for this test
    mkdir("build")
    d, _ = tmp_file(dir_="test", path="test")
    package = build_windows._make_app_from_appdir(d)
    assert exists(package)


@mark.order(7)
@windows
def test_build_windows_make_app(build_windows: BuildWindows) -> None:
    """
    Test `make_app` method

    :param build_windows: Instance of BuildWindows
    :type build_windows: pydeployment.build.BuildWindows
    """
    build_windows._set_up_venv()
    package = build_windows.make_app()
    assert exists(package)


@mark.order(7)
@windows
def test_build_windows_make_arc_from_appdir(
        build_windows: BuildWindows,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_make_arc_from_appdir` method

    :param build_windows: Instance of BuildWindows
    :type build_windows: pydeployment.build.BuildWindows
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    d, _ = tmp_file(dir_="test", path="test")
    package = build_windows._make_arc_from_appdir(d)
    assert exists(package)


@mark.order(7)
@windows
def test_build_windows_make_arc(build_windows: BuildWindows) -> None:
    """
    Test `make_arc` method

    :param build_windows: Instance of BuildWindows
    :type build_windows: pydeployment.build.BuildWindows
    """
    build_windows._set_up_venv()
    package = build_windows.make_arc()
    assert exists(package)
