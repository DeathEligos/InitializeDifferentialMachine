# main.py
"""
A script for the Differential Universe of Honkai: Star Rail.

Designed to roll for desired starting props (boon & equation).
"""

from win32gui import FindWindow, SetForegroundWindow
from time import sleep
from typing import Dict
import logging
import traceback

from mypackage.recognize import Recognizer
from mypackage.operate import Operator
from mypackage.config import *
from mypackage.exceptions import *
from mypackage.utils import setup_logger


def _set_targets(target: Dict[str, str]) -> None:
    """
    Set the target combination {boon, equation}.

    Read and save the name of target props inputed by user.

    Returns:
        dict (Dict[str, str]): {"interface ID": "target name"}.
    """
    
    for term in target:
        name = input(f"\tINPUT:\tEnter the name (Chinese pinyin) of your target for [{term}]: ")

        # Standardize the input.
        name = "".join([letter for letter in name.lower() if letter.isalpha()])  # Keep only letters and lowercase.
        name = HOMOPHONE.get(name, name)  # Correct possible spelling errors.
        target[term] = name


def main() -> None:
    """
    Entry of the program.

    Aactivate the window, monitor the screen, and repeat the following process:
    Take the screenshot -> Match the interface -> Perform the operation
    """

    try:
        # Configure logging and get the root logger.
        setup_logger()
        root_logger = logging.getLogger(__name__)

        # Check if game is open.
        is_open = FindWindow(None, GAME_WINDOW)
        if not is_open:
            raise WindowNotFoundError(GAME_WINDOW)
        
        # Set the target.
        target = {"select_golden_bloods_boon": "", "select_equation": ""}
        _set_targets(target)
        root_logger.debug(f"Set the target combination: [{target}];\n")

        # Active the game window.
        SetForegroundWindow(is_open)
        sleep(ACTIVE_WINDOWS_TIME)

        # Create an interface recognizer.
        interface_matcher = Recognizer(
            templates_dir = INTERFACE_TEMPL_DIR,
            id_to_file_name = {id: id for id in INTERFACE_REGIONS.keys()},
            confidence_threshold = INTERFACE_MATCH_THRESHOLD,
            id_to_coordinate = INTERFACE_REGIONS
        )
        # Create a operator.
        my_operator = Operator(
            id_to_coordinate = OPTION_REGIONS,
            targets = target
        )

        # Ready to run.
        root_logger.info("Begins monitoring, press Ctrl+C to interrupt;\n\n")
        counter = 0                     # Record the times of attempts.
        _current_interface_id = None    # Record the current interface.
        # Continuous monitoring.
        while counter <= MAX_ATTEMPT_COUNT:
            # Match and update current interface.
            _current_interface_id = interface_matcher.match()
            if _current_interface_id == "unmatched":
                root_logger.info("Undefined interface;")
            else:
                # Each time entering the start game interface, the counter plus one.
                if _current_interface_id == "start_game":
                    counter += 1
                    root_logger.info(f"Begin to attempt the order number: {counter};" + "\n" + "-" * 100)
                root_logger.info(f"Current interface id: [{_current_interface_id}];")
                
            # Operate according to the current interface.
            my_operator.operate(_current_interface_id)
            sleep(MONITOR_INTERVAL_TIME)

        raise MaxAttemptCountExceededError(MAX_ATTEMPT_COUNT)

            
    # Catch exceptions.
    except TargetAchievedError as e:
        root_logger.info(e.message)
        # 执行资源清理（如关闭文件、释放连接等）######################################
        # clean_up_resources()
        return 0
    except WindowNotFoundError as e:
        root_logger.error(e.message)
        return 66
    except TemplateNotFoundError as e:
        root_logger.error(e.message)
        return 67
    except MaxAttemptCountExceededError as e:
        root_logger.error(e.message)
        return 75

    except KeyboardInterrupt:
        root_logger.warning("Interrupt process!")
    except Exception as e:
        root_logger.error(f"Undefined error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()