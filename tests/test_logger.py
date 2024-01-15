from logging import INFO, Logger, StreamHandler
from pytest import mark


@mark.order(2)
def test_logger(logger: Logger) -> None:
    """
    Test the build logger

    :param logger: Build logger
    :type logger: logging.Logger
    """
    name = logger.name
    hdlr = logger.handlers[0]
    fmt = hdlr.formatter._fmt
    assert logger.getEffectiveLevel() == INFO
    assert name == "PyDeployment"
    assert isinstance(hdlr, StreamHandler)
    assert fmt == "%(name)s: %(levelname)s: %(message)s"
