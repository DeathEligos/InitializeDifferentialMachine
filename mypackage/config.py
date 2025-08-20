# mypackage/config.py
"""
Configuration file.

Defines the configuration of the program:
* name of window;
* scaling factor of screen;
* times of attempt;
* path of templates;
* threshold of match;
* constants of time;
* coordinates of characteristic regions;
* positions of buttons;
* whitelist of input.
"""

from typing import Dict, Tuple
from pyautogui import size


# -------------------- WINDOW CONFIGURATION --------------------
GAME_WINDOW: str = "崩坏：星穹铁道"


# -------------------- SCREEN CONFIGURATION --------------------
resolution_width, resolution_height = size()                            # Current monitor resolution.
scale_x, scale_y = resolution_width / 1920, resolution_height / 1080    # Coordinates scaling factor.


# -------------------- LOOP CONFIGURATION --------------------
MAX_ATTEMPT_COUNT = 50


# -------------------- PATH CONFIGURATION --------------------
INTERFACE_TEMPL_DIR: str = "interface_templates"
OPTION_TEMPL_DIR: str = "option_templates"


# -------------------- MATCH THRESHOLD CONFIGURATION --------------------
INTERFACE_MATCH_THRESHOLD: float = 0.9
OPTION_MATCH_THRESHOLD: float = 0.7


# -------------------- TIME CONFIGURATION --------------------
MONITOR_INTERVAL_TIME: float = 2        # Time interval for screen monitoring;
ACTIVE_WINDOWS_TIME: float = 0.5        # Time of waiting for game window actived;
HOLD_TIME: float = 0.05                 # Mouse and keyboard hold time;
BOONS_ANIMATION_TIME: float = 2         # Animation duration of entering the boon-selection interface;
SELECT_TO_CONFIRM_TIME: float = 0.5     # Time to wait after selecting before confirming;
ROOL_ANIMATION_TIME: float = 3          # Animation duration of rolling the boon-selection interface.


# -------------------- MATCH CHARACTERISTIC REGIONS --------------------
INTERFACE_REGIONS: Dict[str, Tuple[int, int, int, int]] = {
    "start_game": (1520, 930, 1650, 980),
    "select_conv": (520, 300, 700, 350),
    "conv_calculus": (1600, 950, 1770, 990),
    "run_calculus": (930, 960, 1037, 1010),
    "select_golden_bloods_boon": (70, 50, 240, 100),
    "select_equation": (30, 30, 220, 100),
    "select_oddity": (30, 30, 220, 100),
    "select_blessing": (30, 30, 220, 100),
    "select_weighted_curio": (30, 30, 220, 100),
    "confirm_equation": (870, 980, 1060, 1040),
    "confirm_blessing": (870, 980, 1060, 1040),
    "in_game": (170, 50, 370, 110),
    "restart_game": (1310, 960, 1480, 1000),
    "hint": (1150, 650, 1220, 690),
    "exit": (900, 960, 1040, 1000),
}
OPTION_REGIONS: Dict[str, Tuple[int, int, int, int]] = {  
    "select_golden_bloods_boon_1": (289, 810, 647, 836),
    "select_golden_bloods_boon_2": (781, 767, 1139, 793),
    "select_golden_bloods_boon_3": (1273, 810, 1631, 836),
    "select_equation_1": (291, 490, 688, 530),
    "select_equation_2": (761, 490, 1158, 530),
    "select_equation_3": (1232, 490, 1629, 530),
}


# -------------------- OPERATE COORDINATES --------------------
DEFAULT: Tuple[int, int] = (960, 540)           # Default click coordinate (screen center) for selection interfaces;
ROLL: Tuple[int, int] = (712, 966)              # Roll button coordinate for golden blod's boons selection interface;
CONFIRM: Dict[str, Tuple[int, int]] = {         # Confirm selection button coordinate for selection interfaces;
    "select_golden_bloods_boon": (1026, 965),
    "select_equation": (1709, 973),
    "select_oddity": (1709, 973),
    "select_blessing": (1691, 959),
    "select_weighted_curio": (1709, 973),
}


# -------------------- WHITELIST CONFIGURATION --------------------
HOMOPHONE: Dict[str, str] = {
    "xunyouletuan": "xunyouyuetuan",
    "liemianjinzhao": "liemianjinzhua",
    "yiguwuyangyuan": "yigufuyangyuan",
}
