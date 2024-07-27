from PIL import Image
import sys


def main():
    if len(sys.argv) < 2:
        print("Missing arg for file")
        return
    path = sys.argv[1]
    if not path:
        print("Invalid arg for file")
        return
    try:
        image = Image.open(path)
        width, height = image.size
        mask = image.copy()
        mask_pixels = mask.load()

        for i in range(mask.size[0]):
            row = list()
            for j in range(mask.size[1]):
                # if mask_pixels[i, j][0] > 150:
                #     row.append((0, 0, 0))
                # else:
                #     row.append((255, 255, 255))
                row.append(mask_pixels[i, j])
            row.sort()
            for j in range(mask.size[1]):
                mask_pixels[i, j] = row[j]

        mask.save("./mask.jpeg")

    except ValueError:
        print(ValueError)


main()
