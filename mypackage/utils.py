# mypackage/utils.py
import logging
import logging.config
from typing import Tuple, Union

from mypackage.config import *

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


def scale_coords(coords: Union[Tuple[int, int, int, int],Tuple[int, int]]) -> Union[Tuple[int, int, int, int],Tuple[int, int]]:
    """
    Scale the coordinate data.

    Arguments:
        coords (Union[Tuple[int, int, int, int],Tuple[int, int]]): the original coordinate data to be scaled, support coordinate region and point.

    Return:
        Union[Tuple[int, int, int, int],Tuple[int, int]]: the scaled coordinate data, with the same format as arguments.
    """

    # Scale the coordinate region data.
    if len(coords) == 4:
        x1, y1, x2, y2 = coords
        width, height = x2 - x1, y2 - y1

        x1 = round(x1 * scale_x)
        y1 = round(y1 * scale_y)
        # Image data is scaled based on length and width.
        # Therefore coordinate data also needs to undergo the same calculation, but not scaling x2, y2.
        x2 = round(x1 + width * scale_x)
        y2 = round(y1 + height * scale_y)
        
        return (x1, y1, x2, y2)
    
    # Scale the coordinate point data.
    elif len(coords) == 2:
        x, y = coords
        return (round(x * scale_x), round(y * scale_y))
