import colorlog
import inspect  # TODO: when performance hits, replace with sys
import os

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "[%(asctime)s.%(msecs)03d][TID: %(threadName)-10s : "
        "%(log_color)s%(levelname)-8s]%(reset)s %(log_color)s%(message)s",
        # datefmt="%Y-%m-%d %H:%M:%S",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
)

logger = colorlog.getLogger(
    "logger"
)  # setup one global logger and filter by TID
logger.addHandler(handler)


def logDebug(message):
    func = inspect.currentframe().f_back.f_code

    logger.debug(
        "[%s::%s] %s"
        % (os.path.basename(func.co_filename), func.co_name, message)
    )


def logInfo(message):
    func = inspect.currentframe().f_back.f_code

    logger.info(
        "[%s::%s] %s"
        % (os.path.basename(func.co_filename), func.co_name, message)
    )  # file name is good enough


def logWarning(message):
    func = inspect.currentframe().f_back.f_code

    logger.warning(
        "[%s::%s] %s"
        % (os.path.basename(func.co_filename), func.co_name, message)
    )


def logError(message):
    func = inspect.currentframe().f_back.f_code

    logger.error(
        "[%s::%s] %s"
        % (os.path.basename(func.co_filename), func.co_name, message)
    )


def logCritical(message):
    func = inspect.currentframe().f_back.f_code

    logger.critical(
        "[%s::%s] %s"
        % (os.path.basename(func.co_filename), func.co_name, message)
    )
