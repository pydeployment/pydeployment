from collections.abc import Callable
from os import environ
from typing import Any, Dict, List, Optional, Tuple
from pytest import fixture, mark
from _pytest.monkeypatch import MonkeyPatch
from . import BuildConfig


@mark.order(3)
def test_build_config(build_config: BuildConfig) -> None:
    """
    Test BuildConfig constructor

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    """
    assert build_config.system in ("Linux", "Darwin", "Windows")


@mark.order(3)
@mark.parametrize(
    "key,dict_,result",
    (
        ("key", {"key": True}, True),
        ("key", {"key": None}, False),
        ("key", {}, False)
    )
)
def test_build_config_is_set(
        build_config: BuildConfig,
        key: str,
        dict_: Dict[str, Any],
        result: bool
    ) -> None:
    """
    Test `_is_set` method

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    :param key: Key
    :type key: str
    :param dict_: Dictionary
    :type dict_: Dict[str, Any]
    :param result: Expected result
    :type result: bool
    """
    assert build_config._is_set(key, dict_) is result


@mark.order(3)
def test_build_config_get_config_from_env(build_config: BuildConfig) -> None:
    """
    Test `_get_config_from_env` method

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    """
    config = build_config._get_config_from_env()
    if "ENV_FILE" in environ.keys():
        assert config != {}
    else:
        assert config == {}


@mark.order(3)
def test_build_config_get_config_from_argv(build_config: BuildConfig) -> None:
    """
    Test `_get_config_from_argv` method

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    """
    config = build_config._get_config_from_argv()
    config = {k: v for k, v in config.items() if v and k != "TARGET"}
    assert config == {"LOG": "INFO"}


@mark.order(3)
@mark.parametrize(
    "target,code",
    (
        ("tmp.py", 0),
        (None, 1)
    )
)
def test_build_config_validate_target(
        build_config: BuildConfig,
        tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]],
        target: str,
        code: str
    ) -> None:
    """
    Test `_validate_target` method

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    :param tmp_file: Temporary file function
    :type tmp_file: Callable[[str, Optional[str]], Tuple[str, Optional[str]]]
    :param target: Target filename
    :type target: str
    :param code: Return code
    :type code: int
    """
    if target:
        _, p = tmp_file(path=target)
        config = {"TARGET": [p]}
    else:
        config = {}
    assert build_config._validate_target(config) == code


@mark.order(3)
@mark.parametrize(
    "target,output",
    (
        (["a", "b", "c"], ("a", "b c ")),
        (["a"], ("a", ""))
    )
)
def test_build_config_handle_target(
        build_config: BuildConfig,
        target: List[str],
        output: Tuple[str, str]
    ) -> None:
    """
    Test `_handle_target` method

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    :param target: List of targets
    :type target: List[str]
    :param output: Expected output
    :type output: Tuple[str, str]
    """
    input_cfg = {"TARGET": target, "PYI_ARGS": ""}
    output_cfg = {"TARGET": output[0], "PYI_ARGS": output[1]}
    assert build_config._handle_target(input_cfg) == 0


@mark.order(3)
@mark.parametrize(
    "target,mode",
    (
        ("test.spec", "SPEC"),
        ("test.py", "PY")
    )
)
def test_build_config_handle_defaults(
        build_config: BuildConfig,
        target: str,
        mode: str
    ) -> None:
    """
    Test `_handle_defaults` method

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    :param target: Target filename
    :type target: str
    :param mode: Build mode
    :type mode: str
    """
    input = {"TARGET": target, "AUTHOR": target}
    output = {
        **input, "MODE": mode, "FILENAME": "test", "ID": "id.not.found.test",
        "OUTDIR": "dist", "APPNAME": "test", "PUBLISHER": target
    }
    assert build_config._handle_defaults(input) == 0


@mark.order(3)
@mark.parametrize(
    "attr,val,syst",
    (
        ("LOG", "INFO", None),
        ("NO_CONFIRM", False, None),
        ("NO_CLEAN", False, None),
        ("ARCHIVE", False, None),
        ("FILENAME", "", None),
        ("APPNAME", "", None),
        ("ID", "id.not.found.", None),
        ("VERSION", None, None),
        ("AUTHOR", None, None),
        ("PUBLISHER", None, None),
        ("DESCRIPTION", None, None),
        ("PYI_VERSION", None, None),
        ("ICON", None, None),
        ("LICENSE", None, None),
        ("OUTDIR", "dist", None),
        ("REQUIREMENTS", None, None),
        ("VENV", None, None),
        ("APPDATA", None, "Linux"),
        ("APPIMAGETOOL", None, "Linux"),
        ("ENTI", None, "Darwin"),
        ("CERT", None, "Darwin"),
        ("KEYC", None, "Darwin"),
        ("APID", None, "Darwin"),
        ("TMID", None, "Darwin"),
        ("PASS", None, "Darwin"),
        ("NSIS", None, "Windows"),
        ("MAKENSIS", None, "Windows"),
        ("PYI_ARGS", "", None),
        ("MODE", "PY", None)
    )
)
def test_build_config_get_config(
        build_config: BuildConfig,
        monkeypatch: MonkeyPatch,
        attr: str,
        val: str | bool,
        syst: str
    ) -> None:
    """
    Test `get_config` method

    :param build_config: Instance of BuildConfig for the system OS
    :type build_config: pydeployment.build_config.BuildConfig
    :param monkeypatch: Monkeypatch fixture
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    :param attr: Attribute
    :type attr: str
    :param val: Attribute value
    :type val: str | bool
    :param syst: System OS
    :type syst: str
    """
    with monkeypatch.context() as m:
        m.delitem(environ, "ENV_FILE", raising=False)
        ns = build_config.get_config(skip_validation=True)
        if not syst or build_config.system == syst:
            assert getattr(ns, attr) == val or val in getattr(ns, attr)
