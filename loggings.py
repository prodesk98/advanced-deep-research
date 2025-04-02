from typing import Literal
from loguru import logger as loguru_logger


def logger(message: str | Exception, level: Literal['info', 'warning', 'error', 'debug'] = 'info') -> None:
    """
    Log a message with the specified logging level.

    Args:
        message (str): The message to log.
        level (str): The logging level. Can be 'info', 'warning', 'error', or 'debug'.
    """
    levels = {
        'info': lambda msg: loguru_logger.info(msg),
        'warning': lambda msg: loguru_logger.warning(msg),
        'error': lambda msg: loguru_logger.error(msg),
        'debug': lambda msg: loguru_logger.debug(msg),
    }

    if isinstance(message, Exception):
        message = str(message)

    levels[level](message)
