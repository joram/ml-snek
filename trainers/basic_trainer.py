from trainers.base_trainer import BaseTrainer


class BasicTrainer(BaseTrainer):

    def __init__(self, model, dataloader):
        self.model = model
        self.dataloader = dataloader

    def save(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    def train(self, epocs=1):
        for i in range(0, epocs):
            for data in self.dataloader:
                input_values = [list(data["input"][key].values()) for key in ['body', 'food', 'my_head', 'their_heads']]
                output_value = {
                    "UP": 0,
                    "DOWN": 1,
                    "LEFT": 2,
                    "RIGHT": 3,
                }[data["output"]]
                output_values = [output_value]*4
                self.model.train(input_values, output_values)
