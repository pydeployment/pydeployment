from logging import Formatter, getLogger, StreamHandler
from sys import stdout

logger = getLogger("PyDeployment")
logger.setLevel("INFO")
_hdlr = StreamHandler(stdout)
_hdlr.setFormatter(Formatter("%(name)s: %(levelname)s: %(message)s"))
logger.addHandler(_hdlr)
