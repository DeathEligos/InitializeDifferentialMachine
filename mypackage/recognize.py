# mypackage\recognize.py
"""
Defines Recognizer class.
"""

from typing import Dict, List, Tuple, Union
import numpy
from pyautogui import screenshot
import os
import cv2
import logging
from PIL import Image

from mypackage.exceptions import TemplateNotFoundError


class Recognizer:
    """
    Screen Recognizer, encapsulate the logic of template loading and screen identify.

    Arguments:
        templates_dir (str): directory of template image files;
        id_to_file_name (Dict[str, str]): mapping from characteristic region id to template file name;
        confidence_threshold (float): matching confidence threshold;
        id_to_coordinate (Dict[str, Tuple[int, int, int, int]]): mapping from interface ID to characteristic region coordinates.

    Attributes:
        _file_name_to_template (Dict[str, np.ndarray]): mapping from template file name to template image data;
        _is_loaded (bool): whether template image date loaded;
        _logger (logging.Logger): log.
    """

    # Initialize matcher.
    def __init__(
        self,
        templates_dir: str,
        id_to_file_name: Dict[str, str],
        confidence_threshold: float,
        id_to_coordinate: Dict[str, List[Tuple[int, int, int, int]]]
    ) -> None:

        # Configuration parameters.
        self.templates_dir = templates_dir
        self.id_to_file_name = id_to_file_name
        self.confidence_threshold = confidence_threshold
        self.id_to_coordinate = id_to_coordinate

        # State variables.
        self._file_name_to_template: Dict[str, numpy.ndarray] = {}   # Store the templates data loaded;
        self._is_loaded = False                                      # Whether the templates has been loaded.

        # Logger.
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        self._load_templates()


    def _image_pretreat(self, image: Union[Image.Image, numpy.ndarray], if_cv: bool = False) -> numpy.ndarray:
        """
        Pretreat the image.

        Arguments:
            image (Union[PIL.Image, np.ndarray]): untreated image date
            if_cv (bool): whether the umtreated imgae in format numpy.ndarray

        Returns:
            np.ndarray: treted image data
        """

        if if_cv:
            return image
        else:
            return cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2GRAY)
    

    def _image_identify(self, screenshot: numpy.ndarray, template: numpy.ndarray) -> float:
        """
        Match screemshot with template.

        Arguments:
            image (numpy.ndarray): screenshot image data
            template (numpy.ndarray): template image data

        Returns:
            float: Confidece to treat the screenshot matches with the template. -1 means that the screenshot and template size are different, skipping matching
        """

        if screenshot.shape != template.shape:
            return -1.
        else:
            return cv2.matchTemplate(image = screenshot, templ = template, method = cv2.TM_CCOEFF_NORMED)[0][0]
    

    def _load_templates(self) -> bool:
        """
        Load interface template data and check whether there is a one-to-one correspondence between templates and interface IDs.

        Returns:
            Return True when loading successfully and checking passed.
        """
        
        # Load if and only if the templates unloaded.
        if self._is_loaded:
            return True

        # Check if the folder of templates exists.
        if not os.path.isdir(self.templates_dir):
            raise TemplateNotFoundError(self.templates_dir)

        # Traverse all templates in the folder.
        for template_file in os.listdir(self.templates_dir):
            file_name = os.path.splitext(template_file)[0]
            # Only load specified templates and ignore others.
            if file_name not in self.id_to_file_name.values(): continue
            self._logger.debug(f"Loading the template [{file_name}]...")
            # Load template image data.
            template_path = os.path.join(self.templates_dir, template_file)
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

            if template is None:
                raise TemplateNotFoundError(template_path)

            # Pretreat and record template image data.
            self._file_name_to_template[file_name] = self._image_pretreat(template, if_cv=True)

        # Makesure all characteristic region IDs have corresponding template.
        missing_ids = [id for id in self.id_to_file_name if self.id_to_file_name[id] not in self._file_name_to_template.keys()]
        if missing_ids:
            raise TemplateNotFoundError(missing_ids)

        # Load templates successfully.
        self._is_loaded = True
        self._logger.info(f"Success to load {len(self._file_name_to_template)} templates;\n")
        return True


    def match(self) -> str:
        """
        Match screen with the interface IDS.

        Obtain current screenshot, match with the templates, return the matched interface ID.

        Returns:
            str: if matched, return the interface ID; else, return "unmatched".
        """

        # Makesure the template data is loaded and corresponds to the interface IDs.
        
        
        # Obtain current screenshot.
        screen = screenshot()
        # Traverse all characteristic region IDs, crop and pretreat to obtain characteristic image.
        for region_id, region_coor in self.id_to_coordinate.items():
            character_image = self._image_pretreat(screen.crop(region_coor))
            # Calculate the confidence level.
            confidence = self._image_identify(character_image, self._file_name_to_template[self.id_to_file_name[region_id]])
            self._logger.debug(f"Interface [{region_id}] with confidence level: {confidence:.4f};")

            # Match success.
            if confidence > self.confidence_threshold:
                return region_id
        # All regions unmatched.
        return "unmatched"
