import numpy
from .base_dataloader import BaseDataloader


class Dataloader(BaseDataloader):

    def __init__(self, dataset):
        self._dataset = dataset

    def _frame_to_image(self, frame, winner_id):
            w = frame["board"]["height"]
            h = frame["board"]["width"]

            data = {}
            for x in range(0, w):
                for y in range(0, h):
                    data[x, y] = 0

            # body
            body_data = data
            for snake in frame["board"]["snakes"]:
                body = snake["body"]
                for i in range(len(body)-1, 1, -1):
                    coord = body[i]
                    body_data[coord["x"], coord["y"]] = i
            body_data = list(body_data.values())

            # food
            food_data = data
            foods = frame["board"]["food"]
            for coord in foods:
                food_data[coord["x"], coord["y"]] = 1
            food_data = list(food_data.values())

            # head
            my_head_data = data
            their_head_data = data
            for snake in frame["board"]["snakes"]:
                head = snake["body"][0]
                if snake["id"] == winner_id:
                    my_head_data[head["x"], head["y"]] = 1
                else:
                    their_head_data[head["x"], head["y"]] = 1
            my_head_data = list(my_head_data.values())
            their_head_data = list(their_head_data.values())

            return numpy.array([]+body_data+food_data+my_head_data+their_head_data)

    def _string_dir_to_int(self, direction):
        return {
            "UP": 0,
            "DOWN": 1,
            "LEFT": 2,
            "RIGHT": 3,
        }[direction]

    def __getitem__(self, index):
        frame, winner_id, direction = self._dataset[index]
        input_values = self._frame_to_image(frame, winner_id)
        output_value = self._string_dir_to_int(direction)
        return input_values, output_value

    def __iter__(self):
        for frame, winner_id, direction in self._dataset:
            input_values = self._frame_to_image(frame, winner_id)
            output_value = self._string_dir_to_int(direction)
            yield input_values, output_value