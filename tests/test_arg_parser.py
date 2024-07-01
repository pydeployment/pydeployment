from argparse import Namespace as N
from pytest import mark, raises
from _pytest.capture import CaptureFixture
from . import ArgParser


@mark.order(1)
@mark.parametrize(
    "input,attr,result",
    (
        ("-h", None, "usage: pydeploy"),
        ("--help", None, "usage: pydeploy"),
        ("-v", None, "PyDeployment"),
        ("--version", None, "PyDeployment"),
        ("--log DEBUG", "LOG", N(**{"LOG": "DEBUG"})),
        ("--log INFO", "LOG", N(**{"LOG": "INFO"})),
        ("--log WARNING", "LOG", N(**{"LOG": "WARNING"})),
        ("--log ERROR", "LOG", N(**{"LOG": "ERROR"})),
        ("--log BADINPUT", None, "invalid choice"),
        ("-y", "NO_CONFIRM", N(**{"NO_CONFIRM": True})),
        ("--no-confirm", "NO_CONFIRM", N(**{"NO_CONFIRM": True})),
        ("--no-clean", "NO_CLEAN", N(**{"NO_CLEAN": True})),
        ("--archive", "ARCHIVE", N(**{"ARCHIVE": True})),
        ("-f 0", "FILENAME", N(**{"FILENAME": "0"})),
        ("--filename 0", "FILENAME", N(**{"FILENAME": "0"})),
        ("-a 0", "APPNAME", N(**{"APPNAME": "0"})),
        ("--appname 0", "APPNAME", N(**{"APPNAME": "0"})),
        ("--id 0", "ID", N(**{"ID": "0"})),
        ("--appv 0", "VERSION", N(**{"VERSION": "0"})),
        ("--app-version 0", "VERSION", N(**{"VERSION": "0"})),
        ("--author 0", "AUTHOR", N(**{"AUTHOR": "0"})),
        ("--publisher 0", "PUBLISHER", N(**{"PUBLISHER": "0"})),
        ("-d 0", "DESCRIPTION", N(**{"DESCRIPTION": "0"})),
        ("--description 0", "DESCRIPTION", N(**{"DESCRIPTION": "0"})),
        ("--pyi-version 0", "PYI_VERSION", N(**{"PYI_VERSION": "0"})),
        ("-i 0", "ICON", N(**{"ICON": "0"})),
        ("--icon 0", "ICON", N(**{"ICON": "0"})),
        ("-l 0", "LICENSE", N(**{"LICENSE": "0"})),
        ("--license 0", "LICENSE", N(**{"LICENSE": "0"})),
        ("-o 0", "OUTDIR", N(**{"OUTDIR": "0"})),
        ("--outdir 0", "OUTDIR", N(**{"OUTDIR": "0"})),
        ("-r 0", "REQUIREMENTS", N(**{"REQUIREMENTS": "0"})),
        ("--requirements 0", "REQUIREMENTS", N(**{"REQUIREMENTS": "0"})),
        ("--venv 0", "VENV", N(**{"VENV": "0"})),
        ("0", "TARGET", N(**{"TARGET": ["0"]})),
        ("--appdata 0", "APPDATA", N(**{"APPDATA": "0"})),
        ("--appimagetool 0", "APPIMAGETOOL", N(**{"APPIMAGETOOL": "0"})),
        ("--runtime-file 0", "RUNTIME_FILE", N(**{"RUNTIME_FILE": "0"})),
        ("-E 0", "ENTI", N(**{"ENTI": "0"})),
        ("--enti 0", "ENTI", N(**{"ENTI": "0"})),
        ("--entitlements 0", "ENTI", N(**{"ENTI": "0"})),
        ("-C 0", "CERT", N(**{"CERT": "0"})),
        ("--cert 0", "CERT", N(**{"CERT": "0"})),
        ("--certificate 0", "CERT", N(**{"CERT": "0"})),
        ("-K 0", "KEYC", N(**{"KEYC": "0"})),
        ("--keyc 0", "KEYC", N(**{"KEYC": "0"})),
        ("--keychain-profile 0", "KEYC", N(**{"KEYC": "0"})),
        ("-A 0", "APID", N(**{"APID": "0"})),
        ("--apid 0", "APID", N(**{"APID": "0"})),
        ("--apple-id 0", "APID", N(**{"APID": "0"})),
        ("-T 0", "TMID", N(**{"TMID": "0"})),
        ("--tmid 0", "TMID", N(**{"TMID": "0"})),
        ("--team-id 0", "TMID", N(**{"TMID": "0"})),
        ("-P 0", "PASS", N(**{"PASS": "0"})),
        ("--pass 0", "PASS", N(**{"PASS": "0"})),
        ("--password 0", "PASS", N(**{"PASS": "0"})),
        ("--nsis 0", "NSIS", N(**{"NSIS": "0"})),
        ("--makensis 0", "MAKENSIS", N(**{"MAKENSIS": "0"}))
    )
)
def test_arg_parser(
        arg_parser: ArgParser,
        capsys: CaptureFixture,
        input: str,
        attr: str,
        result: str | N
    ) -> None:
    """
    Test ArgParser class

    :param arg_parser: Instance of ArgParser with all possible options
    :type arg_parser: pydeployment.arg_parser.ArgParser
    :param capsys: System capture fixture
    :type capsys: _pytest.capture.CaptureFixture
    :param input: Input for argument parser
    :type input: str
    :param attr: Attribute name
    :type attr: str
    :param result: Expected output string or namespace
    :type result: str | argparse.Namespace
    """
    try:
        config = arg_parser.parse_args(input.split())
    except SystemExit:
        pass
    if attr:
        assert getattr(config, attr) == getattr(result, attr)
    else:
        output = capsys.readouterr()
        assert result in output.out or result in output.err
