import cv2


def get_luminance_mask(
    image: cv2.typing.MatLike, threshold_value=128
) -> cv2.typing.MatLike:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    return mask
