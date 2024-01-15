from collections.abc import Callable
from argparse import Namespace
from platform import system
from pytest import mark
from _pytest.monkeypatch import MonkeyPatch
from . import BuildConfig


@mark.order(-1)
def test_main(
        main: Callable[[], int],
        mock_build_config: BuildConfig,
        monkeypatch: MonkeyPatch,
        config: Namespace
    ) -> None:
    """
    Test `main` function

    :param main: Main function
    :type main: Callable[[], int]
    :param mock_build_config: BuildConfig class
    :type mock_build_config: pydeployment.build_config.BuildConfig
    :param monkeypatch: Monkeypatch fixture
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    :param config: Test configuration
    :type config: argparse.Namespace
    """
    with monkeypatch.context() as m:
        m.setattr(mock_build_config, "get_config", lambda _: config)
        m.delattr(config, "CERT", raising=False)
        assert main() == 0
