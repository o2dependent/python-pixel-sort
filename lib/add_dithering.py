import cv2
import math
from lib.constants import BAYER_MATRIX_4x4

COLOR_RANGE = [0, 32, 64, 96, 128, 160, 192, 224, 255]


def add_dithering(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    # get grayscale image to have gradient to work with
    print("pre gray image")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("post gray image")
    width, height = gray_image.shape
    print("post gray image shape", width, height)
    bayer_n = 4  # size of matrix
    bayer_r = 205
    # iterate over each pixel
    for i in range(width):
        for j in range(height):
            color_result = 255
            # Bayer matrix dithering equation
            bayer_value = BAYER_MATRIX_4x4[i % bayer_n][j % bayer_n]
            output_color = max(0, gray_image[i, j] + (bayer_r * bayer_value))

            if output_color < bayer_r / 2:
                color_result = 0

            gray_image[i, j] = color_result

    return gray_image
