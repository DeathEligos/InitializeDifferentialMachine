# mypackage/utils.py
import logging
import logging.config

def setup_logger() -> None:
    """
    Configuration of project logging system.
    """

    logging_config = {
        "version": 1,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s\t%(asctime)s\t[%(name)s] %(message)s",
                "datefmt": "%H:%M:%S"
            },
            "simple": {
                "format": "%(levelname)s\t%(message)s"
            }
        },
        "handlers": {
            # Console log handler.
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple"
            },
            # File log handler.
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "idm.log",
                "formatter": "verbose",
                "mode": "w"
            }
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": True
            }
        }
    }

    # Apply the configuration.
    logging.config.dictConfig(logging_config)