import logging
import colorlog

def init_logger(dunder_name, testing_mode) -> logging.Logger:
    log_format = (
        '[%(asctime)s]'
        '[%(name)s]'
        '[%(threadName)s]'
        '[%(funcName)s]'
        '[%(levelname)s] - '
        '%(message)s'
    )
    bold_seq = '\033[1m'
    colorlog_format = (
        '%(log_color)s '
        f'{log_format}'
    )
    logging.basicConfig(level=logging.DEBUG)
    colorlog.basicConfig(format=colorlog_format)
    logger = logging.getLogger(dunder_name)
    return logger