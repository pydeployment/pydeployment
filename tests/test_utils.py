from collections.abc import Callable
from contextlib import nullcontext as does_not_raise
from platform import python_compiler
from typing import Iterator
from pytest import mark, raises
from _pytest.python_api import RaisesContext


@mark.order(0)
@mark.parametrize(
    "command,output,exception",
    (
        ("echo test", "test\n", does_not_raise()),
        ("", "", raises(Exception))
    )
)
def test_run_command(
        run_cmd: Callable[[str], Iterator[str]],
        command: str,
        output: str,
        exception: does_not_raise | RaisesContext
    ) -> None:
    """
    Test `run_command` function

    :param run_cmd: Run command function
    :type run_cmd: Callable[[str], Iterator[str]]
    :param command: Command
    :type command: str
    :param output: Expected output
    :type output: str
    :param exception: Expected exception context
    :type exception: contextlib.nullcontext | _pytest.python_api.RaisesContext
    """
    if command and python_compiler()[:3] == "MSC":
        command = f"cmd /c {command}"
    out = ""
    with exception:
        for line in run_cmd(command):
            out += line
    assert out == output
