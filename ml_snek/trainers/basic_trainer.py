from .base_trainer import BaseTrainer


class BasicTrainer(BaseTrainer):

    def __init__(self, model, dataloader):
        self.model = model
        self.dataloader = dataloader

    def save(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    def train(self, epochs):
        i = 0
        for input_values, output_value in self.dataloader:
            self.model.train([input_values], [output_value])
            print(f"training {output_value}")
            if i >= epochs:
                break
            i += 1
