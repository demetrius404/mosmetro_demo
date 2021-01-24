import logging
from logging import Logger

from .typing_alias import Str


def create_logger(name: Str) -> Logger:
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log
