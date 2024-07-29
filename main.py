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


def get_luminance_mask(
    image: cv2.typing.MatLike, threshold_value=128
) -> cv2.typing.MatLike:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    return mask


def add_bloom(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    # Convert the image to grayscale to find bright regions
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to extract bright regions
    _, bright_regions = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Create a 3-channel mask from the bright regions
    bright_mask = cv2.cvtColor(bright_regions, cv2.COLOR_GRAY2BGR)

    # Apply a Gaussian blur to the bright regions mask
    blurred_mask = cv2.GaussianBlur(bright_mask, (21, 21), 0)

    # Combine the original image with the blurred bright regions mask
    bloomed_image = cv2.addWeighted(image, 1.0, blurred_mask, 0.5, 0)
    return bloomed_image


def sort_pixels(
    _image: cv2.typing.MatLike, mask: cv2.typing.MatLike
) -> cv2.typing.MatLike:
    image = _image.copy()
    width, height, _ = image.shape
    for i in range(width):
        arr = list()
        index_arr = list()
        for j in range(height):
            if mask[i, j] == 255:
                arr.append(image[i, j])
                index_arr.append(j)
            #     arr.append((j, image[i, j]))

        arr = sorted(arr, key=lambda v: v[2])

        for j in range(len(arr)):
            color = arr[j]
            index = index_arr[j]
            image[i, index] = color
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
        # flesh_tone_mask = get_flesh_tone_mask(image)
        # flesh_tone_mask_inv = cv2.bitwise_not(flesh_tone_mask)
        lum_thresh = 168
        luminance_mask = get_luminance_mask(image, lum_thresh)
        luminance_mask_inv = cv2.bitwise_not(luminance_mask, 0)

        # sorted_result = sort_pixels(image, luminance_mask)

        # luminance_mask = get_flesh_tone_mask(sorted_result)
        # luminance_mask_inv = cv2.bitwise_not(luminance_mask, 0)

        sorted_result = sort_pixels(image, luminance_mask)
        inverted_sorted_result = sort_pixels(image, luminance_mask_inv)
        # result_bg = cv2.bitwise_and(sorted_result, sorted_result, mask=luminance_mask_inv)
        # result_fg = cv2.bitwise_and(image, image, mask=luminance_mask)
        # result = cv2.add(result_bg, result_fg)

        bloomed = add_bloom(inverted_sorted_result)

        cv2.imshow("OG", image)
        cv2.imshow("Luminance mask", luminance_mask)
        cv2.imshow("Bloomed", bloomed)
        cv2.imshow("Sorted result", sorted_result)
        cv2.imshow("Inverted sorted result", inverted_sorted_result)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        output_path = "sorted_result.jpg"
        cv2.imwrite(output_path, sorted_result)
        output_path = "inverted_sorted_result.jpg"
        cv2.imwrite(output_path, inverted_sorted_result)

    except ValueError as e:
        print(f"{e}")


main()
