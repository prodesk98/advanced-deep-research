from typing import Literal, Optional
from loguru import logger as loguru_logger
from streamlit.delta_generator import DeltaGenerator


def logger(
    message: str | Exception,
    level: Literal['info', 'warning', 'error', 'debug', 'success'] = 'info',
    ui: Optional[DeltaGenerator] = None
) -> None:
    """
    Log a message with the specified logging level.

    Args:
        message (str): The message to log.
        level (str): The logging level. Can be 'info', 'warning', 'error', or 'debug'.
        ui (Optional[DeltaGenerator]): Optional Streamlit UI element for displaying the message.
        :param message:
        :param level:
        :param ui:
    """
    if level not in ['info', 'warning', 'error', 'debug', 'success']:
        raise ValueError("Invalid log level. Choose from 'info', 'warning', 'error', 'debug' or 'success'.")

    levels = {
        'info': lambda msg: loguru_logger.info(msg),
        'warning': lambda msg: loguru_logger.warning(msg),
        'error': lambda msg: loguru_logger.error(msg),
        'debug': lambda msg: loguru_logger.debug(msg),
        'success': lambda msg: loguru_logger.success(msg),
    }

    if isinstance(message, Exception):
        message = str(message)

    if isinstance(ui, DeltaGenerator):
        match level:
            case 'info':
                ui.info(":material/info: " + message)
            case 'warning':
                ui.warning(":material/warning: " + message)
            case 'error':
                ui.error(":material/error: " + message)
            case 'debug':
                ui.debug(":material/search: " + message)
            case 'success':
                ui.success(":material/check: " + message)

    levels[level](message)
