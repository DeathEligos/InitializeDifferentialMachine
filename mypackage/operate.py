# mypackage\operate.py
"""
Defines Operator class.
"""

import win32api, win32con
import logging
from typing import Dict, Tuple, Union
from time import sleep

from mypackage.recognize import Recognizer
from mypackage.config import *
from mypackage.exceptions import TargetAchievedError


class Operator:
    """
    Operator, encapsulate the logic of operation execution.
    
    Responds according to the current interface ID.

    Arguments:
        id_to_coordinate (Dict[str, Tuple[int, int, int, int]]): mapping from option ID to coordinate;
        targets (Dict[str, str]): mapping from interface ID to target name (template file name).

    Attributes:
        _current_selection (Tuple[bool]): Record the choices made;
        _logger (logging.Logger): log;
        _option_recognizer (Recognizer): Match the options with the templates.
    """
    
    # Initialize Operator.
    def __init__(
        self,
        id_to_coordinate: Dict[str, Tuple[int, int, int, int]],
        targets: Dict[str, str],
    ) -> None:
        
        # Configuration parameters.
        self.id_to_coordinate = id_to_coordinate
        self.interface_id_to_file_name = targets

        # State variables.
        self._current_selection: Tuple[bool] = [False, False]   # Record the choices made

        # Logger.
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Recognizer.
        self._option_recognizer = Recognizer(
            templates_dir = OPTION_TEMPL_DIR,
            id_to_file_name = {id: self.interface_id_to_file_name[id[:-2]] for id in self.id_to_coordinate.keys()},
            confidence_threshold = OPTION_MATCH_THRESHOLD,
            id_to_coordinate = self.id_to_coordinate
        )
    

    # Click on the designated location.
    def _mouse_click(self, coordinate: Union[Tuple[int, int], Tuple[int, int, int, int]]) -> Tuple[int, int]:
        if len(coordinate) == 4:
            x = (coordinate[0] + coordinate[2]) // 2
            y = (coordinate[1] + coordinate[3]) // 2
        elif len(coordinate) == 2:
            x = coordinate[0]
            y = coordinate[1]
        # Mouse move -> press -> hold -> release.
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        sleep(HOLD_TIME)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0, 0, 0, 0)
        return (x, y)


    # Press the designated key.
    def _keyboard_press(self, key_ascii: int) -> int:
        # Keyboard press -> hold -> release
        win32api.keybd_event(key_ascii, 0, 0, 0)
        sleep(HOLD_TIME)
        win32api.keybd_event(key_ascii, 0, win32con.KEYEVENTF_KEYUP, 0)
        return key_ascii


    def _update_selection(self, interfece_id: str) -> None:
        """
        Update the record of target completion status.

        Arguments:
            interfece_id (str): used to determine which target is completed, or whether necessary to reset
        """

        match interfece_id:
            case "in_game":
                self._current_selection = [False, False]
                self._logger.info("Fail to achieve the target, reset the record of target completion status;\n")

            case "select_golden_bloods_boon":
                self._current_selection[0] = True
                self._logger.info("Success to select the target golden blood's boon;\n")

            case "select_equation":
                self._current_selection[1] = True
                self._logger.info("Success to select the target equation;\n")

        if  all(completed for completed in self._current_selection):
            raise TargetAchievedError(self.interface_id_to_file_name)


    def _select(self, interface_id: str, is_rolled: bool = False) -> None:
        """
        Match the options with the templates and take decision.

        This method is called in selection interface.

        Arguments:
            interface_id (str): which selection interfece is currently in;
            is_rolled (bool): whether the boons selection interface is rolled.
        """
    
        # Selections interface which need to judge.
        if interface_id == "select_golden_bloods_boon" or interface_id == "select_equation":

            # Play the animation of entering the boons selection interface.
            if interface_id == "select_golden_bloods_boon" and is_rolled == False:
                sleep(BOONS_ANIMATION_TIME)

            # Match the characteristic regions of options.
            my_option = self._option_recognizer.match()
            # Match successfully. Select and confirm, and update the target progress.
            if my_option != "unmatched":
                self._logger.info(f"Select the target option [{my_option}] and config;\n")
                self._mouse_click(self.id_to_coordinate[my_option])
                sleep(SELECT_TO_CONFIRM_TIME)
                self._mouse_click(CONFIRM[interface_id])
                self._update_selection(interface_id)
                return my_option

            # Match failed. If the unrolled bonns interface is currently in, roll it and call itself with is_rolled = True
            elif interface_id == "select_golden_bloods_boon" and is_rolled == False:
                self._logger.info("Roll the golden blood's boon;")
                self._mouse_click(ROLL)
                self._logger.info(f"Wait {ROOL_ANIMATION_TIME}s for the rolling animation playing;")
                sleep(ROOL_ANIMATION_TIME)
                return self._select(interface_id, is_rolled = True)

        # Select the default option and confirm.
        self._logger.info("Select the default option and confirm;\n")
        self._mouse_click(DEFAULT)
        sleep(SELECT_TO_CONFIRM_TIME)
        self._mouse_click(CONFIRM[interface_id])
        return "opt_default"

    def operate(self, interface_id: str) -> None:
        """
        Perform operation according to the current interface ID.

        Arguments:
            interface_id (str): current interface ID.
        """

        match interface_id:
            case "undefined":
                self._logger.info("No operate;\n")

            case "start_game" | "select_conv" | "conv_calculus" | "run_calculus" | "restart_game" | "hint" | "exit":
                # Fixed process, click on the screen center directly.
                self._logger.info(f"Click on the position: {self._mouse_click(INTERFACE_REGIONS[interface_id])};\n")

            case "select_golden_bloods_boon" | "select_equation" | "select_oddity" | "select_blessing" | "select_weighted_curio":
                # Selection interface.
                self._logger.info("Selecting...")
                self._select(interface_id)

            case "confirm_equation" | "confirm_blessing":
                # Confirm the acquisition interface, press ESC.
                self._logger.info(f"Press the keyboard: {self._keyboard_press(27)}(ASCII);\n")

            case "in_game":
                # Entered the game without achieving the target, execute the restart process.
                self._update_selection(id)
                self._logger.info(f"Press the keyboard: {self._keyboard_press(27)}(ASCII);\n")

            case _:
                self._logger.warning("Abnormal interface id;\n")
        return False