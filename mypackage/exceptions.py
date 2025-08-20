# mypackage/exceptions.py
"""
Custom exception classes:
* target achieved error;
* window not found error.
"""

from typing import Dict


class TargetAchievedError(Exception):
    """
    Exception raised when the process needs to be interrupted upon achievement of the target
    
    This is not an error-related exception. After being thrown, it usually indicates that the process can terminate normally.
    
    Arguments:
        target (Dict[str, str]): the target that is achieved.
    """
    def __init__(self, target: Dict[str, str]):
        self.message = f"Target {target} achieved, program will exit."
        super().__init__(self.message)


class WindowNotFoundError(Exception):
    """
    Exception raised when the window with no matching title exists.

    Arguments:
        window (str): the name of the window unmatched.
    """
    def __init__(self, window: str):
        self.message = f"Window [{window}] not found, program will exit."
        super().__init__(self.message)


class TemplateNotFoundError(Exception):
    """
    Exception raised when the template file cannot be opened.

    Arguments:
        file_name (str): the name of the template file.
    """
    def __init__(self, path: str):
        self.message = f"Template file '{path}' not found, program will exit."
        super().__init__(self.message)


class MaxAttemptCountExceededError(Exception):
    """
    Exception raised when the loop reaches the maximum number of iterations but the target has not been achieved.
    
    Used to indicate that the program fails to complete the target within the preset maximum number of loops, and it belongs to an execution overrun error.

    Attributes:
        max_count (int): maximum times of attempting.
    """
    def __init__(self, max_count: int):
        self.message = f"Attempting times exceeded maximum count ({max_count}), target not achieved."
        super().__init__(self.message)