import cv2
import math
from lib.constants import BAYER_MATRIX_4x4

COLOR_RANGE = [
    (155, 86, 116),
    (203, 179, 255),
    (216, 191, 216),
    (199, 251, 150),
    (174, 255, 247),
]


def add_dithering(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    # get grayscale image to have gradient to work with
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_copy = image.copy()
    width, height = gray_image.shape
    bayer_n = 4  # size of matrix
    bayer_r = 75
    # iterate over each pixel
    for i in range(width):
        for j in range(height):
            color_result = COLOR_RANGE[len(COLOR_RANGE) - 1]
            # Bayer matrix dithering equation
            bayer_value = BAYER_MATRIX_4x4[i % bayer_n][j % bayer_n] / (bayer_n**2)
            output_color = (gray_image[i, j]) + (bayer_r * bayer_value)
            output_index = min(
                len(COLOR_RANGE) - 1,
                math.floor((output_color / 255 * (len(COLOR_RANGE) - 1))),
            )

            print(output_index)

            color_result = COLOR_RANGE[int(output_index)]

            # if output_color < bayer_r / len(COLOR_RANGE) - 1:
            #     color_result = COLOR_RANGE[0]

            image_copy[i, j] = color_result

    return image_copy
