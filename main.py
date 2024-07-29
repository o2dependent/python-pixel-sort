import cv2
import numpy as np
import sys
from lib.get_luminance_mask import get_luminance_mask
from lib.add_bloom import add_bloom
from lib.get_flesh_tone_mask import get_flesh_tone_mask
from lib.sort_pixels import sort_pixels
from lib.add_dithering import add_dithering
from lib.constants import OUTPUT_FOLDER


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

        sorted_result = sort_pixels(image, luminance_mask)
        inverted_sorted_result = sort_pixels(image, luminance_mask_inv)

        # bloomed = add_bloom(inverted_sorted_result)

        dithered_result = add_dithering(image)

        cv2.imshow("OG", image)
        cv2.imshow("Luminance mask", luminance_mask)
        cv2.imshow("Sorted result", sorted_result)
        cv2.imshow("Inverted sorted result", inverted_sorted_result)
        cv2.imshow("Dithered", dithered_result)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        output_path = f"{OUTPUT_FOLDER}/sorted_result.jpg"
        cv2.imwrite(output_path, sorted_result)
        output_path = f"{OUTPUT_FOLDER}/inverted_sorted_result.jpg"
        cv2.imwrite(output_path, inverted_sorted_result)
        output_path = f"{OUTPUT_FOLDER}/dithered_result.jpg"
        cv2.imwrite(output_path, dithered_result)

    except ValueError as e:
        print(f"{e}")


main()
