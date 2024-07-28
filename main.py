import cv2
import numpy as np
import sys


def get_flesh_tone_mask(
    image: cv2.typing.MatLike,
) -> cv2.typing.MatLike:
    lower = np.array([45, 34, 30], dtype=np.uint8)  # Lower bound for flesh tone in RGB
    upper = np.array(
        [255, 104, 183], dtype=np.uint8
    )  # Upper bound for flesh tone in RGB

    mask = cv2.inRange(image, lower, upper)

    return mask


def sort_pixels(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    width, height, _ = image.shape
    for i in range(width):
        row = list()
        for j in range(height):
            row.append(image[i, j])
        row = sorted(row, key=lambda v: v[0])
        for j in range(height):
            image[i, j] = row[j]
    return image


def main():
    if len(sys.argv) < 2:
        print("Missing arg for file")
        return
    path = sys.argv[1]
    if not path:
        print("Invalid arg for file")
        return
    try:
        image = cv2.imread(path)
        flesh_tone_mask = get_flesh_tone_mask(image)
        flesh_tone_mask_inv = cv2.bitwise_not(flesh_tone_mask)
        copied_image = image.copy()
        sorted_copy = sort_pixels(copied_image)
        result_bg = cv2.bitwise_and(sorted_copy, sorted_copy, mask=flesh_tone_mask)
        result_fg = cv2.bitwise_and(image, image, mask=flesh_tone_mask_inv)
        result = cv2.add(result_bg, result_fg)

        cv2.imshow("OG", image)
        cv2.imshow("Flesh tone mask", flesh_tone_mask)
        cv2.imshow("Flesh tone sorted", copied_image)
        cv2.imshow("Result", result)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except ValueError:
        print(ValueError)


main()
