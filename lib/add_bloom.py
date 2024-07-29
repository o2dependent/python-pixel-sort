import cv2


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
