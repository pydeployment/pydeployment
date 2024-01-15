from collections.abc import Callable
from glob import glob
from os import mkdir
from os.path import exists, join
from platform import system
from shutil import move
from typing import Optional, Tuple
from pytest import mark
from _pytest.monkeypatch import MonkeyPatch
from . import BuildConfig, BuildMacos

macos = mark.skipif(system() != "Darwin", reason="System does not match.")


@mark.order(6)
@macos
def test_build_macos(build_macos: BuildMacos) -> None:
    """
    Test BuildMacos constructor

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    """
    assert exists(build_macos.config.ICON)
    assert exists(build_macos.config.ENTI)


@mark.order(6)
@macos
@mark.skipif(not exists(".env"), reason="Notarization info not found.")
def test_build_macos_notarize_app(
        build_macos: BuildMacos,
        build_config: BuildConfig,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_notarize_app` method

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    _, p = tmp_file(path="tmp.py")
    build_macos._set_up_venv()
    build_macos.validate_pyi_arg(
        ["--codesign-identity"], f"'{build_macos.config.CERT}'"
    )
    build_macos.validate_pyi_arg(
        ["--osx-entitlements-file"], f"'{build_macos.config.ENTI}'"
    )
    build_macos.run_pyinstaller(p)
    d = glob(join("dist", "*.app"))[0]
    assert build_macos._notarize_app(d) == 0


@mark.order(6)
@macos
def test_build_macos_build_dmg(
        build_macos: BuildMacos,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_build_dmg` method

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    # Create build directory for this test
    mkdir("build")
    d, _ = tmp_file(dir_="test", path="test")
    dmg = build_macos._build_dmg(d)
    assert exists(dmg)


@mark.order(6)
@macos
def test_build_macos_make_app_from_appdir(
        build_macos: BuildMacos,
        monkeypatch: MonkeyPatch,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_make_app_from_appdir` method

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    :param monkeypatch: Monkeypatch fixture
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    with monkeypatch.context() as m:
        # Delete `CERT` attribute to skip notarization step
        m.delattr(build_macos.config, "CERT", raising=False)
        # Create build directory for this test
        mkdir("build")
        d, _ = tmp_file(dir_="test", path="test")
        package = build_macos._make_app_from_appdir(d)
        assert exists(package)


@mark.order(6)
@macos
def test_build_macos_sub(
        build_macos: BuildMacos,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_sub` method

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    _, p = tmp_file(path="test.txt")
    def contents(p: str) -> str:
        """
        Given a filename, return the contents of the file as a string

        :param p: Filename
        :type p: str
        :return: Contents
        :rtype: str
        """
        with open(p, "r") as f:
            c = f.read()
            f.close()
        return c
    before = contents(p)
    build_macos._sub("[(]", "'test'", p)
    after = contents(p)
    assert before != after


@mark.order(6)
@macos
def test_build_macos_make_app(build_macos: BuildMacos) -> None:
    """
    Test `make_app` method

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    """
    build_macos._set_up_venv()
    package = build_macos.make_app()
    assert exists(package)


@mark.order(6)
@macos
def test_build_macos_make_arc_from_appdir(
        build_macos: BuildMacos,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    ) -> None:
    """
    Test `_make_arc_from_appdir` method

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    """
    d, _ = tmp_file(dir_="test", path="test")
    package = build_macos._make_arc_from_appdir(d)
    assert exists(package)


@mark.order(6)
@macos
def test_build_macos_make_arc(build_macos: BuildMacos) -> None:
    """
    Test `make_arc` method

    :param build_macos: Instance of BuildMacos
    :type build_macos: pydeployment.build.BuildMacos
    """
    build_macos._set_up_venv()
    package = build_macos.make_arc()
    assert exists(package)
