import cv2
import numpy as np


def get_flesh_tone_mask(
    image: cv2.typing.MatLike,
) -> cv2.typing.MatLike:
    lower = np.array([45, 34, 30], dtype=np.uint8)  # Lower bound for flesh tone in RGB
    upper = np.array(
        [255, 104, 183], dtype=np.uint8
    )  # Upper bound for flesh tone in RGB

    mask = cv2.inRange(image, lower, upper)

    return mask
