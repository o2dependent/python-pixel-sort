import cv2


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
