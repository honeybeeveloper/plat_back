import logging
from logging.handlers import TimedRotatingFileHandler

from ozz_backend.common.util import create_dir


def get_logger(logger_name, config):
    """
    Initialise a logger
    :param logger_name: logger name
    :param config: logging config
    :return: logger
    """
    logger = logging.getLogger(f'{logger_name}-logger')
    logging_format = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')
    logger.setLevel(config.logging.level)

    create_dir(config.logging.path)

    # leaver log in a file
    file_log = TimedRotatingFileHandler(filename=f'{config.logging.path}/{logger_name}.log',
                                        when='midnight',
                                        interval=1,
                                        encoding='utf-8')
    file_log.suffix = '%Y%m%d'
    file_log.setFormatter(logging_format)
    logger.addHandler(file_log)

    # display log on the console
    console_log = logging.StreamHandler()
    console_log.setFormatter(logging_format)
    logger.addHandler(console_log)

    return logger
