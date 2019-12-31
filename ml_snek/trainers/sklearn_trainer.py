from .base_trainer import BaseTrainer


class SKLearnTrainer(BaseTrainer):
    "Trains models uing the sklearn model fitting interface"

    def __init__(self, model, dataloader, n_epochs):
        self.model = model
        self.dataloader = dataloader
        self.n_epochs = n_epochs

    def save(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    def train(self):
        i = 0
        for epoch in range(self.n_epochs):
            for i, (x, y) in enumerate(self.dataloader):
                self.model.train(x, y)
                if i % 10 == 0:
                    print(f"training {i}/{self.n_epochs}")
                if i >= self.n_epochs:
                    break
                i += 1
