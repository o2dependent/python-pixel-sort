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
        mask = Image.new("1", image.size, 0)
        sort_image = image.copy()
        mask_pixels = mask.load()
        sort_pixels = sort_image.load()

        for i in range(sort_image.size[0]):
            sort_row = list()
            for j in range(sort_image.size[1]):
                if sort_pixels[i, j][0] > 150:
                    mask_pixels[i, j] = 0
                else:
                    mask_pixels[i, j] = 1
                sort_row.append(sort_pixels[i, j])
            sort_row.sort()
            for j in range(sort_image.size[1]):
                sort_pixels[i, j] = sort_row[j]

        mask.save("./mask.jpeg")

        composite_image = Image.composite(image, sort_image, mask)

        composite_image.save("comp.jpeg")

    except ValueError:
        print(ValueError)


main()
