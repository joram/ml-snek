import os
import importlib

from PIL import Image

import torch
from torchvision import transforms


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


def frame_to_image(frame, winner_id):
    w = frame["board"]["height"]
    h = frame["board"]["width"]

    # The board representation is C x H x W where
    # Channels are [body pos, food pos, self head pos, other head pos]
    data = torch.zeros([4, h, w])

    # body
    current_channel = 0

    for snake in frame["board"]["snakes"]:
        body = snake["body"]
        for i in range(len(body) - 1, 1, -1):
            coord = body[i]
            data[current_channel, coord["y"], coord["x"]] = i

    # food
    current_channel += 1

    foods = frame["board"]["food"]
    for coord in foods:
        data[current_channel, coord["y"], coord["x"]] = 1

    # head
    my_head_channel = current_channel + 1
    their_head_channel = current_channel + 2

    for snake in frame["board"]["snakes"]:
        head = snake["body"][0]
        if snake["id"] == winner_id:
            data[my_head_channel, head["y"], head["x"]] = 1
        else:
            data[their_head_channel, head["y"], head["x"]] = 1

    return data


DIRECTION_DICT = {
    "UP": 0,
    "DOWN": 1,
    "LEFT": 2,
    "RIGHT": 3,
}

N_DIRECTIONS = len(DIRECTION_DICT)


def direction_to_index(direction: str) -> int:
    """Converts string representation of direction into integer

    Parameters
    ----------
    direction: str
        "UP", "DOWN", "LEFT", "RIGHT

    Returns
    -------
    direction_onehot: torch.LongTensor
        Integer representation of the direction
    """
    return torch.Tensor([DIRECTION_DICT[direction]]).long()


def direction_to_onehot(direction: str) -> torch.Tensor:
    """Converts string representation of direction into onehot

    Parameters
    ----------
    direction: str
        "UP", "DOWN", "LEFT", "RIGHT

    Returns
    -------
    direction_onehot: torch.Tensor
        Onehot representation of the direction
    """

    direction_onehot = torch.zeros(N_DIRECTIONS)
    direction_onehot[direction_to_index(direction)] = 1

    return direction_onehot


def load_object(object_name, object_kwargs):
    object_module, object_name = object_name.rsplit(".", 1)
    object_module = importlib.import_module(object_module)

    return getattr(object_module, object_name)(**object_kwargs)
