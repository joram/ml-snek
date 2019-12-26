from dataloaders.base_dataloader import BaseDataloader

from torch.utils.data import DataLoader

class Dataloader(BaseDataloader):

    def __init__(self, dataset):
        self._dataset = dataset

    def frame_to_image(self, frame, winner_id):
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

            # food
            food_data = data
            foods = frame["board"]["food"]
            for coord in foods:
                food_data[coord["x"], coord["y"]] = 1

            # head
            my_head_data = data
            their_head_data = data
            for snake in frame["board"]["snakes"]:
                head = snake["body"][0]
                if snake["id"] == winner_id:
                    my_head_data[head["x"], head["y"]] = 1
                else:
                    their_head_data[head["x"], head["y"]] = 1

            return body_data, food_data, my_head_data, their_head_data

    def __next__(self):
        for frame, winner_id, direction in self._dataset:
            body_data, food_data, my_head_data, their_head_data = self.frame_to_image(frame, winner_id)
