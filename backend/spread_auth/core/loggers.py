import logging
from logging.handlers import RotatingFileHandler
import sys

from fastapi import Request

from .config import settings


class Colors:
    grey = "\x1b[0;37m"
    green = "\x1b[1;32m"
    yellow = "\x1b[1;33m"
    red = "\x1b[1;31m"
    purple = "\x1b[1;35m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    reset = "\x1b[0m"
    blink_red = "\x1b[5m\x1b[1;31m"


class CustomFormatter(logging.Formatter):

    format = '%(asctime)s - [%(name)s.%(funcName)s(%(lineno)d)] - %(levelname)s - %(message)s'

    # FORMATS = {
    #     logging.DEBUG: green + format + reset,
    #     logging.INFO: yellow + format + reset,
    #     logging.WARNING: red + format + reset,
    #     logging.ERROR: purple + format + reset,
    #     logging.CRITICAL: blink_red + format + reset
    # }

    def format(self, record):
        format_prefix = f"{Colors.purple}%(asctime)s{Colors.reset} " \
                        f"{Colors.blue}%(name)-35s{Colors.reset} " \
                        f"{Colors.light_blue}(%(filename)-15s:%(lineno)-4d){Colors.reset} "

        format_suffix = "%(levelname)s - %(message)s"

        formats = {
            logging.DEBUG: format_prefix + Colors.green + format_suffix + Colors.reset,
            logging.INFO: format_prefix + Colors.grey + format_suffix + Colors.reset,
            logging.WARNING: format_prefix + Colors.yellow + format_suffix + Colors.reset,
            logging.ERROR: format_prefix + Colors.red + format_suffix + Colors.reset,
            logging.CRITICAL: format_prefix + Colors.blink_red + format_suffix + Colors.reset
        }
        log_fmt = formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name):
    """
    Получить логгер для модуля
    :param name: Имя модуля
    :return: Экземпляр логгера
    """
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s [%(name)-35s.%(funcName)-15s:(%(lineno)2d)] %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # if logger.hasHandlers():
    #     return logger
    handler = RotatingFileHandler(filename=f'{settings.PROJECT_NAME}.log', maxBytes=10000000, backupCount=5)
    handler.setLevel(settings.LOG_LEVEL)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.LOG_LEVEL)
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)

    # logger.addFilter(CustomFilter())
    return logger


async def logging_middleware(request: Request, call_next):
    logger = get_logger(__name__)
    logger.info(f"Incoming request: {request.method} {request.url.path} {request.query_params}")
    response = await call_next(request)
    logger.info(f"Outgoing response code: {response.status_code}")
    return response


class LogOnce:
    def __init__(self, logger):
        self.logger = logger
        self.logged_messages = {}

    def debug(self, msg, unique_key=None, reset=False):
        """
        Логирует сообщение один раз, если только флаг reset не установлен в True.

        :param msg: Сообщение для логирования
        :param unique_key: Уникальный ключ для сообщения (по умолчанию сам текст сообщения)
        :param reset: Если True, сбрасывает состояние и позволяет повторное логирование
        """
        key = unique_key or msg
        if reset:
            self.logged_messages[key] = False

        # Проверка, было ли сообщение уже логировано
        if not self.logged_messages.get(key, False):
            self.logger.debug(msg)
            self.logged_messages[key] = True
