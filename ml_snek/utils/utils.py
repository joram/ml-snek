import os
from torchvision import transforms
from PIL import Image


def _image_to_input(pixels, w, h):
    values = []
    for x in range(0, w):
        for y in range(0, h):
            val = pixels[x, y]
            values.append(val[0])
            values.append(val[1])
            values.append(val[2])
    return values


def gen_training_data(limit=100):
    i = 0
    values = []
    trans1 = transforms.ToTensor()
    for filename in os.listdir("../images/"):
        filepath = os.path.join("../images/", filename)
        img = Image.open(filepath)
        # import matplotlib.pyplot as plt
        # plt.imshow(img)
        # plt.show()
        img_data = trans1(img)
        directions = ["UP", "DOWN", "LEFT", "RIGHT", "WFT!"]
        try:
            direction = filename.split("::")[1].replace(".png", "")
        except:
            continue
        d = directions.index(direction)
        if d == directions[-1]:
            continue
        # trans2 = transforms.ToTensor()
        # d = trans2(d)

        values.append((img_data, d))

        if i > limit:
            break
        i += 1
    return values

