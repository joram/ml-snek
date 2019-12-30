#!/usr/bin/env python3
from ..dataloaders.dataloader import Dataloader
from ..datasets.jsnek_saved_games_dataset import JSnekDataset
from ..models.random_forest_model import RandomForestModel
from ..trainers.basic_trainer import BasicTrainer
import random


def main():
    dataset = JSnekDataset()
    dataloader = Dataloader(dataset)
    model = RandomForestModel()
    trainer = BasicTrainer(model, dataloader)
    trainer.train(epochs=10)

    # random spot check evaluation
    for i in range(0, 100):
        index = random.randint(0, len(dataset)-1)
        input_values, output_value = dataloader[index]
        expected = [output_value]
        actual = model.model.predict([input_values])
        print(f"expected: {expected}\tactual: {actual}")


if __name__ == '__main__':
    main()
