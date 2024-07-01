from collections.abc import Callable
from os.path import exists, join
from platform import system
from shutil import move
from typing import Optional, Tuple
from pytest import mark
from . import BuildLinux

linux = mark.skipif(system() != "Linux", reason="System does not match.")


@mark.order(5)
@linux
def test_build_linux(build_linux: BuildLinux) -> None:
    """
    Test BuildLinux constructor

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    """
    assert exists(build_linux.config.ICON)
    assert exists(build_linux.config.APPIMAGETOOL)


@mark.order(5)
@linux
def test_build_linux_get_appimagetool(build_linux: BuildLinux) -> None:
    """
    Test `_get_appimagetool` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    """
    assert exists(build_linux._get_appimagetool())


@mark.order(5)
@linux
def test_build_linux_get_appimage_runtime(build_linux: BuildLinux) -> None:
    """
    Test `_get_appimage_runtime` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    """
    assert exists(build_linux._get_appimage_runtime())


@mark.order(5)
@linux
def test_build_linux_make_desktop_file(
        build_linux: BuildLinux,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_make_desktop_file` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    d, p = tmp_file(path="tmp")
    build_linux._make_desktop_file(d, p)
    path = join(d, "usr", "share", "applications")
    assert exists(join(path, f"{build_linux.config.ID}.desktop"))
    assert exists(join(d, f"{build_linux.config.ID}.desktop"))


@mark.order(5)
@linux
def test_build_linux_add_appdata(
        build_linux: BuildLinux,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_add_appdata` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    appdata = f"{build_linux.config.ID}.appdata.xml"
    d, p = tmp_file(path=appdata)
    build_linux.config.APPDATA = p
    build_linux._add_appdata(d)
    path = join(d, "usr", "share", "metainfo")
    assert exists(join(path, appdata))


@mark.order(5)
@linux
def test_build_linux_make_app_from_appdir(
        build_linux: BuildLinux,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_make_app_from_appdir` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    d, _ = tmp_file(dir_="test", path="test")
    package = build_linux._make_app_from_appdir(d)
    assert exists(package)


@mark.order(5)
@linux
def test_build_linux_make_app(build_linux: BuildLinux) -> None:
    """
    Test `make_app` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    """
    build_linux._set_up_venv()
    package = build_linux.make_app()
    assert exists(package)


@mark.order(5)
@linux
def test_build_linux_make_arc_from_appdir(
        build_linux: BuildLinux,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_make_arc_from_appdir` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    d, _ = tmp_file(dir_="test", path="test")
    package = build_linux._make_arc_from_appdir(d)
    assert exists(package)


@mark.order(5)
@linux
def test_build_linux_make_arc(build_linux: BuildLinux) -> None:
    """
    Test `make_arc` method

    :param build_linux: Instance of BuildLinux
    :type build_linux: pydeployment.build.BuildLinux
    """
    build_linux._set_up_venv()
    package = build_linux.make_arc()
    assert exists(package)
