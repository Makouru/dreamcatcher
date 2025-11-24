import logging
import sys

LEVEL = logging.DEBUG # DEBUG, INFO, WARNING, ERROR

log = logging.getLogger("dreamcatcher")
log.setLevel(LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LEVEL)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

log.addHandler(handler)